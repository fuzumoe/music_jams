from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from music_jam.jams import serializers, models


class TestMusicRoleSignal(TestCase):
    def test_music_role_signal_creates_notification(self):
        models.User.objects.all().delete()
        models.MusicRole.objects.all().delete()
        models.PerformerRoleProile.objects.all().delete()
        models.MusicJamRole.objects.all().delete()

        user_data = [
            {
                "email": 'testuser@admin.com',
                "password": 'top_secret',
                "is_staff": True,
                "is_superuser": True,
                "is_active": True
            },
            {
            "email": 'testuser_2@admin.com',
            "password": 'top_secret_2',
            "is_staff": True,
            "is_superuser": False,
            "is_active": True
        }
        ]
        role = {
                "description": "some instrument player",
                "instrument": "some instrument"
            }
        description = "my jam"
        user = models.User.objects.create(**user_data[0])
        user.refresh_from_db()

        host = models.User.objects.create(**user_data[1])
        host.refresh_from_db()

        role = models.MusicRole.objects.create(**role)
        role.refresh_from_db()

        music_jam = models.MusicJam.objects.create(description=description, host=host)
        music_jam.refresh_from_db()

        performer = models.PerformerRoleProile.objects.create(role=role, performer=user)
        performer.refresh_from_db()

        mjr = models.MusicJamRole.objects.create(role=role, performer=user, music_jam=music_jam)
        mjr.refresh_from_db()

        notification = models.Notifications.objects.filter(music_jam=music_jam, notification_for=user)

        self.assertEqual(notification[0].notification_for == user, True)
        self.assertEqual(notification[0].music_jam == music_jam, True)
        self.assertEqual(len(notification) > 0, True)