# Aviation_real_time_streaming

## About
This Project is all about Ingesting Global Aviation data to GCP BigQuery in real time using cloud Pub/Sub and Google Cloud Dataflow and building Analytical Dashboards in looker studio from the Data stored in BigQuery in real time.
## Toolbox 🧰
<img src="https://image.slidesharecdn.com/googlepresents-iotatgooglescale-slideshare-150827115054-lva1-app6892/95/iot-at-google-scale-9-638.jpg?cb=1440676398" width="200" height="80" alt="Pub Sub"/> &emsp; <img src="https://lh6.googleusercontent.com/1MICxjbrbRPtEnzE54g2shaMRD2RocCIcuSOrqwaqryObCR6IrsXNb3Sd5MjBBwmoLeVcgVu_SE3vw-IbRA24SFhH4IT1xppVuuNGodDtFEykgD0Cw1vB2jITTsOgBNHvWfw27icmMs30SYgWQ" width="200" alt="GCP DTAFLOW" height="70"/>
&emsp; <img src="https://miro.medium.com/max/600/1*HEzofakm1-c4c_Qn4zjmnQ.jpeg" width ="170" height="75" alt="Apache Beam"/>
&emsp;<img src ="https://i.ytimg.com/vi/s6ytxB0YSR0/mqdefault.jpg" width="170" height="70" alt="Secret Manager"/> &emsp;
<img src ="https://th.bing.com/th/id/OIP.k11NKB6vQbDyHstjaXOJygHaCk?pid=ImgDet&rs=1" width="200" height="100" alt="Google Cloud Storage"/> &emsp;
<img src ="https://cxl.com/wp-content/uploads/2019/10/google-bigquery-logo-1.png" width="170" height="100" alt="Google Big Query"/> &emsp;
<img src ="https://www.python.org/static/community_logos/python-logo-master-v3-TM-flattened.png" width="170" height="100" alt="Python"/> &emsp;

## Architecture Diagram

<img src ="https://github.com/choco30/Sap_Hana_To_Big_Query_Ingestion/blob/main/SAP%20To%20Big%20Query%20architecture%20Diagram.png" width="900" height="900" alt="Python"/> &emsp;

### Code structure
```
├── Home Directory
|     ├── Sap_Dataflow
|     |     ├── sap_dataflow_job.py
├──Setup.py
 
```
## Installation Steps
<b>1.</b>For running Dataflow We need to install Java Jdk 8 on the master node. For that we are making use of GCS Bucket to hold the JDk 8 Package and installing the dependency at run time on the master Node.<br>
<b>2.</b>We are making use of <b> Setup.py </b> file to pass on the list of all the dependency that needs to be installed at run time on the worker nodes.
A better production approach could be to make a custom container having all the required dependency installed and will be provided to the dataflow job at run time which will increases the job efficiency as need to install dependency seprately on each worker node during up scalling will vanquish. <br>
<b>3.</b>For security purpose we are making use of Gcp Secret Manager to hold the SAP HANA Login Credentials and are fetching them at run time.<br>
<b>4.</b>We are holding the Schema of Big Query Tables as json in GCS Bucket and fetching them at run time.<br>


## Deployment Process
### Triggering dataflow Job
For Running Dataflow Job we are making use of Gcp composer which is the maged version of apache airflow to orchestrate the entire ELT Pipeline which is scheduled dat daily midnight. we are making use of SMTPLIB library to sent the email notification in case of success and failuer of Job. 
