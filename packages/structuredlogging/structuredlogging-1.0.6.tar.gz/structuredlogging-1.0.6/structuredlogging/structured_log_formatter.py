import datetime
import json
import logging
import uuid

import six


def StructuredLog(*args, **kwargs):
    from warnings import warn
    warn("StructuredLog is renamed to StructuredLogFormatter",
         DeprecationWarning, 2)
    return StructuredLogFormatter(*args, **kwargs)


class StructuredLogFormatter(logging.Formatter):
    """ Capture general logs in a structured log """
    def format(self, record):
        super(StructuredLogFormatter, self).format(record)

        log_type = getattr(record, 'type', "log")
        structured = {
            "@type": log_type,
            "timestamp": datetime.datetime.fromtimestamp(record.created).isoformat(),
            "metadata": {k: getattr(record, k)
                         for k in ["filename", "funcName", "lineno", "module",
                                   "pathname", "process", "processName", "thread",
                                   "threadName"]},
            "level": record.levelname,
            "messageId": str(uuid.uuid4())
        }

        if isinstance(record.msg, dict):
            structured.update(record.msg)
        elif isinstance(record.msg, six.string_types):
            structured["messageTemplate"] = record.msg

            if isinstance(record.args, dict):
                structured["message"] = record.msg.format(**record.args)
                structured["messageArguments"] = record.args
            else:
                structured["message"] = record.message
        else:
            structured["message"] = record.msg

        if record.exc_info is not None:
            exc_type, exc_value, _ = record.exc_info
            exc_msg = str(exc_value)
            exc_type = exc_type.__name__
            exc_stack = super(StructuredLogFormatter, self).formatException(record.exc_info)
            structured.update(dict(
                exceptionMessage=exc_msg,
                exceptionType=exc_type,
                exceptionStackTrace=exc_stack
            ))


        return json.dumps(structured)
