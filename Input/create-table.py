import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
    TableName='RInput',
    KeySchema=[
        {
            'AttributeName': 'ResturauntID',
            'KeyType': 'HASH'
               
        },
        {
            'AttributeName': 'PartySize',
            'KeyType': 'RANGE'
               
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'ResturauntID',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'PartySize',
            'AttributeType': 'N'
        }
    ],
    # pricing determined by ProvisionedThroughput
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)
table.meta.client.get_waiter('table_exists').wait(TableName='hashtags')
