#!/usr/bin/env python

"""Python class to search for EC2 instances by criteria."""
# Import libraries
import sys
import re
import logging
from copy import copy

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Hunter:

    @property
    def instance_tags(self) -> list:
        return copy(self._instance_tags)
    
    @instance_tags.setter
    def instance_tags(self, value:list):
        self._instance_tags = value

    @property
    def criteria(self) -> dict:
        return copy(self._criteria)
    
    @criteria.setter
    def criteria(self, value:dict):
        self._criteria = value
    
    def __init__(self, criteria:dict, instance_tags:list):
        if not criteria or instance_tags:
            logger.error(
                f'Empty criteria and/or instance tags - exiting'
            )
            raise sys.exit()
        else:
            self._criteria = criteria
            self._instance_tags = instance_tags

    # TODO: Identify instance tags that violate criteria
    def get_invalid_instances(self, instance_tags:list=None):
        instance_tags = self.instance_tags if not instance_tags else instance_tags
        # for i in :
    
    # TODO: Terminate instance by id
    def terminate_instance(self, instance_id:str):
        pass
    
    # TODO: Terminate instances that violate criteria
    def terminate_invalid_instances(self, instances:list):
        pass