import base64
import logging


def setup_logger(log_file):
    # Create a logger and set its log level
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set its log level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler and set its log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_email_body(payload):
    if 'parts' in payload:
        # If email has parts, check for 'text/plain' or 'text/html' parts
        data = None
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' or \
                    part['mimeType'] == 'text/html':
                data = part['body'].get('data')
            if data:
                return base64.urlsafe_b64decode(data).decode()

    # If no parts found, return an empty string
    return ""