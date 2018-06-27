import boto3
import json
import random
import csv
import pandas


kinesis = boto3.client('kinesis')

colnames = ['RID','Name','ZIPCODE']
data = pandas.read_csv ('New_York_City_Restaurant.csv', names=colnames)
zipcode = data.ZIPCODE.tolist()

i=0
while i==i:
    input = {}
    input['UserID'] = i+1
    input['Zipcode'] = random.choice(zipcode)
    input['PartySize'] = str(random.randint(1,3))
    
    Data = json.dumps(input)
    print Data
  
    response = kinesis.put_record(StreamName='UI8', Data=Data, PartitionKey='partitionkey')
    print response
    i=i+1



