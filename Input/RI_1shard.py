import boto3
import json
import random
import csv
import pandas
import time

colnames = ['RID','Name','ZIPCODE']
data = pandas.read_csv ('New_York_City_Restaurant.csv', names=colnames)
zipcode = data.ZIPCODE.tolist()
name = data.Name.tolist()
#print zipcode
kinesis = boto3.client('kinesis')

i=0
while i==i:
    start = time.time()
    ResturauntID = random.randint(1,1000)
    input = {}
    input['ResturauntID'] = ResturauntID
    input['Zipcode']=zipcode[ResturauntID]
    input['ResturauntName']=name[ResturauntID]
    input['PartySize'] = random.randint(1,6)
    input['WaitTime'] = random.randint(0,60)

    Data = json.dumps(input)
    response = kinesis.put_record(StreamName='RI', Data=Data, PartitionKey='partitionkey')
    print time.time()-start, 'sec'
    i=i+1


