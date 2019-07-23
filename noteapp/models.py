import datetime

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.authtoken.models import Token as DefaultTokenModel
from .utils import import_callable


# userprofile model
class Userprofile(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    name = models.CharField(max_length=100, blank=True, validators=[alphanumeric])
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)

    def __str__(self):
        # Return a human readable representation of the model instance.
        return "{}".format(self.name)


# label model
class Label(models.Model):
    text = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, related_name='labels_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


# note model
class Note(models.Model):
    title = models.CharField(max_length=120, blank=True)
    description = models.CharField(max_length=200, blank=True)
    label = models.ForeignKey(Label, related_name='label_created', on_delete=models.CASCADE)
    is_archive = models.BooleanField(default=False, blank=True)
    is_trash = models.BooleanField(default=False, blank=True)
    is_pin = models.BooleanField(default=False, blank=True)
    delete = models.BooleanField(default=False, blank=True)
    color = models.CharField(max_length=100, blank=True)
    images = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    reminder = models.DateTimeField(default=None, null=True, blank=True)
    collaborate = models.ManyToManyField(User, related_name='notes_collaborate')

    def __str__(self):
        return self.title


# def get_note_url(self):  used absolute url for template
#    return reverse('note_edit', kwargs={'pk': self.pk})


# for every user automatically generate token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Register your models here.

TokenModel = import_callable(
    getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel))
