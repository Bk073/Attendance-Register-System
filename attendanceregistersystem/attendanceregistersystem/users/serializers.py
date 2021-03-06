from rest_framework import serializers
from .models import User, Branch
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from rest_framework import exceptions
from django.contrib.auth.hashers import make_password


class BranchSerializers(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ['branch_id', 'branch_name',]


class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('id','name', 'permissions',)
        extra_kwargs = {
            'permissions': {'write_only': True}
        }

    def create(self, validated_data):
        groups_data = validated_data.pop('permissions')
        group = Group.objects.create(**validated_data)
        for group_data in groups_data:
            # Group.objects.create(user=user, **group_data)
            group.permissions.add(group_data)
        return group


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id','name',)


class UserSerializers(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)
    # branch = BranchSerializers()
    # id = serializers.IntegerField(read_only = True)
    # username = serializers.CharField(max_length=250)
    # password = password = serializers.CharField(
    #     write_only=True,
    #     required=True,
    #     help_text='Leave empty if no change needed',
    #     style={'input_type': 'password', 'placeholder': 'Password'}
    # )
    # first_name = serializers.CharField(max_length=250)
    # last_name = serializers.CharField(max_length=250)
    # address = serializers.CharField(max_length=250)
    # contact = serializers.IntegerField()
    # email = serializers.EmailField()
    # date_of_birth = serializers.DateField()
    class Meta:
        model = User
        fields = ('id', 'username', 'password','first_name', 'last_name','address','contact', 'email', 'date_of_birth', 'gender','branch','groups',)
        # depth = 1

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        user = User.objects.create(**validated_data)
        user.password =make_password(validated_data.pop('password'))
        user.save()
        for group_data in groups_data:
            # Group.objects.create(user=user, **group_data)
            print(group_data)
            user.groups.add(group_data)
        return user
    
    def update(self, instance, validated_data):
        user = User.objects.get(pk=instance.id)
        # validated_data['password'] =make_password(validated_data.pop('password'))
        User.objects.filter(pk=instance.id)\
                            .update(**validated_data)
        # user.update(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    # group = GroupSerializer(many=True, partial=True)
    class Meta:
        model = User
        fields = ('groups',)
        # depth = 1
    # def update(self, instance, validated_data):
    #     id = validated_data.pop['id']
    #     user = User.objects.get(id=id)
    #     # validated_data['password'] =make_password(validated_data.pop('password'))
    #     User.objects.filter(pk=instance.id)\
    #                         .update(**validated_data)
    #     # user.update(**validated_data)
    #     return user


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    branch = BranchSerializers()
    class Meta:
        model = User
        fields = ('id', 'username', 'password','first_name', 'last_name','address','contact', 'email', 'date_of_birth', 'gender', 'branch','groups')
        

class UserSerializersDefault(serializers.Serializer):
    class Meta:
        model = User
        fields = ('username', 'password','first_name', 'last_name','address','contact', 'email', 'date_of_birth', 'gender', 'branch',)

    def create(self, validated_data):
        # groups_data = validated_data.pop('groups')
        admin = self.context['request'].user
        user = User.objects.create(**validated_data)
        user.password =make_password(validated_data.pop('password'))
        user.save()
        # for group_data in groups_data:
        #     # Group.objects.create(user=user, **group_data)
        #     user.groups.add(group_data)
        user.groups.add(admin.groups)
        return user

    def update(self, instance, validated_data):
        user = User.objects.get(pk=instance.id)
        User.objects.filter(pk=instance.id)\
                           .update(**validated_data)
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

        if username and password :
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



