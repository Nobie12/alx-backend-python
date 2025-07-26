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
    Only allow participants of the conversation to view, create, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj is a Message instance
        conversation = obj.conversation
        user = request.user

        # Allow only participants to view, update, delete messages
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return user in conversation.participants.all()

        return False