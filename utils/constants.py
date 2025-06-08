# Imports
import os
from dotenv import load_dotenv
import logging
import colorlog

# Load env
load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")

# Logger
import logging
import colorlog

log = colorlog.ColoredFormatter(
    "%(blue)s[%(asctime)s]%(reset)s - %(filename)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

handler = logging.StreamHandler()
handler.setFormatter(log)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

