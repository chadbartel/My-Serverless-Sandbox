#!/usr/bin/env python

"""Wrapper for AWS EC2 client."""
# Import libraries
import boto3
import logging

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class EC2:

    @classmethod
    def get_session(cls, *args, **kwargs):
        args = [] if not args else args
        kwargs = {} if not kwargs else kwargs
        if 'region' not in kwargs:
            kwargs['region'] = 'us-west-2'
        return boto3.session(*args, **kwargs)

    @classmethod
    def get_client(cls, session:boto3.Session=None, *args, **kwargs):
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
        self._client = self.get_client(self._session, 'ec2', *args, **kwargs)
    
    def list_instances(self, filters:dict=None):
        pass