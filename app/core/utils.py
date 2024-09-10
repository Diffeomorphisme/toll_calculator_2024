import logging


def get_logger():
    logger = logging.getLogger('Toll-fee-calculator-logger')
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%b-%d %H:%M:%S'
    )
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger
