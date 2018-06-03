import boto3
import gzip
import json
import logging
import os
import io
import base64
from botocore.vendored import requests

logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create IoT data plane client 
iot_client = boto3.client('iot-data')

# convert VPC Flow Log format to JSON
def vpcfl_to_json(payload):
    split_payload = payload.split(" ")
    json_payload = {
        'version': split_payload[0],
        'account-id': split_payload[1],
        'interface-id': split_payload[2],
        'srcaddr': split_payload[3],
        'dstaddr': split_payload[4],
        'srcport': split_payload[5],
        'dstport': split_payload[6],
        'protocol': split_payload[7],
        'packets': int(split_payload[8]),
        'bytes': int(split_payload[9]),
        'start': split_payload[10],
        'end': split_payload[11],
        'action': split_payload[12],
        'log-status': split_payload[13]
    }
    return json_payload

def lambda_handler(event, context):

    logger.info(json.dumps(event))
    
    decodedLogsData = base64.b64decode(event['awslogs']['data'])
    # decompress and extract data from payload
    in_ = io.BytesIO()
    in_.write(decodedLogsData)
    in_.seek(0)
    with gzip.GzipFile(fileobj=in_, mode='rb') as payload:
        gunzipped_bytes_obj = payload.read()   

    allEvents = json.loads(gunzipped_bytes_obj.decode())
    
    for log_event in allEvents['logEvents']:

        log_event_json = vpcfl_to_json(str(log_event['message']))       
        logger.info(log_event_json)
        logger.info(iot_client.publish(
            topic=os.environ['IOT_TOPIC_NAME'],
            qos=1, # at least once 
            payload=bytes(json.dumps(log_event_json), "utf-8")
            )
        )
