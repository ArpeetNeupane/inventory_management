from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class LoginSerializers(serializers.Serializer):
    #fields for serializer
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True, write_only = True) #is a security measure to prevent the password from being exposed in responses.

    def validate(self, data):
        entered_username = data.get('username')
        entered_password = data.get('password')

        user_authenticate = authenticate(username = entered_username, password = entered_password)
        #authenticate function returns none if user not found

        #authenticating/ checking if user exists
        if user_authenticate is None:
            raise serializers.ValidationError("Invalid username or password.")
        
        #if user is found, is returning in a dictionary, returning in a dict -- managing maintainability
        data['user'] = user_authenticate
        return data


    