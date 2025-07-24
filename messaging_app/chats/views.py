from .serializers import MessageSerializer, RegisterSerializer, ConversationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ChatPagination
from rest_framework import generics
from .models import Message, Conversation
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsParticipantOfConversation


# List and create messages — only if the user is in the conversation
class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']
    pagination_class = ChatPagination

    def get_queryset(self):
        # Only messages where the user is a participant of the conversation
        return Message.objects.filter(conversation__participants=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')

        if not conversation_id:
            return Response(
                {"detail": "conversation_id is required."},
                status=status.HTTP_403_FORBIDDEN
                )
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_403_FORBIDDEN
                )
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
                )

        serializer.save(author=self.request.user)



# Retrieve, update, or delete a message — only if the user is the owner and in the conversation
class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation, IsOwner]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ConversationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only conversations the user is part of
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)  # Add current user by default