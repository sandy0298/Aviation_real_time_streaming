import argparse
import json
import os
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam import window
logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
from json import loads
BIGQUERY_SCHEMA = "flight_date:DATE,flight_status:STRING,departure_airport:STRING,departure_timezone:STRING,departure_iata:STRING,departure_icao:STRING,departure_scheduled:TIMESTAMP,departure_estimated:TIMESTAMP,arrival_airport:STRING,arrival_timezone:STRING,arrival_iata:STRING,arrival_icao:STRING,arrival_scheduled:TIMESTAMP,arrival_estimated:TIMESTAMP,ariline_name:STRING,flight_number:STRING,flight_iata:STRING,message_time:TIMESTAMP"
class setenv(beam.DoFn): 
      def process(self,context,df_Bucket):
          #import jaydebeapi
          import pandas as pd
          src1='gs://'+df_Bucket+'/JAVA_JDK_AND_JAR'
          os.system('gsutil cp '+src1 + '/jdk-8u202-linux-x64.tar.gz /tmp/')
          logging.info('Jar copied to Instance..')
          logging.info('Java Libraries copied to Instance..')
          os.system('mkdir -p /usr/lib/jvm  && tar zxvf /tmp/jdk-8u202-linux-x64.tar.gz -C /usr/lib/jvm  && update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.8.0_202/bin/java" 1 && update-alternatives --config java')
          logging.info('Enviornment Variable set.')
          return list("1")

class loadingdata(beam.DoFn):
    def process(self,element,timestamp=beam.DoFn.TimestampParam):
        parsed = json.loads(element.decode("utf-8"))
        parsed["message_time"] = timestamp.to_rfc3339()
        yield parsed

def run():
    try:

    # Parsing arguments
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--input_subscription",
            help='Input PubSub subscription of the form "projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."',
            
        )
        parser.add_argument(
            "--output_table", 
            help="Bigquery table where data will reside"
        )
        parser.add_argument(
            "--output_schema",
            help="Output BigQuery Schema in text format",
            default=BIGQUERY_SCHEMA,
        )
        
        parser.add_argument(
            '--dfBucket',
            required=True,
            help= ('Bucket where JARS/JDK is present')
        )
        
        known_args, pipeline_args = parser.parse_known_args()
        global subscription_id
        subscription_id = known_args.input_subscription
        global table_id
        table_id = known_args.output_table
        
        global df_Bucket
        df_Bucket = known_args.dfBucket
        known_args, pipeline_args = parser.parse_known_args()
        
        # Creating pipeline options
        pipeline_options = PipelineOptions(pipeline_args)
        pipeline_options.view_as(StandardOptions).streaming = True
        pcoll = beam.Pipeline(options=pipeline_options)
        logging.info("Pipeline Starts")
        
        dummy= pcoll | 'Initializing..' >> beam.Create(['1'])
        dummy_env = dummy | 'Setting up Instance..' >> beam.ParDo(setenv(),df_Bucket)
        read_messages=dummy_env | "ReadFromPubSub" >> beam.io.ReadFromPubSub(subscription=known_args.input_subscription)
        add_time=read_messages | "Add timestamp to each message" >> beam.ParDo(loadingdata())
        add_window= add_time | "window" >> beam.WindowInto(window.FixedWindows(50))
        bigquery=add_window | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                known_args.output_table,
                schema=known_args.output_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            )
        p=pcoll.run()
        logging.info('Job Run Successfully!')
        p.wait_until_finish()
    except:
        logging.exception('Failed to launch datapipeline')
        raise    

if __name__ == "__main__":
    run()




