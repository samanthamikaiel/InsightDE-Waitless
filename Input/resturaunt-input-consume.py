import boto3
import time
import json
import datetime
import decimal

kinesis = boto3.client('kinesis')
shard_id = 'shardId-000000000000'
pre_shard_it = kinesis.get_shard_iterator(StreamName='resturaunt_input', ShardId=shard_id, ShardIteratorType='LATEST')
shard_it = pre_shard_it ['ShardIterator']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('resturaunt-input')

i=1
while i==1:
    out = kinesis.get_records(ShardIterator=shard_it, Limit=1000)
    #time.sleep(0.2)
    #print out
    if not out['Records']:
        i=0
        break
    for record in out['Records']:
            input = json.loads(record['Data'])
            if input:
                #for ri in input:
                rid = input['ResturauntID']
                ps = input['PartySize']
                wt = input['WaitTime']
                print rid
                
                checkItemExists = table.get_item(Key={'ResturauntID':rid,'PartySize':ps})
                if 'Item' in checkItemExists:
                    response = table.update_item(
                                            Key={'ResturauntID':rid,'PartySize':ps},#Key={'resturaunt-input': rid},
                                                UpdateExpression="set WaitTime=:val",
                                            #ConditionExpression="attribute_exists(ResturauntID)",
                                                ExpressionAttributeValues={':val': wt},
                                                ReturnValues="UPDATED_NEW")
                else:
                    response = table.update_item(
                                                Key={'ResturauntID':rid,'PartySize':ps},
                                                UpdateExpression="set WaitTime=:val",
                                                ExpressionAttributeValues={':val': wt},
                                                ReturnValues="UPDATED_NEW")

    shard_it = out["NextShardIterator"]
    #time.sleep(1.0)
