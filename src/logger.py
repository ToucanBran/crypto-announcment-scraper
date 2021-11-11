import logging, os, pathlib
from load_config import *

# loads local configuration
config = load_config('config.yml')

log = logging

pathlib.Path('./logs').mkdir(exist_ok=True)
log_level = os.environ.get("LOG_LEVEL") if os.environ.get("LOG_LEVEL") is not None else 'INFO'
log_file = './logs/bot.log'

log.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                handlers=[logging.FileHandler(log_file), logging.StreamHandler()])
logger = logging.getLogger(__name__)
level = logging.getLevelName(log_level)
logger.setLevel(level)
