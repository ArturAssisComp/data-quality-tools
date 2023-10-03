import logging


def log_header(logger:logging.Logger, message:str):
    message_formatted = f'| - - - {message} - - - |'
    separate_bar = ''.join(['+', '=' * (len(message_formatted) - 2), '+'])

    logger.info(separate_bar)
    logger.info(message_formatted)

def log_footer(logger:logging.Logger, message:str):
    message_formatted = f'| - - - {message} - - - |'
    separate_bar = ''.join(['+', '=' * (len(message_formatted) - 2), '+'])

    logger.info(message_formatted)
    logger.info(separate_bar)
