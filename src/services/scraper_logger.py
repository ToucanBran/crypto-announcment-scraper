from io import TextIOWrapper
import logging, os, pathlib,yaml
from helpers import is_none_or_whitespace

def read_config(f: TextIOWrapper):
    try:
        configs = yaml.safe_load(f.read())
    except Exception as e:
        print(e)
        logging.basicConfig(level=logging.INFO)

def setup_logger():
    path = os.path.join(os.path.dirname(__file__), "log_configs.yaml")
    with open(path, 'r') as f:
        read_config(f)

    return get_logger("scraper")

def get_logger(name):
    logger = logging.getLogger(name)
    level = os.environ.get("LOGLEVEL", "INFO") if not is_none_or_whitespace(os.environ.get("LOGLEVEL", "INFO")) else "INFO"
    logger.setLevel(level)
    return logger
