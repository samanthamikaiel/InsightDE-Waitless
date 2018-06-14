import boto3

client = boto3.client('kinesis')
response = client.create_stream(
   StreamName='user_input',
   ShardCount=1
)
