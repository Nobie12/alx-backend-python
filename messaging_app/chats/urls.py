# chats/urls.py
from django.urls import path
from .views import MessageListCreateAPIView, MessageDetailAPIView, RegisterView, ConversationListCreateAPIView

urlpatterns = [
    path('messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),
    path('conversations/', ConversationListCreateAPIView.as_view(), name='conversation-list-create'),
    path('register/', RegisterView.as_view(), name='register'),
]
