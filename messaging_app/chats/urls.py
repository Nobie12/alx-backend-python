# chats/urls.py
from django.urls import path
from .views import MessageListCreateAPIView, MessageDetailAPIView

urlpatterns = [
    path('messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),
]
