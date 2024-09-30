from rest_framework.views import APIView
from .serializers import LoginSerializers
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):
    def post(self, request):
        #creating a new instance of serializer based on user login details
        serializer_instance = LoginSerializers(data=request.data)

        #checking if serializer_instance is valid
        if serializer_instance.is_valid():
            user = serializer_instance.validated_data['user']
            access_token = AccessToken.for_user(user)
            return Response({'token': str(access_token)}, status=status.HTTP_200_OK)
        
        return Response(serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)
        