#!/usr/bin/env python

"""Python class to search for EC2 instances by criteria."""
# Import libraries
import re
import boto3
import logging
from copy import copy
from classes.criteria import Criteria
from classes.ec2 import EC2

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Hunter:

    def __init__(self, criteria:Criteria, **client_kwargs):
        self._base_filters = [
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            },
            {
                'Name': 'resource-type',
                'Values': ['instance']
            }
        ]
        self._client = EC2.get_client(**client_kwargs)

    # TODO: Get list of all active EC2 instances
    def find_all_instances(self):
        pass
    
    # TODO: Identify any active EC2 instances with tags that violate criteria
    def violating_instances(self):
        pass
    
    # TODO: Terminate all EC2 instances with invalid tagging
