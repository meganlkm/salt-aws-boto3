from aws_decorators import boto_client

from aws_boto3.iam.policies import create_policy, get_policy_arn
from aws_boto3.iam.roles import attach_role_policy, create_role, detach_role_policy, get_attached_policies, get_role_arn


@boto_client('sts')
def get_account_id(client=None, region=None):
    return client.get_caller_identity()['Account']


def iam_ensure_policy(policy_name, policy_document, path=None, description=None, region=None):
    arn = get_policy_arn(policy_name)
    if not arn:
        arn = create_policy(
            policy_name=policy_name,
            policy_document=policy_document,
            description=description,
            path=path,
            region=region
        )
    return arn


def iam_ensure_role(role_name, assume_role_policy_document, region=None, path=None, description=None,
                    attach_policy_name=None, attach_policy_path=None, attach_policy_description=None,
                    attach_policy_document=None):
    policy_arn = None
    role_arn = get_role_arn(role_name)
    if not role_arn:
        role_arn = create_role(role_name, assume_role_policy_document, path, description)

    response = {'RoleArn': role_arn}

    if all([attach_policy_name, attach_policy_document]):
        policy_arn = iam_ensure_policy(
            policy_name=attach_policy_name,
            policy_document=attach_policy_document,
            path=attach_policy_path,
            description=attach_policy_description,
            region=region
        )
    response['PolicyArn'] = policy_arn
    if all([role_arn, policy_arn]):
        response['attach_role_policy'] = attach_role_policy(role_name, policy_arn)
    return response


def __policy_attachment(role_name, policies, action_fn, region=None):
    if isinstance(policies, str):
        policies = [policies]
    for policy in policies:
        if not policy.startswith('arn'):
            policy = get_policy_arn(policy)
        action_fn(role_name, policy, region=region)
    return get_attached_policies(role_name, region=region)


def iam_attach_policies(role_name, policies, region=None):
    return __policy_attachment(role_name, policies, attach_role_policy, region)


def iam_detach_policies(role_name, policies, region=None):
    return __policy_attachment(role_name, policies, detach_role_policy, region)
