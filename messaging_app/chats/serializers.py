from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'author', 'content', 'timestamp']
        read_only_fields = ['author', 'timestamp']

    def create(self, validated_data):
        user = self.context['request'].user
        return Message.objects.create(author=user, **validated_data)