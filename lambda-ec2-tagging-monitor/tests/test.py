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

ec2 = EC2(profile_name=AWS_PROFILE)

running_instances = ec2.list_instances()
tag_response = ec2._client.describe_tags(Filters=TAG_FILTERS)
instance_tags = ec2.list_instance_tags(instance_id=running_instances[0])

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