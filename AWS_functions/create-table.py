import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
    TableName='user-input',
    KeySchema=[
        {
            'AttributeName': 'UserID',
            'KeyType': 'HASH'
               
        },
        {
            'AttributeName': 'Zipcode',
            'KeyType': 'RANGE'
               
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'UserID',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'Zipcode',
            'AttributeType': 'N'
        }
    ],
    # pricing determined by ProvisionedThroughput
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
table.meta.client.get_waiter('table_exists').wait(TableName='hashtags')
