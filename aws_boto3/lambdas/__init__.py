from botocore.exceptions import ClientError

from aws_boto3.common import boto_client, dict_to_str

from aws_boto3.cloudwatch import cw_ensure_log_stream
from aws_boto3.iam.roles import get_role_arn
from aws_boto3.lambdas.utils import lambda_lookup, lambda_create, publish_version


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
        status['actions'].append(
            cw_ensure_log_stream(
                log_group_name='/aws/lambda/{}'.format(function_name),
                log_stream_name='/aws/lambda/{}'.format(function_name),
                region=None
            )
        )

    return status
