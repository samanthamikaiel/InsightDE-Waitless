import boto3
import json
import random
import csv
import pandas


kinesis = boto3.client('kinesis')

zipcode = np.genfromtxt('zipcodes.csv',delimiter=",",dtype=int)

i=0
while i==i:
    input = {}
    input['UserID'] = i+1
    input['Zipcode'] = random.choice(zipcode)
    input['PartySize'] = str(random.randint(1,3))
    
    Data = json.dumps(input)
    print Data
    response = kinesis.put_record(StreamName='UI8', Data=Data, PartitionKey='partitionkey')
    i=i+1



