import logging

from aws_decorators import boto_client

from aws_boto3.common import object_search

logger = logging.getLogger(__name__)


def __alias_name(alias):
    if not alias.startswith('alias/'):
        return 'alias/{}'.format(alias)
    return alias


@boto_client('kms')
def get_alias_attr(alias, return_attr='AliasArn', region=None, client=None):
    q = "Aliases[?AliasName=='{}']".format(__alias_name(alias))
    if return_attr.lower() == 'all':
        q += " | [0]"
    else:
        q += ".{}".format(return_attr)
    return object_search(
        client=client,
        paginator='list_aliases',
        query=q
    )


@boto_client('kms')
def kms_list_keys(client=None, region=None):
    response = client.list_keys()
    return [key['KeyId'] for key in response['Keys']]


@boto_client('kms')
def kms_create_key(description, policy=None, bypass_policy_lockout_safety_check=False,
                   key_usage='ENCRYPT_DECRYPT', origin='AWS_KMS', tags=[],
                   region=None, client=None):
    create_key_params = {
        'Description': description,
        'BypassPolicyLockoutSafetyCheck': bypass_policy_lockout_safety_check,
        'KeyUsage': key_usage,
        'Origin': origin,
        'Tags': tags
    }
    if policy:
        create_key_params['Policy'] = policy
    logger.debug({'create_key_params': create_key_params})
    return client.create_key(**create_key_params).get('KeyMetadata')


@boto_client('kms')
def kms_create_alias(alias_name, key_id, region=None, client=None):
    alias_name = __alias_name(alias_name)
    create_alias_params = {
        'AliasName': alias_name,
        'TargetKeyId': key_id
    }
    logger.debug({'create_alias_params': create_alias_params})
    try:
        client.create_alias(**create_alias_params)
    except Exception as e:
        logger.error(str(e))
        return False
    return True


def kms_ensure_key(alias_name, description=None, policy=None, bypass_policy_lockout_safety_check=False,
                   key_usage='ENCRYPT_DECRYPT', origin='AWS_KMS', tags=[], region=None):
    alias_name = __alias_name(alias_name)
    key_alias = get_alias_attr(alias_name, region=region)

    if not key_alias:
        logger.debug('[kms_ensure_key] key does not exist... creating it...')
        if description is None:
            description = alias_name

        key = kms_create_key(
            description=description,
            policy=policy,
            bypass_policy_lockout_safety_check=bypass_policy_lockout_safety_check,
            key_usage=key_usage,
            origin=origin,
            tags=tags,
            region=region
        )
        if kms_create_alias(alias_name, key['KeyId'], region=region):
            # need to get the new alias arn
            key_alias = get_alias_attr(alias_name, region=region)

    return key_alias
