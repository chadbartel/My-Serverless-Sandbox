#!/usr/bin/env python

"""Wrapper for AWS EC2Client client."""
# Import libraries
import logging
from copy import copy
from os import terminal_size
from boto3.session import Session

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


DEFAULT_FILTERS = [
    {
        'Name': 'instance-state-name',
        'Values': ['running']
    }
]

class EC2Client:

    @classmethod
    def get_session(cls, *args, **kwargs):
        args = [] if not args else args
        kwargs = {} if not kwargs else kwargs
        if 'region_name' not in kwargs.keys():
            kwargs['region_name'] = 'us-west-2'
        return Session(*args, **kwargs)

    @classmethod
    def get_client(cls, session:Session=None, *args, **kwargs):
        args = [] if not args else args
        kwargs = {} if not kwargs else kwargs
        session = EC2Client.get_session() if not session else session
        return session.client('ec2', *args, **kwargs)
    
    @property
    def instances(self):
        return copy(self._instances)
    
    @instances.setter
    def instances(self, value):
        self._instances = value
    
    @instances.deleter
    def instances(self):
        self._instances = []

    def set_instances(self, *args, **kwargs):
        self._instances = self.get_instances(*args, **kwargs)

    @property
    def instance_tags(self):
        return copy(self._tags)
    
    @instance_tags.setter
    def instance_tags(self, value):
        self._tags = value
    
    @instance_tags.deleter
    def instance_tags(self):
        self._tags = []
    
    def set_instance_tags(self, *args, **kwargs):
        self._tags = self.get_instance_tags(*args, **kwargs)
    
    def __init__(self, region_name:str=None, profile_name:str=None, *args, **kwargs):
        self._region_name = 'us-west-2' if not region_name else region_name
        self._profile_name = profile_name
        args = [] if not args else args
        kwargs = {} if not kwargs else kwargs
        self._session = self.get_session(
            region_name=self._region_name,
            profile_name=self._profile_name
        )
        self._client = EC2Client.get_client(self._session, *args, **kwargs)
        self._instances = []
        self._tags = []
    
    def get_instances(self, client:Session.client=None, response:dict=None, filters:dict=None):
        """Generate list of all EC2 instances based on filters."""
        # Set initial empty list of instances
        instances = []

        # Check if we have a client to use
        if not client:
            try:
                client = self._client
            except Exception as e:
                logger.error(
                    f'Client property not found: {e}'
                )
                self._client = EC2Client.get_client()
                client = self._client
        
        # Set EC2 instance filters
        filters = DEFAULT_FILTERS if not filters else filters
        
        # Check if we already have a response
        if not response:
            response = client.describe_instances(
                Filters=filters
            )
        else:
            response = copy(response)

        # Get instances from the response or return an empty list
        try:
            for r in response['Reservations']:
                for i in r['Instances']:
                    instances.append({'InstanceId': i['InstanceId']})
        except IndexError as e:
            logger.error(
                f'No running instances found: {e}'
            )
            return instances

        # Check if there are any other instances
        if 'NextToken' in response:
            response = client.describe_instances(
                Filters=filters,
                NextToken=response['NextToken']
            )
            return instances + self.get_instances(
                client=client, 
                response=response, 
                filters=filters
            )
        else:
            return instances
    
    def get_instance_tags(self, instances:list, client:Session.client=None):
        """Generate list of all tags for a given list of instances."""
        # Set initial empty list of tags
        tags = []
    
        # Check if passed an empty list of instance ids
        instance_ids = copy(instances)

        # Check if we have a client to use
        if not client:
            try:
                client = self._client
            except Exception as e:
                logger.error(
                    f'Client property not found: {e}'
                )
                self._client = EC2Client.get_client()
                client = self._client

        # Pop an instance from the list
        if instance_ids:
            i = instance_ids.pop()
        else:
            return tags

        # Create filter dictionary
        filters = [
            {
                'Name': 'resource-type',
                'Values': ['instance'],
                'Name': 'resource-id',
                'Values': [i['InstanceId']]
            }
        ]
        
        # Check if we already have a response, get one if not
        response = client.describe_tags(Filters=filters)

        # Get tags from the response or return an empty list
        tags.append(
            {
                'InstanceId': i['InstanceId'],
                'Tags': [
                    {
                        tag['Key']: tag['Value']
                    } for tag in response['Tags']
                ]
            }
        )

        # Call method if instances still in list
        if instance_ids:
            return tags + self.get_instance_tags(
                instances=instance_ids,
                client=client
            )
        return tags
    
    def terminate_instances(self, instance_ids:list, client:Session.client=None):
        # Set empty response variable
        responses = []
        
        # Check if we have a client to use
        if not client:
            try:
                client = self._client
            except Exception as e:
                logger.error(
                    f'Client property not found: {e}'
                )
                self._client = EC2Client.get_client()
                client = self._client
        
        # Copy list of instance ids
        instance_ids = copy(instance_ids)

        # Empty list was passed
        if not instance_ids:
            logger.info(
                'No instances found in list'
            )
            return responses
        # Only one element in list
        elif len(instance_ids) == 1:
            responses.append(
                client.terminate_instances(
                    InstanceIds=instance_ids
                )
            )
            return responses
        # At least two instance id elements in list
        else:
            i = instance_ids.pop()
            try:
                responses.append(
                    client.terminate_instances(
                        InstanceIds=instance_ids
                    )
                )
            except Exception as e:
                logger.error(
                    f'Unable to locate EC2 instance(s) by id \'{i}\': {e}'
                )
            return responses + self.terminate_instances(
                instance_ids=instance_ids,
                client=client
            )