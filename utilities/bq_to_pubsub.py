"""Reads transactions from BigQuery and ingests
into Pub/Sub for simulating realtime scenarios."""
import json
import sys
import time
from google.cloud import bigquery
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
project_id = sys.argv[1]
topic_name = sys.argv[2]
topic_path = publisher.topic_path(project_id, topic_name)

# Construct a BigQuery client object.
client = bigquery.Client()
query = """SELECT t1.*,t2.* EXCEPT(cc_num)
FROM `qp-fraud-detection.cc_data.simulation_data` t1 
LEFT JOIN `qp-fraud-detection.cc_data.demographics` t2
ON t1.cc_num =t2.cc_num 
order by trans_date_trans_time asc limit 1000"""

print('Fetching simulated transactions from BigQuery')
query_job = client.query(query)
print('Publishing messages to Pub/Sub topic')
count=0
for row in query_job:
    row = dict(row)
    row['trans_date_trans_time'] = row['trans_date_trans_time'].strftime('%Y-%m-%d %H:%M:%S')
    row['dob'] = row['dob'].strftime('%Y-%m-%d')
    # Data must be a bytestring
    data = json.dumps(row).encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
