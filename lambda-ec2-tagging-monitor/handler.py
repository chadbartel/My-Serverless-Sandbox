#!/usr/bin/env python

# Import libraries
import sys
import datetime
import logging

from classes import EC2Client
from classes import Criteria
from classes import Hunter

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
    
    # Get EC2 client and list all running EC2 instances
    ec2 = EC2Client()

    # Load instance tag criteria
    criteria = Criteria()

    # TODO: Get instances w/invalid criteria
    hunter = Hunter(criteria, ec2)

    # TODO: Terminate instances w/invalid criteria
    hunter.terminate_invalid_instances()