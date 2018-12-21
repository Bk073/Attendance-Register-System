from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import exceptions


# class GroupSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = Group
#         fields = ('name',)


class UserSerializers(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)

    class Meta:
        model = User
<<<<<<< Updated upstream
        fields = ('username', 'password','first_name', 'last_name','address','contact', 'email', 'date_of_birth', 'branch', 'groups')
=======
        fields = ('username' ,'password' ,'first_name', 'last_name','address','contact', 'email', 'date_of_birth', 'branch', 'groups')
>>>>>>> Stashed changes

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        user = User.objects.create(**validated_data)
        for group_data in groups_data:
            # Group.objects.create(user=user, **group_data)
            user.groups.add(group_data)
        return user

    
# class UserSerializers(serializers.ModelSerializer):
#     def create(self, validated_data):
#         user = User.objects.create(**validated_data)
#         group = Group.objects.get(name='Staff')
#         #group.user_set.set(self.object)
#         group.user_set.set(user)
#         user.save()
#         return user
#     class Meta:
#         model = User
#         fields = (
#             'password',
#             'first_name',
#             'last_name',
#             'email',
#             'groups',
#         )

    # def create(self, validated_data):
    #     groups_data = validated_data.pop('groups')
    #     album = Album.objects.create(**validated_data)
    #     for track_data in tracks_data:
    #         Track.objects.create(album=album, **track_data)
    #     return album
        
#handle group when saving
#add user to group

class UserLoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

<<<<<<< Updated upstream
        if username and password :
=======
        if email and password :
>>>>>>> Stashed changes
            user = authenticate(username=username, password=password)
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


