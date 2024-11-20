from rest_framework.views import APIView
from .serializers import LoginSerializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.response import Response #will take in any py data or already serialized data and will render it out as json
from rest_framework import status

class LoginView(APIView):
    def post(self, request):
        #creating a new instance of serializer based on user login details
        serializer_instance = LoginSerializers(data=request.data)

        #checking if serializer_instance is valid according to serializer's defined validation rules
        if serializer_instance.is_valid():
            user = serializer_instance.validated_data['user'] #validated_data contains data after is_valid is true, and user is key of dict 
                                                              #containing user data, so variable user contains value corresponding to key user

            #creating access and refresh token for the user
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)

            return Response({
                'access_token': str(access_token),
                'refresh_token':  str(refresh_token), #also blacklist tokens
            }, status=status.HTTP_200_OK)
        
        return Response(serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)