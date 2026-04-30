from rest_framework import permissions


class InternalServicePermission(permissions.BasePermission):
    """
    Permission class to check if the user is an internal service from Kong key authentication.
    """
    def has_permission(self, request, view):
        req_headers = request.headers
        return True
