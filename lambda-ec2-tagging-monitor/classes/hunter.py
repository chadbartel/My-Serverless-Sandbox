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
    def criteria(self) -> list:
        return copy(self._criteria)
    
    @criteria.setter
    def criteria(self, value:list):
        self._criteria = value
    
    @property
    def invalid_instances(self) -> list:
        return copy(self._invalid_instances)
    
    @invalid_instances.setter
    def invalid_instances(self, value:list):
        self._invalid_instances = value

    def set_invalid_instances(self, *args, **kwargs):
        self._invalid_instances = self.get_invalid_instances(*args, **kwargs)
    
    def __init__(self, criteria:list, instance_tags:list):
        if not criteria:
            logger.error(
                f'Empty criteria - exiting'
            )
            raise sys.exit()
        elif not instance_tags:
            logger.error(
                f'Empty instance tags - exiting'
            )
            raise sys.exit()
        else:
            self._criteria = criteria
            self._instance_tags = instance_tags
        self._invalid_instances = []

    # Identify instance tags that violate criteria
    def get_invalid_instances(self, instance_tags:list=None):
        instance_tags = self.instance_tags if not instance_tags else instance_tags
        instances = []
        if not instance_tags:
            return instances

        # There are three cases we need to consider:
        #   1. There are no tags
        #   2. Not all of the tag keys are present
        #   3. All tag keys are present, values aren't valid
        i = instance_tags.pop()

        # Instance has no tags whatsoever
        if not i["Tags"]:
            instances.append(i["InstanceId"])
            # No instance tags left to examine
            if not instance_tags:
                return instances
            # Recurse function with remaining instances
            else:
                return instances + self.get_invalid_instances(
                    instance_tags=instance_tags
                )
        
        # Get list of tag keys
        tag_keys = list(
            set().union(*(tag.keys() for tag in i["Tags"]))
        )
        # Get list of criteria keys
        criteria_keys = list(
            set().union((c['key'] for c in self.criteria))
        )
        
        # There are not enough tags on the instance
        if set(tag_keys) < set(criteria_keys):
            instances.append(i["InstanceId"])
        else:
            # Set empty match result variable
            matches = []
            # Go over all criteria
            for c in self.criteria:
                # Compile regex pattern
                pat = re.compile(c['value'])
                # Get EC2 tag we need to apply the regex pattern
                tag = list(
                    filter(lambda x: c['key'] in x, i["Tags"])
                )
                match = pat.match(tag[0][c['key']])
                # Append match to matches result variable
                if match.group(0):
                    matches.append(match.group(0))
            # Length of matched tags is equal to length of criteria
            if len(matches) != len(criteria_keys):
                instances.append(i["InstanceId"])

        # No instance tags left to examine
        if not instance_tags:
            return instances
        # Recurse function with remaining instances
        else:
            return instances + self.get_invalid_instances(
                instance_tags=instance_tags
            )
    
    # TODO: Terminate instance by id
    def terminate_instance(self, instance_id:str):
        pass
    
    # TODO: Terminate instances that violate criteria
    def terminate_invalid_instances(self, instance_ids:list):
        pass