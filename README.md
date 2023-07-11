# Aviation Real Time Streaming

## About
This project aims to develop a credit card fraud transaction detection system for Global Bank Limited. The system utilizes historical financial and demographic data to train a model using BigQuery Machine Learning (BQML). The trained model is then deployed on Vertex AI Endpoint to perform real-time fraud prediction on incoming credit card transactions.
## Toolbox 🧰
<img src="https://image.slidesharecdn.com/googlepresents-iotatgooglescale-slideshare-150827115054-lva1-app6892/95/iot-at-google-scale-9-638.jpg?cb=1440676398" width="200" height="80" alt="Pub Sub"/> &emsp; <img src="https://lh6.googleusercontent.com/1MICxjbrbRPtEnzE54g2shaMRD2RocCIcuSOrqwaqryObCR6IrsXNb3Sd5MjBBwmoLeVcgVu_SE3vw-IbRA24SFhH4IT1xppVuuNGodDtFEykgD0Cw1vB2jITTsOgBNHvWfw27icmMs30SYgWQ" width="200" alt="GCP DTAFLOW" height="70"/>
&emsp; <img src="https://miro.medium.com/max/600/1*HEzofakm1-c4c_Qn4zjmnQ.jpeg" width ="170" height="75" alt="Apache Beam"/>
&emsp;<img src ="https://i.ytimg.com/vi/s6ytxB0YSR0/mqdefault.jpg" width="170" height="70" alt="Secret Manager"/> &emsp;
<img src ="https://th.bing.com/th/id/OIP.k11NKB6vQbDyHstjaXOJygHaCk?pid=ImgDet&rs=1" width="200" height="100" alt="Google Cloud Storage"/> &emsp;
<img src ="https://cxl.com/wp-content/uploads/2019/10/google-bigquery-logo-1.png" width="170" height="100" alt="Google Big Query"/> &emsp;
<img src ="https://www.python.org/static/community_logos/python-logo-master-v3-TM-flattened.png" width="170" height="100" alt="Python"/> &emsp;


This project aims to develop a credit card fraud transaction detection system for Global Bank Limited. The system utilizes historical financial and demographic data to train a model using BigQuery Machine Learning (BQML). The trained model is then deployed on Vertex AI Endpoint to perform real-time fraud prediction on incoming credit card transactions.

## Project Workflow:

## 1. Data Training:
   - Historical financial and demographic data is collected and stored in BigQuery.
   - BQML is used to train a credit card fraud transaction model using the collected data.

## 2. Model Deployment:
   - The trained model is deployed on Vertex AI Endpoint, which provides a scalable and reliable infrastructure for hosting machine learning models.

## 3. Real-Time Transaction Processing:
   - Incoming credit card transactions from on-prem servers are streamed to a Pub/Sub topic.
   - A streaming Dataflow pipeline is set up to retrieve each transaction record from the Pub/Sub subscriber and load it into a Firestore database.

## 4. Fraud Prediction:
   - Each transaction record is sent to the Vertex AI Endpoint for fraud prediction.
   - The endpoint analyzes the transaction and returns a result in the form of a "is_fraud" column, indicating whether the transaction is fraudulent or not.

## 5. Data Storage:
   - Based on the predicted result, the transaction record is written to the appropriate BigQuery table.
     - If the "is_fraud" column value is 0, the record is stored in the non_fraud_transaction table.
     - If the "is_fraud" column value is 1, the record is stored in the fraud_transaction_layer table.

## 6. Fraud Alert and Incident Handling:
   - For transactions flagged as fraudulent (is_fraud = 1), a record is published to another Pub/Sub topic.
   - A cloud function is triggered by the published record, which sends fraud email alerts to the respective customers and creates a high priority incident ticket in ServiceNow, a ticketing system used by the bank.
   - The cloud function fetches the required credentials from Secret Manager to access the necessary resources.

## 7. Reporting and Visualization:
   - Looker Dashboards are created to provide visual insights into both fraud and non-fraud transactions.
   - These dashboards enable stakeholders to monitor transaction patterns, detect potential fraud trends, and make data-driven decisions.

## Conclusion:
This GitHub project showcases the end-to-end workflow of a credit card fraud transaction detection system. It demonstrates the integration of various technologies such as BQML, Vertex AI Endpoint, Pub/Sub, Firestore, BigQuery, Secret Manager, and Looker Dashboards. The project aims to provide a scalable and automated solution for real-time fraud detection, alerting, and incident handling, empowering Global Bank Limited to mitigate potential financial risks and protect its customers' interests.


## Dashboard

<img src = "https://github.com/sandy0298/Aviation_real_time_streaming/blob/main/images/report1.jpg" width="800" height="600" alt="report1"/> &emsp;
<img src ="https://github.com/sandy0298/Aviation_real_time_streaming/blob/main/images/report2.jpg" width="800" height="600" alt="report2"/> &emsp;

## Link to Dashboard

https://lookerstudio.google.com/s/nB_GDX1CYq8

## Architecture Diagram

<img src ="https://github.com/sandy0298/Aviation_real_time_streaming/blob/main/aviation_data_final.png" width="800" height="600" alt="architecture"/> &emsp;

### Code structure
```
├── Home Directory
|     ├── pubsub_aviation.py
|     ├── Datastreaming_ingestion.py

 
```
## Installation Steps and deployment process
<b>1.</b>For running Dataflow We need to install Java Jdk 8 on the master node. For that we are making use of GCS Bucket to hold the JDk 8 Package and installing the dependency at run time on the master Node.<br>
<b>2.</b>first we need to run our Dataflow Pipeline script i.e datastreaming.py which will build the streaming pipeline for data ingestion activity to bigquery with a fixed window session of 50 seconds i.e data from the pubsub will be pulled to dataflow and will be ingested to bigquery in realtime. <br>
<b>3.</b> Then we need to run the pubsub_aviation.py script as it will publish the json Paylod from aviation API to the Pub/Sub topic. we have defined a sleep timer of 10 seconds in the code.<br>
<b>4.</b>For security purpose we are making use of Gcp Secret Manager to hold the Aviation Access API and are fetching them at run time.<br>
<b>5.</b>We are holding the Schema of Big Query Tables in our dataflow pipeline code.<br>
<b>6.</b> Data from Bigquery is ingested to looker studio and insights are generated with some KPIs. <br>


