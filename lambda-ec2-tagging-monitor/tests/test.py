#!/usr/bin/env python

# Import libraries
import datetime
import json
import boto3
import logging


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


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def get_client(region_name='us-west-2', profile_name=None, *args, **kwargs):
    session = boto3.Session(
        region_name=region_name, 
        profile_name=profile_name
    )
    args = [] if not args else args
    kwargs = {} if not kwargs else kwargs
    return session.client('ec2', *args, **kwargs)


ec2_client = get_client(profile_name=AWS_PROFILE)
instance_response = ec2_client.describe_instances(
    Filters = INSTANCE_FILTERS
)
tag_response = ec2_client.describe_tags(
    Filters = TAG_FILTERS
)
print('Running instances:')
print(json.dumps(instance_response, indent=4, default=default))
print()
print('Instance tags:')
print(json.dumps(tag_response, indent=4, default=default))