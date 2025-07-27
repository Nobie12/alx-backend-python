from rest_framework import serializers
from .models import Message, Conversation, CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    # Explicitly define fields to use CharField
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    role = serializers.CharField()

    full_name = serializers.SerializerMethodField()  # for SerializerMethodField

    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")  # 👈 ValidationError
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['sender', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']
