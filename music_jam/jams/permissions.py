from rest_framework import permissions

from music_jam.jams.models import User


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return User.objects.get(pk=view.kwargs['pk']) == request.user