from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase

from music_jam.jams import models


class APITestCaseBase(APITestCase):
    def setUp(self) -> None:
        client = {
            "email": 'testuser@admin.com',
            "password": 'top_secret',
            "is_staff": True,
            "is_superuser": True,
            "is_active": True
        }
        host = {
            "email": 'testuser_2@admin.com',
            "password": 'top_secret_2',
            "is_staff": True,
            "is_superuser": False,
            "is_active": True
        }

        self.user = models.User.objects.create(**client)
        self.user.refresh_from_db()

        self.host = models.User.objects.create(**host)
        self.host.refresh_from_db()


class TestMusicJamViewSet(APITestCaseBase):

    def test_jams_list_succeeds(self):
        self.client.force_authenticate(self.user)

        response = self.client.get("/jams/")

        self.assertEqual((bool(response.json()) or response.json() is not None), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jams_retrieve_succeeds(self):
        models.MusicJam.objects.all().delete()

        description = 'some_jam'
        music_jam = models.MusicJam.objects.create(description=description, host=self.host)

        music_jam.refresh_from_db()
        self.client.force_authenticate(self.host)

        response = self.client.get(path=f"/jams/{music_jam.id}/", format='json')

        self.assertEqual((bool(response.json()) or response.json() is not None), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jams_post_succeeds(self):
        post_data = {
            'description': 'some_data',
            'roles': [{'description': 'some instrument player', 'instrument': 'some instrument'}]
        }

        self.client.force_authenticate(self.host)

        response = self.client.post(path="/jams/", data=post_data, format='json')

        self.assertEqual((bool(response.json()) or response.json() is not None), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jams_join_succeeds(self):
        models.MusicJam.objects.all().delete()
        models.MusicRole.objects.all().delete()
        models.PerformerRoleProile.objects.all().delete()

        description = 'some_jam'
        role = {'description': 'some instrument player', 'instrument': 'some instrument'}

        music_jam = models.MusicJam.objects.create(description=description, host=self.host)
        music_jam.refresh_from_db()

        new_role = models.MusicRole.objects.create(**role)
        new_role.refresh_from_db()

        models.MusicJamRole.objects.create(role=new_role, music_jam=music_jam)
        models.PerformerRoleProile.objects.create(role=new_role, performer=self.user)

        self.client.force_authenticate(self.user)

        response = self.client.get(f"/jams/{music_jam.id}/join_jam/")

        self.assertEqual((bool(response.json()) or response.json() is not None), True)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)


class TestUserProfileViewSet(APITestCaseBase):
    def test_profile_list_succeeds(self):
        self.client.force_authenticate(self.user)

        response = self.client.get("/profiles/")

        self.assertEqual((bool(response.json()) or response.json() is not None), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_retrieve_succeeds(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(path=f"/jams/{self.host.id}/", format='json')

        self.assertEqual((bool(response.json()) or response.json() is not None), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_post_succeeds(self):
        post_data = {'role': {'description': 'some instrument player', 'instrument': 'some instrument'}}

        self.client.force_authenticate(self.user)

        response = self.client.post(path="/profiles/", data=post_data, format='json')

        self.assertEqual((bool(response.json()) or response.json() is not None), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPerformersViewSet(APITestCaseBase):
    def test_performers_list_succeeds(self):
        self.client.force_authenticate(self.user)

        response = self.client.get("/performers/")

        self.assertEqual((bool(response.json()) or response.json() is not None), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_performers_retrieve_succeeds(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(path=f"/performers/{self.host.id}/", format='json')

        self.assertEqual((bool(response.json()) or response.json() is not None), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_performers_post_succeeds(self):
        post_data = [
            {
                "email": "adminuser@example.com",
                "password": "adminuserpassword",
                "is_superuser": True,
                "is_staff": True,
                "is_active": True
            },
            {
                "email": "cleintuser@example.com",
                "password": "cleintuserpassword",
                "is_superuser": False,
                "is_staff": False,
                "is_active": True
            }
        ]

        self.client.force_authenticate(self.user)
        for data in post_data:
            with self.subTest(data):
                response = self.client.post(path="/performers/", data=data, format='json')
                self.assertEqual((bool(response.json()) or response.json() is not None), True)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)