from .serializers import MessageSerializer
from rest_framework import generics
from .models import Message
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permission import IsOwner


# Create your views here.
class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]