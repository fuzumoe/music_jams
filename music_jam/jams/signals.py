from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from music_jam.jams import models



@receiver(post_save, sender=models.MusicJamRole)
def create_user_profile(sender, instance, created, **kwargs):
    all_roles = models.MusicJamRole.objects.filter(music_jam=instance.music_jam)
    all_roles_filled = all([mjr.performer is not None for mjr in all_roles])
    if all_roles_filled:
        for role in all_roles:
            notification = models.Notifications.objects.create(
                notification_for=instance.music_jam.host,
                music_jam=role.music_jam,
                message=f"""  f{role.music_jam.description} that you have joined has staarted"""
            )