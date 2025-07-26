from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Conversation, CustomUser
from .serializers import MessageSerializer, ConversationSerializer, RegisterSerializer
from .pagination import ChatPagination
from .permissions import IsOwner, IsParticipantOfConversation


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']
    pagination_class = ChatPagination

    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).order_by('-sent_at')

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')

        if not conversation_id:
            raise serializers.ValidationError({"detail": "conversation_id is required."})

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError({"detail": "Conversation not found."})

        if self.request.user not in conversation.participants.all():
            raise serializers.ValidationError({"detail": "You are not a participant in this conversation."})

        serializer.save(sender=self.request.user)


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class RegisterView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
