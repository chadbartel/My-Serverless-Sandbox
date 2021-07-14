#!/usr/bin/env python

# Import libraries
import os
import sys
import json
import logging
from copy import copy

# Update path
sys.path.insert(
    0, 
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 
            '..'
        )
    )
)
sys.path.append('.')
sys.path.append('..')
from helpers import default
from classes import EC2Client
from classes import Criteria
from classes import Hunter

# Start logger
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG, filename='tests/output.log', filemode='w')

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


def test(profile:str=AWS_PROFILE, filters:dict=TAG_FILTERS, test_data=False):
    criteria = Criteria()
    if not test_data:
        ec2 = EC2Client(profile_name=AWS_PROFILE)
        ec2.set_instances()
        ec2.set_instance_tags(instances=ec2.instances)


        print('Running instances:')
        print(
            json.dumps(
                ec2.instances,
                indent=4,
                default=default
            )
        )
        print()
        print('Instance tags:')
        print(
            json.dumps(
                ec2.instance_tags,
                indent=4,
                default=default
            )
        )
    
        hunter = Hunter(
            criteria=criteria.criteria['criteria'], 
            instance_tags=ec2.instance_tags
        )
        hunter.set_invalid_instances()
        print(hunter.invalid_instances)
    else:
        instances = []
        with open(r'tests/test_instances.json', 'r') as f:
            instance_response = json.loads(f.read())
        try:
            for r in instance_response['Reservations']:
                for i in r['Instances']:
                    instances.append({'InstanceId': i['InstanceId']})
        except IndexError as e:
            logger.error(
                f'No running instances found: {e}'
            )
        print('Running instances:')
        print(
            json.dumps(
                instances,
                indent=4,
                default=default
            )
        )
        print()
        tags = []
        instance_ids = copy(instances)
        with open(r'tests/test_instance_tags.json', 'r') as f:
            tags_response = json.loads(f.read())
        for i in instance_ids:
            tags.append(
                {
                    'InstanceId': i['InstanceId'],
                    'Tags': [
                        {
                            tag['Key']: tag['Value']
                        } for tag in tags_response['Tags']
                        if tag["ResourceId"] == i["InstanceId"]
                    ]
                }
            )
        print('Instance tags:')
        print(
            json.dumps(
                tags,
                indent=4,
                default=default
            )
        )
    
        hunter = Hunter(
            criteria=criteria.criteria['criteria'], 
            instance_tags=tags
        )
        hunter.set_invalid_instances()
        print(hunter.invalid_instances)


if __name__ == "__main__":
    profile = AWS_PROFILE
    filters = TAG_FILTERS
    test_data = True
    test(profile=profile, filters=filters, test_data=test_data)