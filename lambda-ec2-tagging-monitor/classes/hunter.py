#!/usr/bin/env python

"""Python class to search for EC2 instances by criteria."""
# Import libraries
import re
import logging
from copy import copy

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Hunter:

    # TODO: Get list of all active EC2 instances
    # TODO: Identify any active EC2 instances with tags that violate criteria
    # TODO: Terminate all EC2 instances with invalid tagging
    
    pass