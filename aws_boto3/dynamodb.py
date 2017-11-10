from aws_decorators import boto_client
from botocore.exceptions import ClientError


@boto_client('dynamodb')
def ddb_get_table(table_name, region=None, client=None):
    table = False
    try:
        table = client.describe_table(TableName=table_name)
    except ClientError:
        table = False
    return table
