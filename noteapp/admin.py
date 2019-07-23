from django.contrib import admin

# Register your models here.
from rest_framework.authtoken.admin import TokenAdmin
from .models import Userprofile

from .models import Note

from .models import Label

admin.site.register(Userprofile)
admin.site.register(Note)
admin.site.register(Label)
# create Tokens manually through admin interface"""
TokenAdmin.raw_id_fields = ('user',)
