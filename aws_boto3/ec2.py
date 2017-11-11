from aws_decorators import boto_client


@boto_client('elb')
def ensure_elb(elb_def, region=None, client=None):
    response = client.create_load_balancer(**elb_def)
    return response['DNSName']


@boto_client('ec2')
def ensure_sg(sg_def, region=None, client=None):
    group = client.create_security_group(**sg_def['group'])
    group_id = group['GroupId']

    egress_rules = []
    if 'egress' in sg_def:
        egress_rules = sg_def['egress']

    ingress_rules = []
    if 'ingress' in sg_def:
        ingress_rules = sg_def['ingress']

    for rule in egress_rules:
        client.authorize_security_group_egress(GroupId=group_id, **rule)

    for rule in ingress_rules:
        client.authorize_security_group_ingress(GroupId=group_id, **rule)

    return group_id
