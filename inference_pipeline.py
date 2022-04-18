import argparse
import json
import logging
from math import cos, asin, sqrt, pi
import time
import warnings
from datetime import datetime, timedelta
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from google.cloud import bigquery
from google.cloud import firestore
from googleapiclient import discovery

warnings.filterwarnings(action='ignore')


def distance(lat1, lon1, lat2, lon2):
    """Given two locations with latitude and longitude,
    calculates distance between them"""
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a))

class LookupFirestore(beam.DoFn):
    """Lookups firestore and computes aggregate features 
    required for ML model inference"""
    def __init__(self, project_id, firestore_collection):
        self.project_id = project_id
        self.firestore_collection = firestore_collection
        pass

    def start_bundle(self):
        self.db = firestore.Client(project=self.project_id)

    def process(self, elem):
        trans_date_trans_time = datetime.strptime(elem['trans_date_trans_time'], '%Y-%m-%d %H:%M:%S')
        last_day_date_ts = trans_date_trans_time - timedelta(days=1)
        last_week_date_ts = trans_date_trans_time - timedelta(days=7)
        last_month_date_ts = trans_date_trans_time - timedelta(days=30)
        # Day adjustment, weekday treat Sunday as 6 and BigQuery treats Sunday as 1
        elem['day'] = (trans_date_trans_time.weekday()+2)%7
        # Age of the customer at the time of transaction
        elem['age'] = round((trans_date_trans_time - datetime.strptime(elem['dob'], '%Y-%m-%d')).days/365,2)
        # Distance between customer location and merchant location
        elem['distance'] = round(distance(elem['lat'],elem['long'], elem['merch_lat'],elem['merch_long']),2)
        # Lookup firestore and fetch document for a particular credit card number
        cc_num = elem['cc_num']
        db_ref = self.db.collection(self.firestore_collection)
        query = db_ref.where(u'cc_num', u'==', cc_num)
        docs = query.get()
        # If Firestore returns zero documents, add the document with the current transaction
        if not docs:
            print("No document")
            doc_ref = db_ref.add({
                'cc_num': elem['cc_num'],
                'trans_details': [{
                    'amt': elem['amt'],
                    'trans_date_trans_time': trans_date_trans_time.replace(tzinfo=None)
                }]
                
            })
            print(f'Added document with ID{doc_ref[1].id}')
            elem['trans_diff'] = 0
            elem['avg_spend_pw'] = 0
            elem['avg_spend_pm'] = 0
            elem['trans_freq_24'] = 0
        # Incase of an existing document, update the transaction history
        else:
            for item in docs:
                doc = {
                    'id': item.id,
                    'doc': item.to_dict()
                }
            trans_details = doc['doc']['trans_details']
            # if transaction history is available, compute the derived features 
            if trans_details:
                last_trans_time = trans_details[0]['trans_date_trans_time'].replace(tzinfo=None)
                elem['trans_diff'] = int((trans_date_trans_time - last_trans_time).total_seconds()/60)
                
                trans_freq_24 = 0
                last_week_freq = 0
                last_week_spend = 0
                last_month_freq = 0
                last_month_spend = 0
                for i,trans in enumerate(trans_details):
                    if  trans['trans_date_trans_time'].replace(tzinfo=None) >= last_month_date_ts:
                        last_month_freq +=1
                        last_month_spend += trans['amt']
                    else:
                        break
                    if trans['trans_date_trans_time'].replace(tzinfo=None) >= last_week_date_ts:
                        last_week_freq +=1
                        last_week_spend += trans['amt']
                    if  trans['trans_date_trans_time'].replace(tzinfo=None) >= last_day_date_ts:
                        trans_freq_24 +=1
                
                trans_details = trans_details[:i]
                elem['avg_spend_pw'] = last_week_spend/last_week_freq if last_week_freq else 0
                elem['avg_spend_pm'] = last_month_spend/last_month_freq  if last_month_freq else 0
                elem['trans_freq_24'] = trans_freq_24
            # in case of no history, provide default values
            else:
                elem['trans_diff'] = 0
                elem['avg_spend_pw'] = 0
                elem['avg_spend_pm'] = 0
                elem['trans_freq_24'] = 0

            # Insert the current transaction at the starting of the transaction history
            trans_details.insert(0, {'amt':elem['amt'], 'trans_date_trans_time': trans_date_trans_time})
            doc_ref = db_ref.document(doc['id'])
            doc_ref.update({'trans_details': trans_details})

        return[elem]


