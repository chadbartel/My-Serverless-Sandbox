#!/usr/bin/env python

"""Python class to search for EC2 instances by criteria."""
# Import libraries
import re
import boto3
import logging
from copy import copy
from classes.criteria import Criteria
from classes.ec2client import EC2Client

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Hunter:

    def __init__(self, criteria:Criteria, **client_kwargs):
        self._client = EC2Client.get_client(**client_kwargs)

    # TODO: Get list of all active EC2 instances
    def find_all_instances(self):
        pass
    
    # TODO: Identify any active EC2 instances with tags that violate criteria
    def violating_instances(self):
        pass
    
    # TODO: Terminate all EC2 instances with invalid tagging

    @property
    def region(self):
        return copy(self._region)
    
    def __init__(self, region:str='us-west-2'):
        self._region = region
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
        pass


    def get_instances(self):
        pass
    
    def get_resource(self):
        ec2 = boto3.resource('ec2', region_name=self._region)
        return ec2