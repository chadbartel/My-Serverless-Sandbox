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

    # Load instance tag criteria
    criteria = Criteria()

    # TODO: Get instances w/invalid criteria
    hunter = Hunter(criteria, ec2)

    # TODO: Terminate instances w/invalid criteria
    hunter.terminate_invalid_instances()