"""Reads past transaction history from BigQuery and loads them
into Firestore for enabling lookups during Dataflow pipeline"""
from datetime import datetime
import sys
import time
from google.cloud import bigquery
from google.cloud import firestore

db = firestore.Client(project=sys.argv[1])
db_ref = db.collection(sys.argv[2])
# Construct a BigQuery client object.
bq_client = bigquery.Client()
# Fetching approximately last 1 month data from BQ
query = '''WITH t1 AS (SELECT cc_num, amt, trans_date_trans_time FROM `qp-fraud-detection.cc_data.train_raw`
UNION ALL 
SELECT cc_num, amt, trans_date_trans_time FROM `qp-fraud-detection.cc_data.test_raw`),
t2 AS (SELECT * FROM t1 WHERE trans_date_trans_time > TIMESTAMP('2020-11-01 00:00:00 UTC'))
SELECT cc_num, ARRAY_AGG(STRUCT(amt, trans_date_trans_time) ORDER BY trans_date_trans_time desc) AS trans_details FROM t2 GROUP BY cc_num
'''

print('Fetching transaction history from BigQuery')
query_job = bq_client.query(query)
print('Loading transaction history into Firestore')
count = 0
start = time.time()
# Create documents in Firestore
for row in query_job:
    db_ref.add({
        "cc_num": row['cc_num'],
        "trans_details": row['trans_details']
    })
    count += 1
end = time.time()
print('Took {} sec to ingest past transaction history of {} customers'.format(round(end-start,1), count))
