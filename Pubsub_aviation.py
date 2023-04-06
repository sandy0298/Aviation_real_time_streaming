import requests
import time
from google.cloud import pubsub_v1
import json
import pandas as pd
from json import loads
from google.cloud import secretmanager
publisher = pubsub_v1.PublisherClient()
project_id = "sandy-376313"
topic_name = "projects/sandy-376313/topics/aviation"
secret_client = secretmanager.SecretManagerServiceClient()
secret_response = secret_client.access_secret_version(
    {"name": "projects/"+project_id+"/secrets/aviation_key/versions/latest"})
secret_response = secret_response.payload.data.decode("utf-8")
my_credentials= loads(secret_response)
api_key=my_credentials["access_key"]
while True:

    params = {

        'access_key': api_key
    }

    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
    response = api_result.json()    
    for flight in response['data']:

        data1=dict(

            flight_date=flight['flight_date'],
            flight_status=flight['flight_status'],
            departure_airport=flight['departure']['airport'],
            departure_timezone=flight['departure']['timezone'],
            departure_iata=flight['departure']['iata'],
            departure_icao=flight['departure']['icao'],
            departure_scheduled=flight['departure']['scheduled'],
            departure_estimated=flight['departure']['estimated'],
            arrival_airport=flight['arrival']['airport'],
            arrival_timezone=flight['arrival']['timezone'],
            arrival_iata=flight['arrival']['iata'],
            arrival_icao=flight['arrival']['icao'],
            arrival_scheduled=flight['arrival']['scheduled'],
            arrival_estimated=flight['arrival']['estimated'],
            ariline_name=flight['airline']['name'],
            flight_number=flight['flight']['number'],
            flight_iata=flight['flight']['iata']
        )
        
        message_payload = json.dumps(data1).encode("utf-8")
        print(message_payload)
        future = publisher.publish(topic_name, data=message_payload)
        future.result()
        time.sleep(10)



    




     
