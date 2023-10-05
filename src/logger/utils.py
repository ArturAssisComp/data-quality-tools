import logging
from typing import Literal


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

def get_custom_logger_name(name:str, len_minus_depth=1, start:Literal['last', 'first'] = 'first'):
    """Returns the last or first `depth` components of the module name, letting out len_minus_depth."""
    parts = name.split('.')
    match start:
        case 'first':
            return '.'.join(parts[:(len(parts) - len_minus_depth)])
        case 'last':
            return '.'.join(parts[len_minus_depth:])

