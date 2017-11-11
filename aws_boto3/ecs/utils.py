import logging

from aws_decorators import boto_client
from botocore.exceptions import ClientError


@boto_client('ecs')
def ensure_instance(container_def, region=None, client=None):
    return client.register_container_instance(**container_def)


@boto_client('ecs')
def ensure_register_task(task, region=None, client=None):
    return client.register_task_definition(**task['task_definition'])


@boto_client('ecs')
def ensure_service(service, region=None, client=None):
    task_response = None
    if 'task' in service:
        task = service['task']
        task['cluster_arn'] = service['service_definition']['cluster']
        task['service_name'] = service['service_definition']['serviceName']
        task_response = ensure_register_task(task, region)
        task_arn = task_response['taskDefinition']['taskDefinitionArn']
        service['service_definition']['taskDefinition'] = task_arn

    response = None
    create_failed = False

    try:
        response = client.create_service(**service['service_definition'])
    except ClientError:
        logging.warn("Failed to create service. Attempting to update...")
        create_failed = True

    if create_failed:
        service_def = service['service_definition']
        wanted_keys = ['cluster', 'desiredCount', 'taskDefinition', 'deploymentConfiguration']
        update_service_def = dict((k, service_def[k]) for k in wanted_keys if k in service_def)
        update_service_def['service'] = service_def['serviceName']
        response = client.update_service(**update_service_def)

    if 'task' in service:
        response['task'] = task_response

    return response


@boto_client('ecs')
def ensure_cluster(cluster_def, region=None, client=None):
    response = client.create_cluster(**cluster_def)
    return response['cluster']['clusterArn']
