# Import libraries
import datetime
import logging

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))

    # TODO: Load criteria

    # TODO: Get instances w/invalid criteria
 
    # TODO: Terminate instances w/invalid criteria
