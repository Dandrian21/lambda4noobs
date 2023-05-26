import json
import logging    

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # You can set this to be DEBUG, INFO, ERROR as needed

def log_format(func):
    def wrapper(*args, **kwargs):
        formatter = logging.Formatter('[%(levelname)s]\t%(asctime)s\t%(request_id)s\tPID:%(taskId)s  STATE:%(state)s  MESSAGE:%(message)s','%Y-%m-%dT%H:%M:%S')
        for handler in logger.handlers:
            logger.removeHandler(handler)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.info = add_extra(logger.info)  # Override logger.info with the decorated version
        func(*args, **kwargs)
    return wrapper

def add_extra(logger_info):
    def wrapper(msg, *args, **kwargs):
        extra = kwargs.get('extra', {})
        request_id = extra.get('request_id')
        taskId = 1222333
        state = "RUNNING"
        updated_extra = {'request_id': request_id, 'taskId': taskId, 'state': state}
        updated_extra.update(extra)  # Merge existing extra with updated_extra
        kwargs['extra'] = updated_extra
        return logger_info(msg, *args, **kwargs)
    return wrapper

@log_format
def lambda_handler(event, context):
    request_id = context.aws_request_id

    logger.info('This is an info log message')
    logger.info('hi')
    logger.error('danger danger')
