from botocore.exceptions import ClientError

from aws_boto3.common import boto_client


@boto_client('logs')
def make_log_group(log_group_name, region=None, client=None):
    try:
        client.create_log_group(logGroupName=log_group_name)
    except ClientError as e:
        if 'ResourceAlreadyExistsException' not in str(e):
            raise e


@boto_client('logs')
def make_log_stream(log_stream_name, log_group_name, region=None, client=None):
    try:
        client.create_log_stream(logStreamName=log_stream_name, logGroupName=log_group_name)
    except ClientError as e:
        if 'ResourceAlreadyExistsException' not in str(e):
            raise e


def cw_ensure_log_stream(log_group_name, log_stream_name, region=None):
    make_log_group(log_group_name, region=region)
    make_log_stream(log_stream_name, log_group_name, region=region)
    return {
        'logGroupName': log_group_name,
        'logStreamName': log_stream_name
    }
