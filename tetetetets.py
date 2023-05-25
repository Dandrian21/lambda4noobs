import json
import logging


class CustomLogger(logging.Logger):
    def info(self, msg, *args, **kwargs):
        extra = kwargs.get("extra", {})
        request_id = extra.get("request_id", "")
        taskId = extra.get("taskId", "")
        state = extra.get("state", "")
        extra.update({"request_id": request_id, "taskId": taskId, "state": state})
        super().info(msg, *args, extra=extra)


logger = CustomLogger()
logger.setLevel(logging.INFO)


def log_format(func):
    def wrapper(*args, **kwargs):
        formatter = logging.Formatter(
            "[%(levelname)s]\t%(asctime)s\t%(request_id)s\tPID:%(taskId)s  STATE:%(state)s  MESSAGE:%(message)s",
            "%Y-%m-%dT%H:%M:%S",
        )
        for handler in logger.handlers:
            logger.removeHandler(handler)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        func(*args, **kwargs)

    return wrapper


@log_format
def lambda_handler(event, context):
    request_id = context.aws_request_id

    # Include the request ID and custom inputs in logging calls
    # taskId = 1222333
    # state = "RUNNING"
    # extra = {"request_id": request_id, "taskId": taskId, "state": state}
    logger.info("This is an info log message")
    logger.info("hi")
    logger.error("danger danger")