class InvokeMLEndpoint(beam.DoFn):
    """Sends two requests to AI platform hosted models, 
    one for model without aggregates and one for model with aggregates"""
    def __init__(self, project_id, model_name, model_w_agg, model_wo_agg):
        # Full qualifier paths for the models hosted on AI Platform
        self.model_w_agg = f'projects/{project_id}/models/{model_name}/versions/{model_w_agg}'
        self.model_wo_agg = f'projects/{project_id}/models/{model_name}/versions/{model_wo_agg}'

    def start_bundle(self):
        self.service = discovery.build('ml', 'v1', cache_discovery=False)

    def process(self, elem):
        def predict_json(model_full_name, instances):
            response = self.service.projects().predict(
                name=model_full_name,
                body={'instances': instances}
            ).execute()
            if 'error' in response:
                print(response)
                return 'Fail', response['error']

            return 'Success', response['predictions']

        # Request Instance for model without aggregates
        wo_agg_instance = [{
            "category": elem['category'],
            "amt": elem['amt'],
            "state": elem['state'],
            "job": elem['job'],
            "unix_time": elem['unix_time'],
            "city_pop": elem['city_pop'],
            "merchant": elem['merchant'],
            "day": elem['day'],
            "age": elem['age'],
            "distance": elem['distance']
        }]
        # Get prediction and store prediction and confidence scores
        output = predict_json(self.model_wo_agg, wo_agg_instance)
        if output[0]=='Success':
            elem['is_fraud_model_wo_aggregates'] = int(output[1][0]['predicted_is_fraud'])
            elem['prob_is_fraud_model_wo_aggregates'] = [round(output[1][0]['is_fraud_probs'][0],5), round(output[1][0]['is_fraud_probs'][1],5)]

        # Request Instance for model with aggregates
        w_agg_instance = [{
            "category": elem['category'],
            "amt": elem['amt'],
            "state": elem['state'],
            "job": elem['job'],
            "unix_time": elem['unix_time'],
            "city_pop": elem['city_pop'],
            "merchant": elem['merchant'],
            "day": elem['day'],
            "age": elem['age'],
            "distance": elem['distance'],
            "trans_freq_24": elem['trans_freq_24'],
            "trans_diff": elem['trans_diff'],
            "avg_spend_pw": elem['avg_spend_pm'],
            "avg_spend_pm": elem['avg_spend_pw'],
        }]
        # Get prediction and store prediction and confidence scores
        
        output = predict_json(self.model_w_agg, w_agg_instance)
        if output[0]=='Success':
            elem['is_fraud_model_w_aggregates'] = int(output[1][0]['predicted_is_fraud'])
            elem['prob_is_fraud_model_w_aggregates'] = [round(output[1][0]['is_fraud_probs'][0],5), round(output[1][0]['is_fraud_probs'][1],5)]

        return [elem]

class FilterFraud(beam.DoFn):
    def __init__(self):
        pass

    def process(self, elem):
        """Filter transactions which are predicted as fraud by model with aggregates or any prioritized model"""
        if elem['is_fraud_model_w_aggregates'] and elem['is_fraud_model_w_aggregates']==1:
            return[str(elem).encode('utf-8')]


def run(argv=None):
    """Run the workflow."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--firestore-project',
                        dest='firestore_project',
                        required=True,
                        help='Firestore Project ID')
    parser.add_argument('--subscription-name',
                        dest='subscription_name',
                        required=True,
                        help='PubSub subscription name to be consumed')
    parser.add_argument('--firestore-collection',
                        dest='firestore_collection',
                        required=True,
                        help='Collection ID storing transaction details')
    parser.add_argument('--dataset-id',
                        dest='dataset_id',
                        required=True,
                        help='BigQuery dataset ID containing transaction data')
    parser.add_argument('--table-name',
                        dest='table_name',
                        required=True,
                        help='BigQuery table name containing transaction data')
    parser.add_argument('--model-name',
                        dest='model_name',
                        required=True,
                        help='AI Platform model name')
    parser.add_argument('--model-with-aggregates',
                        dest='model_w_agg',
                        required=True,
                        help='Version name of the model with aggregates')
    parser.add_argument('--model-without-aggregates',
                        dest='model_wo_agg',
                        required=True,
                        help='Version name of the model without aggregates')
    parser.add_argument('--fraud-notification-topic',
                        dest='fraud_notification_topic',
                        required=True,
                        help='PubSub topic name to receive notification on fraud transactions')

    known_args, pipeline_args = parser.parse_known_args(argv)

    project_id = known_args.firestore_project
    subscription_name = known_args.subscription_name
    firestore_collection = known_args.firestore_collection
    dataset_id = known_args.dataset_id
    table_name = known_args.table_name
    model_name = known_args.model_name
    model_w_agg = known_args.model_w_agg
    model_wo_agg = known_args.model_wo_agg
    fraud_notification_topic = known_args.fraud_notification_topic
    
    subscription_full_path = f'projects/{project_id}/subscriptions/{subscription_name}'

    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True

    p = beam.Pipeline(options = pipeline_options)

    input_transactions = p | "Read txns from PubSub" >> beam.io.ReadFromPubSub(subscription = subscription_full_path)

    processed_data = input_transactions | "Convert to JSON" >> beam.Map(lambda x: json.loads(x)) \
        | "Lookup Historical txns" >> beam.ParDo(LookupFirestore(project_id, firestore_collection))

    ml_output = processed_data | "Invoke ML Model" >> beam.ParDo(InvokeMLEndpoint(project_id, model_name, model_w_agg, model_wo_agg))
    ml_output | "Filter fraudulent txns" >> beam.ParDo(FilterFraud()) \
        | "Notifications to PubSub" >> beam.io.WriteToPubSub(topic = f'projects/{project_id}/topics/{fraud_notification_topic}')
    ml_output | "Write pred to BigQuery" >> beam.io.WriteToBigQuery(
            table=f'{project_id}:{dataset_id}.{table_name}',
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
            method="STREAMING_INSERTS")

    result = p.run()


if __name__ == "__main__":
    run()
