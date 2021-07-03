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
    def get_client(cls, *args, **kwargs):
        args = [] if not args else args
        kwargs = {} if not kwargs else kwargs
        if 'region' not in kwargs:
            kwargs['region'] = 'us-west-2'
        return boto3.client('ec2', *args, **kwargs)

    @classmethod
    def get_resource(cls, *args, **kwargs):
        args = [] if not args else args
        kwargs = {} if not kwargs else kwargs
        if 'region' not in kwargs:
            kwargs['region'] = 'us-west-2'
        return boto3.resource('ec2', *args, **kwargs)