import boto3
import time
import json
import datetime
import decimal
from boto3.dynamodb.conditions import Key, Attr

kinesis = boto3.client('kinesis')
shard_id = 'shardId-000000000006'
pre_shard_it = kinesis.get_shard_iterator(StreamName='UI8', ShardId=shard_id, ShardIteratorType='LATEST')
shard_it = pre_shard_it ['ShardIterator']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('resturaunt-input')


i=1
while i==1:
    out = kinesis.get_records(ShardIterator=shard_it, Limit=1000)
    print out
    if not out['Records']:
        i=0
        print "records not found"
        break
    for record in out['Records']:
        input = json.loads(record['Data'])
        if input:
            uid = input ['UserID']
            zc = str(input['Zipcode'])
            ps = int(input['PartySize'])

            response = table.scan(FilterExpression=Attr('Zipcode').eq(zc) & Attr('PartySize').eq(ps))
            
            items = response['Items']
            print(items)


shard_it = out["NextShardIterator"]
