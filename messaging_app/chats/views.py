from .serializers import MessageSerializer
from rest_framework import generics
from .models import Message
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner


# Create your views here.
class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)