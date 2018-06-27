import boto3
import time
import json
import datetime
import decimal
import time

kinesis = boto3.client('kinesis')
shard_id = 'shardId-000000000000'
pre_shard_it = kinesis.get_shard_iterator(StreamName='RI', ShardId=shard_id, ShardIteratorType='LATEST')
shard_it = pre_shard_it ['ShardIterator']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('RInput')

time.sleep(1.0)

i=1
while i==1:
    start=time.time()
    out = kinesis.get_records(ShardIterator=shard_it, Limit=4000)
    #time.sleep(0.2)
    #print out
    if not out['Records']:
        i=1
        print 'no more records'
        break
    for record in out['Records']:
            input = json.loads(record['Data'])
            if input:
                #for ri in input:
                rid = input['ResturauntID']
                ps = input['PartySize']
                wt = input['WaitTime']
                zc = input ['Zipcode']
                rn = input ['ResturauntName']
                #print rid
                
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
    print time.time()-start, 'sec'
    shard_it = out["NextShardIterator"]
#time.sleep(1.0)
