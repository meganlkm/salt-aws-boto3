from aws_decorators import boto_client
from botocore.exceptions import ClientError

from aws_boto3.common import dict_to_str, object_search
from aws_boto3.lookup import lookup


@boto_client('iam')
def get_policy_arn(name, region=None, client=None):
    return object_search(
        client=client,
        paginator='list_policies',
        query="Policies[?PolicyName == '{}'].Arn".format(name),
        return_single=True
    )


@boto_client('iam')
def create_policy(policy_name, policy_document, description=None, path=None, region=None, client=None):
    for statement in policy_document.get('Statement', []):
        if statement.get('Resource'):
            if statement['Resource'].startswith('lookup'):
                lookup_request = statement['Resource'].split(':')
                lookup_request.pop(0)
                statement['Resource'] = lookup(region=region, *lookup_request)

    kwargs = {
        'PolicyName': policy_name,
        'PolicyDocument': dict_to_str(policy_document)
    }
    if path:
        kwargs['Path'] = path
    if description:
        kwargs['Description'] = description

    response = False
    try:
        response = client.create_policy(**kwargs)
        response = response['Policy']['Arn']
    except ClientError as e:
        # return '[ERROR] {}'.format(str(e))
        response = {'ERROR': str(e), 'kwargs': kwargs}
    return response
