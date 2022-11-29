from rest_framework.views import exception_handler

from django.db import DataError
from rest_framework.response import Response
from rest_framework import status
from redis.exceptions import RedisError

import logging
logger = logging.getLogger("django")

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        view = context["view"]
        if isinstance(exc, DataError):
            logger.error('[%s] %s'%(view, exc))
            response = Response({"errmsg": "Internal Server Error"}, status = status.HTTP_507_INSUFFICIENT_STORAGE)
        elif isinstance(exc, RedisError):
            logger.error('redis operation error! [%s] %s'%(view, exc))
            response = Response({"errmsg": "Internal Cache Error"}, status = status.HTTP_507_INSUFFICIENT_STORAGE)
    return response
