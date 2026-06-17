# Day 68 - Error Finding Quiz

import logging

# Bug 1 - basicConfig after logging call has no effect
logging.warning("This appears before basicConfig")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# Bug 2 - handler added multiple times in a function
def get_logger(name):
    log = logging.getLogger(name)
    handler = logging.StreamHandler()
    log.addHandler(handler)    # Bug 2 - called repeatedly adds duplicate handlers
    return log

# Bug 3 - incorrect level comparison
def process(value):
    if value < 0:
        logger.log("ERROR", "Negative value")  # Bug 3 - should be logging.ERROR not string
    return abs(value)

process(-5)
process(10)