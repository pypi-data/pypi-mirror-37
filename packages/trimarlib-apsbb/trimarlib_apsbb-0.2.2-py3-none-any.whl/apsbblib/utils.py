import json
import logging
import logging.config


def setup_logging(path='logging.json',
                  level=logging.INFO):
    try:
        with open(path, 'r') as fd:
            config = json.load(fd)
        logging.config.dictConfig(config)
        return
    except FileNotFoundError:
        pass
    fmt = '%(asctime)s %(name)s:%(funcName)s [%(filename)s:%(lineno)d] <%(levelname)s>: %(message)s'
    logging.basicConfig(level=level, format=fmt)
    return
