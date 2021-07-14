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

    # TODO: Identify instance tags that violate criteria
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

        if not i["Tags"]:
            instances.append(i["InstanceId"])
            if not instance_tags:
                return instances
            else:
                return instances + self.get_invalid_instances(
                    instance_tags=instance_tags
                )
        
        tag_keys = list(
            set().union(*(tag.keys() for tag in i["Tags"]))
        )
        tag_values = list(
            set().union(*(tag.values() for tag in i["Tags"]))
        )
        criteria_keys = list(
            set().union((c['key'] for c in self.criteria))
        )
        
        if set(tag_keys) != set(criteria_keys):
            instances.append(i["InstanceId"])
        else:
            matches = []
            for c in self.criteria:
                pat = re.compile(self.criteria[c['value']])
                matches = matches + list(filter(pat.match, tag_values))
            if len(matches) != len(criteria_keys):
                instances.append(i["InstanceId"])

        if not instance_tags:
            return instances
        else:
            return instances + self.get_invalid_instances(
                instance_tags=instance_tags
            )
    
    # TODO: Terminate instance by id
    def terminate_instance(self, instance_id:str):
        pass
    
    # TODO: Terminate instances that violate criteria
    def terminate_invalid_instances(self, instances:list):
        pass