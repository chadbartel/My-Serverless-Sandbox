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

BASE_FILTERS = [
    # {
    #     'Name': 'resource-type',
    #     'Values': ['instance']
    # },
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
response = ec2_client.describe_instances(
    Filters = BASE_FILTERS
)
print(json.dumps(response, indent=4, default=default))

