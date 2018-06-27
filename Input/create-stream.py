import boto3

client = boto3.client('kinesis')
response = client.create_stream(
   StreamName='RI4_fanout',
   ShardCount=4
)
