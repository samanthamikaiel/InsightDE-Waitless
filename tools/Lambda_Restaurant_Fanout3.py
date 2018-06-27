import base64
import json
import boto3
import datetime


def lambda_handler(event, context):
    
    kinesis = boto3.client('kinesis')
    shard_id = 'shardId-000000000003'
    pre_shard_it = kinesis.get_shard_iterator(StreamName='Fanout3', ShardId=shard_id, ShardIteratorType='LATEST')
    shard_it = pre_shard_it ['ShardIterator']
    
    print('Received request')
    item = None
    dynamo_db = boto3.resource('dynamodb')
    table = dynamo_db.Table('resturaunt-input')
    
    out = kinesis.get_records(ShardIterator=shard_it, Limit=4000)
    for record in out['Records']:
        input = json.loads(record['Data'])
        if input:
            rid = input['ResturauntID']
            ps = input['PartySize']
            wt = input['WaitTime']
            zc = input ['Zipcode']
            rn = input ['ResturauntName']
            
            checkItemExists = table.get_item(Key={'ResturauntID':rid,'PartySize':ps})
                if 'Item' in checkItemExists:
                    response = table.update_item(
                                                 Key={'ResturauntID':rid,'PartySize':ps},
                                                 UpdateExpression="set WaitTime=:val, Zipcode=:val1, ResturauntName=:val2",
                                                 ExpressionAttributeValues={':val': wt,':val1':zc, ':val2':rn},
                                                 ReturnValues="UPDATED_NEW")
                else:
                    response = table.update_item(
                                                 Key={'ResturauntID':rid,'PartySize':ps},
                                                 UpdateExpression="set WaitTime=:val, Zipcode=:val1, ResturauntName=:val2",
                                                 ExpressionAttributeValues={':val': wt,':val1':zc, ':val2':rn},
                                                 ReturnValues="UPDATED_NEW")
