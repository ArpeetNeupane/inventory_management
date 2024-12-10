from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from accounts.serializers import LoginSerializers

from inventory_management.utils import api_response

class LoginView(APIView):
    def post(self, request):

        try:
            #creating a new instance of serializer based on user login details
            serializer_instance = LoginSerializers(data=request.data)

            #checking if serializer_instance is valid according to serializer's defined validation rules
            if serializer_instance.is_valid():
                user = serializer_instance.validated_data['user']

                try:
                    #creating access and refresh token for the user
                    access_token = AccessToken.for_user(user)
                    refresh_token = RefreshToken.for_user(user)

                    #return Response(response_data, status=response_data['status_code'])
                    return api_response(
                        is_success=True,
                        status_code=status.HTTP_200_OK,
                        result= {
                            "access_token": str(access_token),
                            "refresh_token": str(refresh_token)
                        }
                    )

                except Exception as token_error:
                    return api_response(
                        is_success=False,
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        error_message=f'Token generation failed: {str(token_error)}'
                    )
            
            #if serializer validation fails
            return api_response(
                is_success=False,
                status_code=status.HTTP_400_BAD_REQUEST,
                error_message=serializer_instance.errors
            )
        
        except AuthenticationFailed:
            #handling authentication failures
            return api_response(
                is_success=False,
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_message='Authentication failed'
            )
        
        except Exception as e:
            #catching any unexpected errors
            return api_response(
                is_success=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_message=f'An unexpected error occurred: {str(e)}'
            )