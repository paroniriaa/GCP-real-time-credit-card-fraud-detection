# GCP-real-time-credit-card-fraud-detection

## Overview

This project aim to predict whether a credit card transaction is fradulent or not in real time. This uses a streaming dataflow pipeline to

* consume incoming transaction details from Cloud Pub/Sub
* does data preprocessing (by calling Firestore for data enrichment using transaction history)
* invokes multiple ML models deployed on AI Platform
* stores the prediction results to BigQuery and
* sends notification to another Pub/Sub topic when a transaction is predicted fraudlent for downstream consumptions

Refer the project document for details 

[Project Document](report/Project_Document.pdf)

Refer the below architecture diagram for workflow

## Architecture
<img width="1234" alt="Architecture" src="https://user-images.githubusercontent.com/44891450/168407436-1bae4106-682a-4b9d-948e-1cf53e35f9d6.png">

## Dataset

Below are the details of BigQuery tables & models used for this pattern which are publicly available on GCP BigQuery (The underlying source dataset is from project qp-fraud-detection dataset cc_datacc_data)

* Project ID: qp-fraud-detection
* Dataset name: cc_datacc_data
* Tables:

  * train_raw - Data used for ML model training
  * test_raw - Data used for ML model evaluation
  * simulation_data - Data to be used for realtime inferences
  * train_with_standard - BQ view providing features for training simple model
  * train_with_aggregates - BQ view providing features for training model with aggregates
  * test_with_standard - BQ view providing test data for evaluating simple model
  * test_with_aggregates - BQ view providing test data for evaluating model with aggregates
  * demographics - Data comprising customer demographics like name, gender, address

## Model

For this pattern, we opted for XGBoost model which worked really well while still retaining some level of model explainability. We initially used the boosted tree classifier in BigQuery ML by using standard SQL to train the model and arrive at the probability score for each transaction. Due to the imbalanced nature of the dataset, we used F1 score and AUC to evaluate the performance of the model. 

After the initial evaluation, to boost the performance of the model we derived additional features from the dataset focusing on the frequency of the transactions and the average transaction amount over a period of time. 

As part of the solution, we have used predictions from both the models as part of the pipeline. The model using the standard features gives you relatively faster results, the other model uses the features derived from looking at historical data to make the predictions.

## Model Differences

In this example, based on the fed training dataset, we have two types of models

* Model with standard features: This uses the features which are present in the dataset and doesn't rely on any feature generation techniques

* Model with aggregate fetures: Along with the provided features, this uses feature generation techniques to compute transaction frequency, average spend etc for a given credit card
  * trans_freq_24 - Number of transactions in the last 24 hours
  * trans_diff - Time difference between current transaction and last transaction in seconds
  * avg_spend_pw - Average transaction amount in the past 1 week
  * avg_spend_pm - Average transaction amount in the past 1 month

| Feature       | Derived     | Used in Model1 | Used in Model2,3,4,5,6 |
| ------------- |-------------| --------------:| --------------:|
| category      | No          | Yes            | Yes            |
| amt           | No          | Yes            | Yes            |
| gender        | No          | No             | No             |
| state         | No          | Yes            | Yes            |
| job           | No          | Yes            | Yes            |
| unix_time     | No          | Yes            | Yes            |
| city_pop      | No          | Yes            | Yes            |
| merchant      | No          | Yes            | Yes            |
| day           | Yes         | Yes            | Yes            |
| age           | Yes         | Yes            | Yes            |
| distance      | Yes         | Yes            | Yes            |
| trans_freq_24 | Yes         | No             | Yes            |
| trans_diff    | Yes         | No             | Yes            |
| avg_spend_pw  | Yes         | No             | Yes            |
| avg_spend_pm  | Yes         | No             | Yes            |

## Work Refernece and Contribution
### Reference
This project is referenced and developed based on the existing solution:

* Workflow Reference: [GCP Blog - How to build a serverless real-time credit card fraud detection solution](https://cloud.google.com/blog/products/data-analytics/how-to-build-a-fraud-detection-solution)
* BigQuery Reference: [GitLab Repo - cc_fraud_detection](https://cloud.google.com/blog/products/data-analytics/how-to-build-a-fraud-detection-solution)
* Dataset Reference: [GitHub Repo - Generate Fake Credit Card Transaction Data, Including Fraudulent Transactions](https://github.com/namebrandon/Sparkov_Data_Generation)

### Contribution
* Based on references, constructed the complete workflow for developing and deploying the GCP based severless real-time credit card fraud detection solution using Google Colab
* Trained, evaluated, and deployed different machine learning models:
  * (Deployed) BigQuery: Boost Tree Models, Deep Neural Network Model
  * (Not yet deploy) TensorFlow TFDF: Random Forest Model, Gradient Boosted Trees Model, Cart Model

### Future Work
* Deploy esisting TensorFlow TFDF models on GCP AI-Platform
* Train, evaluate, standard TensorFlow models, and deploy them
* Create clear and comprehensive data visualization on Data Studio based on the real-time stream processing of the deployed Dataflow pipeline
