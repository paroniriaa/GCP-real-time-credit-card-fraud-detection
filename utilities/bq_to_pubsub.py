"""Reads transactions from BigQuery and ingests
into Pub/Sub for simulating realtime scenarios."""
import json
import sys
import time
from typing import Callable
from concurrent import futures
from google.cloud import bigquery
from google.cloud import pubsub_v1

def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 30 seconds for the publish call to succeed.
            print(publish_future.result(timeout=30))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback

publisher = pubsub_v1.PublisherClient()
project_id = PROJECT_ID
topic_name = PUBSUB_TOPIC_NAME
topic_path = publisher.topic_path(project_id, topic_name)
publish_futures = []

# Construct a BigQuery client object.
client = bigquery.Client()
query = """SELECT t1.*,t2.* EXCEPT(cc_num)
FROM `cmpe-255-342823.BQML_CREDIT_CARD_FRAUD.simulation_data` t1 
LEFT JOIN `cmpe-255-342823.BQML_CREDIT_CARD_FRAUD.demographics` t2
ON t1.cc_num = t2.cc_num 
ORDER BY trans_date_trans_time ASC LIMIT 100"""

print('Fetching simulated transactions from BigQuery')
query_job = client.query(query)
print('Publishing messages to Pub/Sub topic')

for row in query_job:
    row = dict(row)
    #print(row)
    #print(row['trans_date_trans_time'])
    row['trans_date_trans_time'] = row['trans_date_trans_time'].strftime('%Y-%m-%d %H:%M:%S')
    #print(row['trans_date_trans_time'])
    #print(row['dob'])
    row['dob'] = row['dob'].strftime('%Y-%m-%d')
    #print(row['dob'])
    data = json.dumps(row)
    print(data)
    # Data must be a bytestring when publishing
    # When you publish a message, the client returns a future. 
    publish_future = publisher.publish(topic_path, data.encode("utf-8"))
    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(get_callback(publish_future, data))
    publish_futures.append(publish_future)

# Wait for all the publish futures to resolve before exiting.
futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

print(f"Published messages with error handler to {topic_path}.")
