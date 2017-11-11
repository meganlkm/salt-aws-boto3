from aws_decorators import boto_client
from botocore.exceptions import ClientError

from aws_boto3.common import object_search


@boto_client('lambda')
def lambda_lookup(name, return_attr='FunctionArn', client=None, region=None):
    return object_search(
        client=client,
        paginator='list_functions',
        query="Functions[?FunctionName == '{}'].{}".format(name, return_attr),
        return_single=True
    )


@boto_client('lambda')
def lambda_create(function_definition, client=None, region=None):
    status = {
        'status': None,
        'exists': False
    }
    try:
        response = client.create_function(**function_definition)
        status['status'] = 'Created'
        status['exists'] = True
        status['response'] = response
    except ClientError as e:
        raise e
    return {'lambda_create': status}


@boto_client('lambda')
def publish_version(function_name, version, alias, region=None, client=None):
    response = {'actions': []}
    publish_response = client.publish_version(
        FunctionName=function_name,
        Description=version
    )
    response['lambda_version'] = publish_response.get('Version')
    response['actions'].append({'publish_version': publish_response})
    try:
        alias_response = client.create_alias(
            FunctionName=function_name,
            Name=alias,
            FunctionVersion=response['lambda_version']
        )
        response['actions'].append({'create_alias': alias_response})
    except ClientError as e:
        if 'Alias already exists' not in str(e):
            # TODO
            raise e
    response['alias'] = alias
    return response
