import logging

import six
import requests
from six.moves.urllib.parse import urlparse

from structuredlogging.structured_log_formatter import StructuredLogFormatter


class RequestsLogFormatter(StructuredLogFormatter):
    """ Capture logs from requests library in a structured log """
    def format(self, record):
        if isinstance(record.msg, requests.Response):
            response = record.msg
            request = response.request
            url = urlparse(request.url)
            http_version = "HTTP/1.0" if response.raw.version == 10 else "HTTP/1.1"
            log_args = {
                "proto": url.scheme,
                "durationInMs": response.elapsed.total_seconds()*1000,
                "endpoint": request.url,
                "endpointHostName": url.netloc,
                "endpointPath": url.path,
                "httpMethod": request.method,
                "httpStatusCode": response.status_code,
                "httpVersion": http_version
            }
            if isinstance(record.args, dict):
                record.args.update(log_args)
            else:
                record.args = log_args
            record.msg = "{proto}://{endpointHostName} " \
                "\'{httpMethod} {endpointPath} {httpVersion}\' " \
                "{httpStatusCode}"
            setattr(record, "type", "request")

        if record.msg == "%s://%s:%s \"%s %s %s\" %s %s":
            proto, host, port, method, path, http_version, \
                status_code, _ = record.args
            record.msg = "{proto}://{endpointHostName} " \
                "\'{httpMethod} {endpointPath} {httpVersion}\' " \
                "{httpStatusCode}"
            record.args = {
                "proto": proto,
                "endpoint": "{}://{}:{}{}".format(proto, host, port, path),
                "endpointHostName": "{}:{}".format(host, port),
                "endpointPath": path,
                "httpMethod": method,
                "httpStatusCode": status_code,
                "httpVersion": http_version
            }

        return super(RequestsLogFormatter, self).format(record)



""" Log a http request/response

This is a convenience method monkey patched to a logging.Logger for
logging a request/response pair with associated timing information,
presumably from a response object provided by the requests library.
"""
def log_http_request(self, http_response, operationType, level=None,
                     additionalCorrelationIds=None, correlationId=None,
                     deploymentConfiguration=None, endTime=None, flagged=None,
                     flaggedDescription=None, messagename=None,
                     messageStats_Avg=None, messageStats_Count=None,
                     messageStats_ErrorCount=None, messageStats_Max=None,
                     messageStats_P50=None, messageStats_P90=None,
                     messageStats_P99=None, 
                     persistentConnection=None, product=None, retryCount=None,
                     secondaryCorrelationId=None, sourceCloudPlatform=None,
                     startTime=None):

    if not isinstance(http_response, requests.Response):
        raise TypeError("http_response needs to be a requests.Response")

    if level is None:
        if http_response.status_code >= 300:
            level = logging.ERROR
        else:
            level = logging.INFO

    args = dict(additionalCorrelationIds=additionalCorrelationIds,
                correlationId=correlationId,
                deploymentConfiguration=deploymentConfiguration,
                endTime=endTime,
                flagged=flagged,
                flaggedDescription=flaggedDescription,
                messagename=messagename,
                messageStats_Avg=messageStats_Avg,
                messageStats_Count=messageStats_Count,
                messageStats_ErrorCount=messageStats_ErrorCount,
                messageStats_Max=messageStats_Max,
                messageStats_P50=messageStats_P50,
                messageStats_P90=messageStats_P90,
                messageStats_P99=messageStats_P99,
                operationType=operationType,
                persistentConnection=persistentConnection,
                product=product,
                secondaryCorrelationId=secondaryCorrelationId,
                sourceCloudPlatform=sourceCloudPlatform,
                startTime=startTime)
    args = {k:v for k, v in six.iteritems(args) if v is not None}

    self.log(level, http_response, args)


def log_request(self, level, operationType, additionalCorrelationIds=None, correlationId=None,
                deploymentConfiguration=None, durationInMs=None, endpoint=None,
                endpointHostName=None, endpointPath=None, endTime=None,
                exceptionClass=None, exceptionDetail=None,
                exceptionMessage=None, flagged=None, flaggedDescription=None,
                httpMethod=None, httpStatusCode=None, messageName=None,
                messageStats_Avg=None, messageStats_Count=None,
                messageStats_ErrorCount=None, messageStats_Max=None,
                messageStats_P50=None, messageStats_P90=None,
                messageStats_P99=None, persistentConnection=None, product=None,
                retryCount=None, secondaryCorrelationId=None, sourceCloudPlatform=None,
                startTime=None):
    args = dict(additionalCorrelationIds=additionalCorrelationIds,
                correlationId=correlationId,
                deploymentConfiguration=deploymentConfiguration,
                durationInMs=durationInMs,
                endpoint=endpoint,
                endpointHostName=endpointHostName,
                endpointPath=endpointPath,
                endTime=endTime,
                exceptionClass=exceptionClass,
                exceptionDetail=exceptionDetail,
                exceptionMessage=exceptionMessage,
                flagged=flagged,
                flaggedDescription=flaggedDescription,
                httpMethod=httpMethod,
                httpStatusCode=httpStatusCode,
                messageName=messageName,
                messageStats_Avg=messageStats_Avg,
                messageStats_Count=messageStats_Count,
                messageStats_ErrorCount=messageStats_ErrorCount,
                messageStats_Max=messageStats_Max,
                messageStats_P50=messageStats_P50,
                messageStats_P90=messageStats_P90,
                messageStats_P99=messageStats_P99,
                operationType=operationType,
                persistentConnection=persistentConnection,
                product=product,
                retryCount=retryCount,
                secondaryCorrelationId=secondaryCorrelationId,
                sourceCloudPlatform=sourceCloudPlatform,
                startTime=startTime)
    args = {k:v for k, v in six.iteritems(args) if v is not None}

    self.log(level, {"@type": "request", "messageArguments": args})

logging.Logger.logHttpRequest = log_http_request
logging.Logger.logRequest = log_request
