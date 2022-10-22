from django.conf.urls import url, include
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from music_jam.jams.models import PerformerRoleProile
from music_jam.jams.permissions import IsOwner
from music_jam.jams.serializers import PerformerRoleProileSerializer


class ProfileViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = PerformerRoleProile.objects.all()
    serializer_class = PerformerRoleProileSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        if self.action == 'retrieve':
            permission_classes = [IsOwner | IsAdminUser]
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)
