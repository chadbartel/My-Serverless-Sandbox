#!/usr/bin/env python

# Import libraries
import sys
import json
import boto3
import logging

sys.path.append(".")
from helpers.helpers import default
from classes.ec2 import EC2


# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


AWS_PROFILE = 'sso_poweruser'

TAG_FILTERS = [
    {
        'Name': 'resource-type',
        'Values': ['instance']
    }
]
INSTANCE_FILTERS = [
    {
        'Name': 'instance-state-name',
        'Values': ['running']
    }
]


def get_client(region_name='us-west-2', profile_name=None, *args, **kwargs):
    session = boto3.Session(
        region_name=region_name, 
        profile_name=profile_name
    )
    args = [] if not args else args
    kwargs = {} if not kwargs else kwargs
    return session.client('ec2', *args, **kwargs)


ec2_client = get_client(profile_name=AWS_PROFILE)
instance_response = ec2_client.describe_instances(Filters=INSTANCE_FILTERS)
try:
    running_instances = [
        i['InstanceId'] for i in instance_response['Reservations'][0]['Instances']
    ]
except IndexError as e:
    running_instances = []
    print(
        f'No running instances found: {e}'
    )
tag_response = ec2_client.describe_tags(Filters=TAG_FILTERS)
instance_tags = [
    tag for tag in tag_response['Tags'] if tag['ResourceId'] in running_instances
]

print('Running instances:')
print(
    json.dumps(
        running_instances,
        indent=4,
        default=default
    )
)
print()
print('Instance tags:')
print(
    json.dumps(
        instance_tags,
        indent=4,
        default=default
    )
)