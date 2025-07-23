from .serializers import MessageSerializer
from rest_framework import generics
from .models import Message, Conversation
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsParticipantOfConversation


# List and create messages — only if the user is in the conversation
class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only messages where the user is a participant of the conversation
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')

        if not conversation_id:
            raise PermissionDenied(detail="conversation_id is required.")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied(detail="Conversation not found.")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant in this conversation.")

        serializer.save(author=self.request.user)


# Retrieve, update, or delete a message — only if the user is the owner and in the conversation
class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation, IsOwner]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)
