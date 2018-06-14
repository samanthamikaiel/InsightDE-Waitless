import boto3
import json
import random

kinesis = boto3.client('kinesis')

i=0
while i==i:
	input = {}
	input['ResturauntID'] = random.randint(1,10)
	input['PartySize'] = random.randint(1,3)
	input['WaitTime'] = random.randint(5,60)

	Data = json.dumps(input)
	print Data
	response = kinesis.put_record(StreamName='resturaunt_input', Data=Data, PartitionKey='partitionkey')
	i=i+1


