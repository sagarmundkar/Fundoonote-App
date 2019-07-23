from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Note, Label


# create a form for our UserProfile model


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('text',)


