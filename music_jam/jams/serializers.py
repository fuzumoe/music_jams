from music_jam.jams.models import User, PerformerRoleProile, MusicRole, MusicJam, MusicJamRole
from rest_framework import serializers


# Serializers define the API representation.

class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = User(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['url', 'email', 'password','is_superuser', 'is_staff', 'is_active']
        read_only_fields = ['id', 'url']
        extra_kwargs = {
            'id': {'write_only': True},
            'password': {'write_only': True},
            'is_active': {'write_only': True},
            'is_superuser': {'write_only': True},
            'date_joined': {'write_only': True},
            'is_staff': {'write_only': True},
        }


class MusicRoleSerializer(serializers.Serializer):
    description = serializers.CharField()
    instrument = serializers.CharField()


class PerformerSerializer(serializers.Serializer):
    performer = serializers.CharField( allow_null=True)
    role = MusicRoleSerializer(allow_null=True)


class PerformerRoleProileSerializer(serializers.Serializer):
    role = MusicRoleSerializer(many=False)
    performer = UserSerializer(read_only=True)

    def create(self, validated_data):
        user = User.objects.get(email=self.context["request"].user)
        fetched, created = MusicRole.objects.get_or_create(**validated_data.pop('role'))
        instance = PerformerRoleProile.objects.create(performer=user, role=(fetched or created))
        return instance

    class Meta:
        model = PerformerRoleProile
        fields = ['id', 'role', 'performer']
        read_only_fields = ['id', 'performer']


class MusicJamSerializer(serializers.HyperlinkedModelSerializer):
    host = UserSerializer(read_only=True, many=False, allow_null=True)
    available_roles = MusicRoleSerializer(many=True, allow_null=True, read_only=True)
    performers = PerformerSerializer(read_only=True, many=True, allow_null=True, )
    roles = MusicRoleSerializer(many=True, allow_null=True,)

    def create(self, validated_data):
        user = User.objects.get(email=self.context["request"].user)
        description = validated_data["description"]
        music_jam = MusicJam.objects.create(host=user, description=description)
        for role in validated_data.pop('roles'):
            fetched, created = MusicRole.objects.get_or_create(**role)
            data = {"role": fetched or created, "music_jam": music_jam}
            MusicJamRole.objects.create(**data)
        return music_jam


    class Meta:
        model = MusicJam
        fields = ['id', 'url', 'host', 'description', 'status', 'performers','roles', 'available_roles']
        read_only_fields = ['id', 'url', 'performers', 'status', 'available_roles']
        depth = 1

class MusicJamRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicJamRole
        fields = ['id', 'role', 'performer', 'music_jam', ]
        read_only_fields = ['id', ]
        depth = 1

