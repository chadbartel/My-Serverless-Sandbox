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

    def _get_client(self, *args, **kwargs):
        self._ec2_client = EC2.get_client(*args, **kwargs)

    def __init__(self, criteria:Criteria, *client_args, **client_kwargs):
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
        self._client = self._get_client(*client_args, **client_kwargs)

    # TODO: Get list of all active EC2 instances
    def find_all_instances(self):
        self._instances = []
    
    
    # TODO: Identify any active EC2 instances with tags that violate criteria
    def violating_instances(self):
        pass
    
    # TODO: Terminate all EC2 instances with invalid tagging
