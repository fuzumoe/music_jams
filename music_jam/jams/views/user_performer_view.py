from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from music_jam.jams.models import User
from music_jam.jams.permissions import IsOwner
from music_jam.jams.serializers import UserSerializer


# ViewSets define the view behavior.
class PerformersViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        if self.action == 'retrieve':
            permission_classes = [IsOwner | IsAdminUser]
        if self.action == 'create':
            permission_classes = [IsOwner | IsAdminUser]
        return [permission() for permission in permission_classes]


    def list(self, request):
        self.permission_classes = [IsAuthenticated]
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        self.permission_classes = [IsAuthenticated]
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user, context={'request': request})
        return Response(serializer.data)
