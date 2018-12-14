from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions


class UserSerializers(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        

class UserLoginSerializers(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if email and password :
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactive"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide email and password both"
            raise exception.ValidateError(msg)
        
        return data


