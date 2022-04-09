"""Basic implementation of a logger, change the level in the configuration file if desired"""
import logging

logging.basicConfig(
    format='%(asctime)s-%(levelname)s-%(module)s.py-%(funcName)s -> %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

log = logging.getLogger(__name__)
