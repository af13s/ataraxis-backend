import boto3

AWS_ACCESS_KEY_ID='AKIA2EWPK2SSZVRE734J'
AWS_SECRET_ACCESS_KEY = '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'
REGION_NAME='us-east-1'


session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
dynamodb = session.resource('dynamodb',region_name=REGION_NAME)

tablename = "experiences"


table = dynamodb.create_table(
    TableName=tablename ,
    KeySchema=[
        {
            'AttributeName': 'EventId',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'EventStart',
            'KeyType': 'RANGE'
        },
        
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'EventId',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'EventStart',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
	)

table.meta.client.get_waiter('table_exists').wait(TableName=tablename)

print("table created")