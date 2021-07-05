#!/usr/bin/env python

"""Python class to search for EC2 instances by criteria."""
# Import libraries
import re
import logging
from copy import copy
from classes import Criteria
from classes import EC2Client

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Hunter:
    
    def __init__(self, criteria:Criteria, ec2:EC2Client):
        self._criteria = criteria
        self._ec2 = ec2

    # TODO: Identify instance tags that violate criteria
    def violating_instances(self):
        pass
    
    # TODO: Terminate instance by id
    def terminate_instance(self, instance_id:str):
        pass