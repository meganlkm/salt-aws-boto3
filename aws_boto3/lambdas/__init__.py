from aws_decorators import boto_client
from botocore.exceptions import ClientError

from aws_boto3.common import dict_to_str
from aws_boto3.iam.roles import get_role_arn
from aws_boto3.lambdas.utils import lambda_lookup, lambda_create, publish_version
from aws_boto3.utils import run_client


@boto_client('lambda')
def lambda_invoke(function_name, payload=None, region=None, client=None, *args, **kwargs):
    kwargs = {'FunctionName': function_name}
    if payload:
        kwargs['Payload'] = dict_to_str(payload)
    response = None
    try:
        response = client.invoke(**kwargs)
        response['Payload'].read()
    except ClientError as e:
        raise e
    return response


def lambda_sync_function(function_name, handler, role_name, code, region=None, runtime='python2.7',
                         description=None, timeout=None, memory_size=None, publish=True,
                         vpc_config=None, dead_letter_config=None, environment=None,
                         kms_key_arn=None, tracing_config=None, tags=None, version=None, alias=None,
                         make_log_group=True):
    role = get_role_arn(role_name, region=region)
    status = {
        'function_name': function_name,
        'region': region,
        'actions': []
    }
    function_definition = {
        'FunctionName': function_name,
        'Runtime': runtime,
        'Role': role,
        'Handler': handler,
        'Code': code,
        'Publish': publish
    }
    if description:
        function_definition['Description'] = description
    if timeout:
        function_definition['Timeout'] = timeout
    if memory_size:
        function_definition['MemorySize'] = memory_size
    if vpc_config:
        function_definition['VpcConfig'] = vpc_config
    if dead_letter_config:
        function_definition['DeadLetterConfig'] = dead_letter_config
    if environment:
        function_definition['Environment'] = environment
    if kms_key_arn:
        function_definition['KMSKeyArn'] = kms_key_arn
    if tracing_config:
        function_definition['TracingConfig'] = tracing_config
    if tags:
        function_definition['Tags'] = tags

    lambda_arn = lambda_lookup(function_name, region=region)

    if not lambda_arn:
        status['actions'].append(lambda_create(function_definition, region=region))

    if publish:
        published = publish_version(function_name, version, alias, region)
        status['actions'].extend(published.pop('actions'))
        status.update(published)

    if make_log_group:
        try:
            run_client(
                service='logs',
                function='create_log_group',
                region=region,
                payload={
                    'logGroupName': '/aws/lambda/{}'.format(function_name)
                }
            )
        except ClientError as e:
            if 'ResourceAlreadyExistsException' not in str(e):
                raise e

    return status
