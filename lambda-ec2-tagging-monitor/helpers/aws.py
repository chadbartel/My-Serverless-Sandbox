"""API service AWS functions."""

# Import libraries
import logging
import boto3
from boto3.exceptions import UnauthorizeOperation

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def describe_ec2_tags(**kwargs):
    ec2_client = boto3.client('ec2')
    
    try:
        _ = ec2_client.describe_tags(DryRun=True)
    except UnauthorizeOperation as e:
        logger.error(
            f'Insufficient permissions to perform this action: {e}'
        )
        raise(e)
    
    try:
        response = ec2_client.describe_tags(**kwargs)
    except Exception as e:
        logger.error(
            f'Received invalid `kwargs`: {e}'
        )
        raise(e)
    else:
        return response