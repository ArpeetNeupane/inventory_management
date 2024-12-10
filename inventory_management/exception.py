from rest_framework.views import exception_handler, status
from inventory_management.utils import api_response
import logging

logger = logging.getLogger(__name__)
#retrieving a logger with the name of the current module. The __name__ variable holds the module's name (inventory_management.utils)

def custom_exception_handler(exc, context):
    #calling DRF's default exception handler
    response = exception_handler(exc, context)

    if response is not None:
        #here, we're modifying existing response object so we're reassigning response.data
        response.data = api_response(
            is_success=False,
            error_message=str(exc),
            status_code=response.status_code,
            result=response.data,
        ).data #converting the response obj to a dict by appending .data

    else: #already handled most exception types in views but using else for safety net
        #logging unhandled exceptions for debugging
        logger.error("Unhandled exception: %s", exc, exc_info=True) #exc_info=True --> including the exception traceback in the log message

        #fallback generic error response
        #here, we're creating a new response object in case of fallback so response = api_response() instead of response.data = api_response()
        response = api_response(
            result=None,
            is_success=False,
            error_message="An unexpected error occurred.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
