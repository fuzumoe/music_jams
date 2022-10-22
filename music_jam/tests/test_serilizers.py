from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from music_jam.jams import serializers, models


class TestUserSerializers(TestCase):
    def setUp(self) -> None:
        self.users_data = [
            {
                "email": 'user_1@admin.com',
                "password": 'admin',
                "is_staff": False,
                "is_superuser": False,
                "is_active": True
            },
            {
                "email": 'user_2@test.com',
                "password": 'test',
                "is_staff": True,
                "is_superuser": True,
                "is_active": True
            }
        ]
        self.factory = APIRequestFactory()
        self.context = {'request': self.factory.get('/user/')}

    def test_user_serializer_accepts_single_valid_data(self):
        serializer = serializers.UserSerializer(data=self.users_data[0], many=False, context=self.context)
        self.assertEqual(serializer.is_valid(), True)

    def test_user_serializer_accepts_muliple_valid_data(self):
        serializer = serializers.UserSerializer(data=self.users_data, many=True, context=self.context)
        self.assertEqual(serializer.is_valid(), True)

    def test_user_serializer_rejects_single_invalid_data(self):
        data = self.users_data[0]
        data.pop("email")
        serializer = serializers.UserSerializer(data=data, many=False, context=self.context)
        self.assertEqual(serializer.is_valid(), False)


class TestMusicRoleSerializer(TestCase):
    def setUp(self) -> None:
        self.music_roles = [
            {
                "instrument": "Bass guitar",
                "description": "Bass guitar player"
            },
            {
                "instrument": "Acoustic guitar",
                "description": "Acoustic guitar player"
            },
        ]

    def test_music_role_serializer_accepts_single_valid_data(self):
        serializer = serializers.MusicRoleSerializer(data=self.music_roles[0], many=False, )
        self.assertEqual(serializer.is_valid(), True)

    def test_music_role__serializer_accepts_muliple_valid_data(self):
        serializer = serializers.MusicRoleSerializer(data=self.music_roles, many=True, )
        self.assertEqual(serializer.is_valid(), True)

    def test_music_role_serializer_rejects_single_invalid_data(self):
        data = self.music_roles[0]
        data.pop("instrument")
        serializer = serializers.MusicRoleSerializer(data=data, many=False)
        self.assertEqual(serializer.is_valid(), False)


class TestPerformerSerializer(TestCase):
    def setUp(self) -> None:
        self.performer = [
            {
                "performer": "test@test.com",
                "role": {
                    "instrument": "Bass guitar",
                    "description": "Bass guitar player"
                }
            },
            {
                "performer": "test@test.com",
                "role": {
                    "instrument": "Acoustic guitar",
                    "description": "Acoustic guitar player"
                }
            }
        ]

    def test_perfomer_serializer_accepts_single_valid_data(self):
        serializer = serializers.PerformerSerializer(data=self.performer[0], many=False, )
        serializer.is_valid()
        self.assertEqual(serializer.is_valid(), True)

    def test_perfomer_serializer_accepts_muliple_valid_data(self):
        serializer = serializers.PerformerSerializer(data=self.performer, many=True, )
        self.assertEqual(serializer.is_valid(), True)

    def test_perfomer_serializer_rejects_single_invalid_data(self):
        data = self.performer[0]
        data.pop("role")
        serializer = serializers.PerformerSerializer(data=data, many=False)
        self.assertEqual(serializer.is_valid(), False)


class TestPerformerRoleProileSerializer(TestCase):
    def setUp(self) -> None:
        self.performer_role = [
            {
                "performer": {
                    "email": "test@test.com",
                },
                "role": {
                    "instrument": "Bass guitar",
                    "description": "Bass guitar player"
                }
            },
            {"performer": {
                "email": "admin@admin.com",
            },
                "role": {
                    "instrument": "Acoustic guitar",
                    "description": "Acoustic guitar player"
                }
            }
        ]
        self.factory = APIRequestFactory()

    def test_perfomer_role_serializer_accepts_single_valid_data(self):
        data = self.performer_role[0]
        serializer = serializers.PerformerRoleProileSerializer(data=self.performer_role[0], many=False, )
        self.assertEqual(serializer.is_valid(), True)

    def test_perfomer_role_serializer_accepts_muliple_valid_data(self):
        serializer = serializers.PerformerRoleProileSerializer(data=self.performer_role, many=True, )
        self.assertEqual(serializer.is_valid(), True)

    def test_perfomer_role_serializer_rejects_single_invalid_data(self):
        data = self.performer_role[0]
        data.pop("role")
        serializer = serializers.PerformerRoleProileSerializer(data=data, many=False)
        self.assertEqual(serializer.is_valid(), False)

    def test_perfomer_role_serializer_creates_performer_role(self):
        data = self.performer_role[0]
        email = data["performer"]["email"]
        instrument = data["role"]["instrument"]
        request = APIRequestFactory().request()
        request.user = models.User.objects.get(email=email)
        context = {"request": request}
        serializer = serializers.PerformerRoleProileSerializer(data=data, context=context)

        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        performer_role_exists = any(
            [
                pr.role.instrument == instrument
                for pr in models.PerformerRoleProile.objects.filter(performer=request.user)
            ]
        )

        self.assertEqual(performer_role_exists, True)


class MusicJamSerializer(TestCase):

    def setUp(self) -> None:
        self.muscic_jam = [{
            "host": {"email": "test@test.com", "is_superuser": False},
            "description": "Mothers Day Jam",
            "status": "pending",
            "performers": [],
            "roles": [
                    {"description": "Harp player", "instrument": "Harp"},
                    {"description": "Accordion player", "instrument": "Accordion"},
            ],
            "available_roles": [
                {"description": "Bugle player", "instrument": "Bugle"},
                {"description": "Accordion player", "instrument": "Accordion"},
            ]
        },
            {
                "host": {"email": "test@test.com", "is_superuser": False},
                "description": "Saint patric Day Jam",
                "status": "pending",
                "performers": [],
                "roles": [
                    {"description": "Harp player", "instrument": "Harp"},
                    {"description": "Accordion player", "instrument": "Accordion"},
                ],
                "available_roles": [
                    {"description": "Harp player", "instrument": "Harp"},
                    {"description": "Accordion player", "instrument": "Accordion"},
                ]
            }
        ]
        self.factory = APIRequestFactory()
        self.context = {'request': self.factory.get('/jams/')}

    def test_perfomer_serializer_accepts_single_valid_data(self):
        data = self.muscic_jam[0]
        serializer = serializers.MusicJamSerializer(data=self.muscic_jam[0], many=False, context=self.context)
        self.assertEqual(serializer.is_valid(), True)

    def test_perfomer_serializer_accepts_muliple_valid_data(self):
        serializer = serializers.MusicJamSerializer(data=self.muscic_jam, many=True, context=self.context)
        self.assertEqual(serializer.is_valid(), True)
    #
    def test_perfomer_serializer_saves_valid_data(self):
        data = self.muscic_jam[0]
        roles = data["roles"]
        description = data["description"]
        email = data["host"]["email"]
        description = data["description"]
        request = APIRequestFactory().request()
        request.user = models.User.objects.get(email=email)
        context = {"request": request}
        serializer = serializers.MusicJamSerializer(data=data, context=context)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(serializer.is_valid(), True)
        music_jam_exists = any(
            [
                music_jam.description == description
                for music_jam in models.MusicJam.objects.filter(host__id=request.user.id)
            ]
        )

        self.assertEqual(music_jam_exists, True)
