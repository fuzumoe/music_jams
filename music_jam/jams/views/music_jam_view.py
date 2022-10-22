from django.conf.urls import url, include
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from music_jam.jams.models import MusicJam, PerformerRoleProile, MusicRole, MusicJamRole
from music_jam.jams.permissions import IsOwner
from music_jam.jams.serializers import MusicJamSerializer, MusicJamRoleSerializer


# ViewSets define the view behavior.
# class MusicJamViewSet(viewsets.ModelViewSet):
class MusicJamViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = MusicJam.objects.all()
    serializer_class = MusicJamSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return MusicJamSerializer
        if self.action == 'retrieve':
            return MusicJamSerializer
        if self.action == 'join_jam':
            return MusicJamRoleSerializer

        return MusicJamSerializer

    def list(self, request):
        self.permission_classes = [IsAuthenticated]
        data = [d for d in self.queryset if d.status == 'pending']
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        self.permission_classes = [IsAuthenticated]
        music_jam = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(music_jam, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        self.permission_classes = [IsAuthenticated]
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def join_jam(self, request, pk=None):
        self.permission_classes = [IsAuthenticated]
        user = request.user
        perfermor_role = PerformerRoleProile.objects.filter(performer=user)
        if len(perfermor_role) > 0:
            performer_role_ids = [prf.role.id for prf in perfermor_role]
            music_jam_roles = MusicJamRole.objects.filter(music_jam_id=pk)
            music_jam_roles_ids = [msjr.role.id for msjr in music_jam_roles]
            role_matches_jam = all(z == i for z, i in zip(music_jam_roles_ids, performer_role_ids))
            if role_matches_jam:
                music_jam_role = MusicJamRole.objects.filter(music_jam_id=pk).filter(role_id=music_jam_roles_ids[0])
                for mjr in music_jam_role:
                    mjr.performer = user
                    mjr.save()
                message = f"You have succefully joined the jam '{pk}'"
                return Response({"message": message}, status=status.HTTP_202_ACCEPTED)
            else:
                message = "You do not posses the right music roles to join the jam"
                return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)
        else:
            message = "You do not posses the right music roles to join the jam"
            return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)
