#!/usr/bin/env python

# Import libraries
import sys
import json
import logging

sys.path.append('.')
from helpers import default
from classes import EC2Client


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

ec2 = EC2Client(profile_name=AWS_PROFILE)

running_instances = ec2.list_instances()
instance_tags = ec2.list_tags(instance_ids=running_instances)

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