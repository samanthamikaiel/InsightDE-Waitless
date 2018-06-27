import base64
import json
import boto3
import datetime
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    
    
    print('Received request')
    item = None
    kinesis = boto3.client('kinesis')
    shard_id = 'shardId-000000000006'
    pre_shard_it = kinesis.get_shard_iterator(StreamName='UI8', ShardId=shard_id, ShardIteratorType='LATEST')
    shard_it = pre_shard_it ['ShardIterator']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('resturaunt-input')
    
    out = kinesis.get_records(ShardIterator=shard_it, Limit=4000)
    for record in out['Records']:
        input = json.loads(record['Data'])
        if input:
            #for ri in input:
            uid = input ['UserID']
            zc = str(input['Zipcode'])
            ps = int(input['PartySize'])
            
            response = table.scan(FilterExpression=Attr('Zipcode').eq(zc) & Attr('PartySize').eq(ps))
            
            items = response['Items']
            Output = json.dumps(items)
            waittime = Output
            
            Data = json.dumps(waittime)
            
            response = kinesis.put_record(StreamName='waittimes', Data=Data, PartitionKey='partitionkey')
