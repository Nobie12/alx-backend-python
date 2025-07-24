from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'author', 'conversation', 'content', 'timestamp']
        read_only_fields = ['author', 'timestamp']

    def create(self, validated_data):
        user = self.context['request'].user
        return Message.objects.create(author=user, **validated_data)

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)