import base64
import json

import boto3
import datetime


def lambda_handler(event, context):
    """
        Receive a batch of events from Kinesis and insert into our DynamoDB table
        """
    print('Received request')
    item = None
    dynamo_db = boto3.resource('dynamodb')
    table = dynamo_db.Table('resturaunt-input')
    decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in event['Records']]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]
    
    with table.batch_writer() as batch_writer:
        for item in deserialized_data:
            # Add a processed time so we have a rough idea how far behind we are
            item['processed'] = datetime.datetime.utcnow().isoformat()
            batch_writer.put_item(Item=item)

# Print the last item to make it easy to see how we're doing


