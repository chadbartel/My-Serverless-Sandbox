# Import libraries
import datetime
import logging

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# TODO: List all EC2 instance(s)
# TODO: Terminate EC2 instance(s) that don't meet tagging criteria


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
