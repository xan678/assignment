# url_shortener_app/permissions.py

from rest_framework import permissions

class RetrieveOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow unauthenticated users to perform read-only actions (GET)
        if request.method in permissions.SAFE_METHODS:
            return True

        # For other actions (e.g., PUT, POST, DELETE), require authentication
        return request.user and request.user.is_authenticated
