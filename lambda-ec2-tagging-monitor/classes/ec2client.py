#!/usr/bin/env python

"""Wrapper for AWS EC2 client."""
# Import libraries
import boto3
import logging
from copy import copy

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class EC2Client:

    @classmethod
    def get_client(class, **kwargs):
        kwargs = {} if not kwargs else kwargs
        if 'region' not in kwargs:
            kwargs['region'] = 'us-west-2'
        return boto3.client('ec2', **kwargs)
