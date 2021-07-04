#!/usr/bin/env python

"""Wrapper for AWS EC2 client."""
# Import libraries
import boto3
import logging

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


DEFAULT_FILTERS = [
    {
        'Name': 'instance-state-name',
        'Values': ['running']
    }
]

class EC2:

    @classmethod
    def get_session(cls, *args, **kwargs):
        args = [] if not args else args
        kwargs = {} if not kwargs else kwargs
        if 'region_name' not in kwargs.keys():
            kwargs['region_name'] = 'us-west-2'
        return boto3.session.Session(*args, **kwargs)

    @classmethod
    def get_client(cls, session:boto3.session.Session=None, *args, **kwargs):
        args = [] if not args else args
        kwargs = {} if not kwargs else kwargs
        session = cls.get_session() if not session else session
        return session.client('ec2', *args, **kwargs)
    
    def __init__(self, region_name:str=None, profile_name:str=None, *args, **kwargs):
        self._region_name = 'us-west-2' if not region_name else region_name
        self._profile_name = profile_name
        args = [] if not args else args
        kwargs = {} if not kwargs else kwargs
        self._session = self.get_session(
            region_name=self._region_name,
            profile_name=self._profile_name
        )
        self._client = self.get_client(self._session, *args, **kwargs)
    
    def list_instances(self, response=None, filters:dict=None):
        """Generate list of all EC2 instances based on filters."""
        # Set EC2 instance filters
        filters = DEFAULT_FILTERS if not filters else filters
        instances = []
        
        # Check if we already have a response
        if not response:
            response = self._client.describe_instances(
                Filters=filters
            )
        else:
            response = self._client.describe_instances(
                Filters=filters,
                NextToken=response['NextToken']
            )

        # Get instances from the response or return an empty list
        try:
            instances += [
                i['Instances'][0]['InstanceId'] 
                for i in response['Reservations']
            ]
        except IndexError as e:
            logger.error(
                f'No running instances found: {e}'
            )
            return instances

        # Check if there are any other instances
        if 'NextToken' not in response:
            return instances
        else:
            return instances + self.get_running_instances(response=response, filters=filters)
    
    def list_instance_tags(self, response=None, instance_id:str=None):
        """Generate list of all tags for a given instance id."""
        # Set initial empty list of tags
        tags = []

        # Check if there was no instance id provided
        if not instance_id:
            logger.error(
                f'Instance id not provided, returning empty list of tags'
            )
            return tags

        # Create filter dictionary
        filters = [
            {
                'Name': 'resource-type',
                'Values': ['instance'],
                'Name': 'resource-id',
                'Values': [instance_id]
            }
        ]
        
        
        # Check if we already have a response
        if not response:
            response = self._client.describe_tags(
                Filters=filters
            )
        else:
            response = self._client.describe_tags(
                Filters=filters,
                NextToken=response['NextToken']
            )

        # Get tags from the response or return an empty list
        try:
            tags += [
                {tag['Key']:tag['Value']} for tag in response['Tags']
            ]
        except IndexError as e:
            logger.error(
                f'No running instances found: {e}'
            )
            return tags

        # Check if there are any other tags
        if 'NextToken' not in response:
            return tags
        else:
            return tags + self.get_running_instances(response=response, filters=filters)