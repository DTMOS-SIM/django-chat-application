from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', ]

    def create(self, validated_data):
        return self

    def update(self, instance, validated_data):
        return self

    def __delete__(self, instance):
        return self


class AppUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = AppUser
        fields = ['user', 'dob', 'gender', 'friend']

    def create(self, validated_data):
        return self

    def update(self, instance, validated_data):
        return self

    def __delete__(self, instance):
        return self


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['name', 'description', 'user']

    def create(self, validated_data):
        return self

    def __delete__(self, instance):
        return self


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['friend']

    def create(self, validated_data):
        return self

    def __delete__(self, instance):
        return self


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = ['message', 'user', 'room']

    def create(self, validated_data):
        return self

    def __delete__(self, instance):
        return self


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['name', 'description', 'user']

    def create(self, validated_data):
        return self

    def __delete__(self, instance):
        return self


class AjaxChatSerializer(serializers.Serializer):

    message = serializers.CharField(max_length=256, allow_blank=False)
    user = serializers.CharField(max_length=256, allow_blank=False)
    room = serializers.CharField(max_length=256, allow_blank=True)
