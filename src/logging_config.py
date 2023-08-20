import logging


def configure_logging():
    logging.basicConfig(filename='log.txt', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

