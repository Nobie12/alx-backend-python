from django.urls import path, include
from rest_framework import routers
from .views import MessageViewSet, ConversationViewSet, RegisterView

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]
