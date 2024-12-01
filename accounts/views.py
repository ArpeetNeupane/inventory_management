from rest_framework.views import APIView
from .serializers import LoginSerializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

class LoginView(APIView):
    def post(self, request):
        #default response data
        response_data = {
            'status_code': 500,
            'is_success': False,
            'result': {},
            'error_message': ''
        }

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

                    # Successful token generation
                    response_data['status_code'] = status.HTTP_200_OK
                    response_data['is_success'] = True
                    response_data['result'] = {
                        'access_token': str(access_token),
                        'refresh_token': str(refresh_token)
                    }
                    return Response(response_data, status=response_data['status_code'])

                except Exception as token_error:
                    response_data['error_message'] = f'Token generation failed: {str(token_error)}'
                    return Response(response_data, status=response_data['status_code'])
            
            #if serializer validation fails
            response_data['status_code'] = status.HTTP_400_BAD_REQUEST
            response_data['error_message'] = serializer_instance.errors
            return Response(response_data, status=response_data['status_code'])
        
        except AuthenticationFailed:
            # Handle authentication failures
            response_data['status_code'] = status.HTTP_401_UNAUTHORIZED
            response_data['error_message'] = 'Authentication failed'
            return Response(response_data, status=response_data['status_code'])
        
        except Exception as e:
            # Catch any unexpected errors
            response_data['error_message'] = f'An unexpected error occurred: {str(e)}'
            return Response(response_data, status=response_data['status_code'])