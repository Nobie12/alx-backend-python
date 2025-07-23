# chats/permissions.py
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Allow access only to the owner of the message/conversation.
    Assumes the model has a `user` or `owner` foreign key.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user