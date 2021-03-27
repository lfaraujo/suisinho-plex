import yaml
import logging
import logging.config

with open("logger/config/log_config.yml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_logger():
    return logging.getLogger('main_app')
