#!/usr/bin/env python

# Import libraries
import sys
import datetime
import logging

from classes import EC2
from classes import Criteria
from classes import Hunter

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
    
    # Get list of EC2 instances
    ec2 = EC2()
    instances = ec2.list_instances()
    if not instances:
        logger.error(
            'No running instances found'
        )
        sys.exit()

    # Load instance tag criteria
    criteria = Criteria()

    # TODO: Get instances w/invalid criteria
    hunter = Hunter(criteria)

    # Loop over list of instances
    for i in instances:
        # Get list of instance tags
        tags = ec2.list_instance_tags()
        
        # Terminate instances without any tags
        if not tags:
            hunter.terminate_invalid_instances()
        
        # TODO: Terminate instances w/invalid criteria
        hunter.terminate_invalid_instances()