def lambda_handler(event, context):
import json
import boto3

kinesis = boto3.client('kinesis')
cw = boto3.client('cloudwatch')

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    
    streamName = message['Trigger']['Dimensions'][0]['value']
    stream = kinesis.describe_stream(
                                     StreamName=streamName
                                     )
        
                                     #determine total number of shards in the stream
                                     totalShardCount = len(stream['StreamDescription']['Shards'])
                                     lastShardId = stream['StreamDescription']['Shards'][totalShardCount - 1]['ShardId']
                                     while(stream['StreamDescription']['HasMoreShards']):
                                         stream = kinesis.describe_stream(
                                                                          StreamName=streamName,
                                                                          ExclusiveStartShardId=lastShardId
                                                                          )
                                             currentShardCount = len(stream['StreamDescription']['Shards'])
                                             totalShardCount += currentShardCount
                                                 lastShardId = stream['StreamDescription']['Shards'][currentShardCount - 1]['ShardId']

#double the shard count in the stream
kinesis.update_shard_count(
                           StreamName=streamName,
                           TargetShardCount=totalShardCount * 0.5,
                           ScalingType='UNIFORM_SCALING'
                           )
    
    #double the threshold for the CloudWatch alarm that triggered this function
    cw.put_metric_alarm(
                        AlarmName=message['AlarmName'],
                        AlarmActions=[event['Records'][0]['Sns']['TopicArn']],
                        MetricName=message['Trigger']['MetricName'],
                        Namespace=message['Trigger']['Namespace'],
                        Statistic=message['Trigger']['Statistic'].title(),
                        Dimensions=[
                                    {
                                    'Name': message['Trigger']['Dimensions'][0]['name'],
                                    'Value': message['Trigger']['Dimensions'][0]['value']
                                    }
                                    ],
                        Period=message['Trigger']['Period'],
                        EvaluationPeriods=message['Trigger']['EvaluationPeriods'],
                        Threshold=message['Trigger']['Threshold'] * 0.5,
                        ComparisonOperator=message['Trigger']['ComparisonOperator']
                        )
