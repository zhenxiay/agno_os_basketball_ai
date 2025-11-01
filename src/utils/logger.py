'''
Logger module provides some features to help to log and monitor the code execution.
'''
import logging

def get_logger():
    '''
    Logger function used by other modules to log messages.
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # Add a StreamHandler to output logs to the console
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.info("Logger initialized")

    return logger
