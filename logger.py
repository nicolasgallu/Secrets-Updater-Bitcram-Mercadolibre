import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s / %(module)s / %(levelname)s / %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S',
    stream=sys.stdout

)

logger = logging.getLogger()
