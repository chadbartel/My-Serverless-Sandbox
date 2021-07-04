#!/usr/bin/env python

"""Python class to search for EC2 instances by criteria."""
# Import libraries
import re
import logging
from copy import copy
from classes import Criteria
from classes import EC2

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Hunter:
    
    def __init__(self, criteria:Criteria):
        self.criteria = criteria

    # TODO: Get list of all active EC2 instances
    def find_all_instances(self):
        self._instances = []
        return None
    
    # TODO: Identify any active EC2 instances with tags that violate criteria
    def violating_instances(self):
        pass
    
    # TODO: Terminate all EC2 instances with invalid tagging
