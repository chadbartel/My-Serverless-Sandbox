#!/usr/bin/env python

"""Wrapper for AWS EC2Client client."""
# Import libraries
import logging
from copy import copy
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
            response = client.describe_instances(
                Filters=filters,
                NextToken=response['NextToken']
            )

        # Get instances from the response or return an empty list
        try:
            for r in response['Reservations']:
                for i in r['Instances']:
                    instances.append(i['InstanceId'])
        except IndexError as e:
            logger.error(
                f'No running instances found: {e}'
            )
            return instances

        # Check if there are any other instances
        if 'NextToken' not in response:
            return instances
        else:
            return instances + self.list_instances(
                client=client, 
                response=response, 
                filters=filters
            )
    
    def get_instance_tags(self, instance_ids:list, client:Session.client=None, response:dict=None):
        """Generate list of all tags for a given list of instances."""
        # Set initial empty list of tags
        tags = []
    
        # Check if passed an empty list of instance ids
        if not instance_ids:
            logger.error(
                f'No instance ids found in list, returning empty tags'
            )
            return tags
        else:
            instance_ids = copy(instance_ids)

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

        while instance_ids:
            # Get current instance from list
            i = instance_ids.pop()

            # Create filter dictionary
            filters = [
                {
                    'Name': 'resource-type',
                    'Values': ['instance'],
                    'Name': 'resource-id',
                    'Values': [i]
                }
            ]
            
            # Check if we already have a response
            if not response:
                response = client.describe_tags(
                    Filters=filters
                )
            elif 'NextToken' in response:
                response = client.describe_tags(
                    Filters=filters,
                    NextToken=response['NextToken']
                )
            else:
                response = copy(response)

            # Get tags from the response or return an empty list
            try:
                tags.append(
                    {i:[
                        {tag['Key']:tag['Value']} for tag in response['Tags']
                    ]}
                )
            except IndexError as e:
                logger.error(
                    f'No running instances found: {e}'
                )
                return tags

        # Check if there are any other tags
        if 'NextToken' not in response:
            return tags
        else:
            return tags.update(
                self.list_tags(
                    instance_ids=instance_ids,
                    client=client,
                    response=response
                )
            )