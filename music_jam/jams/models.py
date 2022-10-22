from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class MusicRole(models.Model):
    instrument = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True)


class PerformerRoleProile(models.Model):
    performer = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(MusicRole, on_delete=models.CASCADE)


class MusicJam(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    @property
    def status(self):
        instance = self
        music_jam_role = MusicJamRole.objects.filter(music_jam_id=instance.id)
        mstatus = [(mjr.performer is None) for mjr in music_jam_role]
        return "pending" if all(mstatus) == True else "started"

    @property
    def roles(self):
        instance = self
        music_jam_role = MusicJamRole.objects.filter(music_jam_id=instance.id)
        roles = [mjr.role for mjr in music_jam_role]
        return roles

    @property
    def available_roles(self):
        instance = self
        music_jam_role = MusicJamRole.objects.filter(music_jam_id=instance.id)
        roles = [mjr.role for mjr in music_jam_role]
        return [role for role in self.roles if role]

    @property
    def performers(self):
        instance = self
        music_jam_role = MusicJamRole.objects.filter(music_jam_id=instance.id)
        performers = [{"role":mjr.role, "performer": mjr.performer} for mjr in music_jam_role if mjr.performer]
        return performers


class MusicJamRole(models.Model):
    role = models.ForeignKey(MusicRole, on_delete=models.CASCADE, null=True, blank=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    music_jam = models.ForeignKey(MusicJam, on_delete=models.CASCADE, null=True, blank=True)


class Notifications(models.Model):
    notification_for = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    music_jam = models.ForeignKey(MusicJam, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
