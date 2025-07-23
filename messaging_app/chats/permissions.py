# chats/permissions.py
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Allow access only to the owner of the message/conversation.
    Assumes the model has a `user` or `owner` foreign key.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users to access the api
    Allow only participants in a conversation to send, view, update and delete messages
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        conversation = obj.conversation
        return request.user in conversation.participants.all()