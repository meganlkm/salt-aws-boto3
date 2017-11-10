import logging

from aws_decorators import boto_client
from botocore.exceptions import ClientError

from aws_boto3.common import dict_to_str, object_search

logger = logging.getLogger(__name__)


@boto_client('ecr')
def get_repo_attr(name, return_attr='repositoryArn', region=None, client=None):
    return object_search(
        client=client,
        paginator='describe_repositories',
        query="repositories[?repositoryName == '{}'].{}".format(name, return_attr),
        return_single=True
    )


@boto_client('ecr')
def ecr_ensure_repo(repo_name, policy=None, region=None, client=None):
    response = {
        'repositoryArn': get_repo_attr(repo_name, region=region)
    }
    if not response['repositoryArn']:
        try:
            response['create_repository'] = client.create_repository(repositoryName=repo_name)
            response['repositoryArn'] = response['create_repository']['repository']['repositoryArn']
        except ClientError:
            # TODO
            raise
    if policy:
        try:
            response['set_repository_policy'] = client.set_repository_policy(
                repositoryName=repo_name,
                policyText=dict_to_str(policy)
            )
        except ClientError:
            # TODO
            raise
    return response


@boto_client('ecr')
def ecr_absent_repo(repo_name, force=False, registry_id=None, region=None, client=None):
    response = False
    repo_arn = get_repo_attr(repo_name)
    if repo_arn:
        kwargs = {
            'repositoryName': repo_name,
            'force': force
        }
        if registry_id:
            kwargs['registryId'] = registry_id
        try:
            client.delete_repository(**kwargs)
            response = {'RepositoryAbsent': repo_name}
        except Exception as e:
            response = {'ERROR': str(e)}
            logger.exception(str(e))
    else:
        response = {'RepositoryAbsent': repo_name}
    return response
