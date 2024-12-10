from rest_framework.response import Response
from rest_framework import status

def api_response(
        is_success=False,
        error_message=None,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        result = None,
    ):

    return Response(
        {
            "IsSuccess": is_success,
            "ErrorMessage": error_message,
            "StatusCode": status_code,
            "Result": result
        }
    )