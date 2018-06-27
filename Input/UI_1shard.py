import boto3
import json
import random
import csv
import numpy as np


kinesis = boto3.client('kinesis')

zipcode = np.genfromtxt('zipcodes.csv',delimiter=",",dtype=int)

i=0
while i==i:
    input = {}
    input['UserID'] = i+1
    input['Zipcode'] = random.choice(zipcode)
    input['PartySize'] = str(random.randint(1,3))
    
    Data = json.dumps(input)
    
    response = kinesis.put_record(StreamName='UI', Data=Data, PartitionKey='partitionkey')
    i=i+1



