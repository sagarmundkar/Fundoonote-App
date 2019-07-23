from django.contrib.auth.models import User
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import pagination
from rest_framework.validators import UniqueValidator

from .documents import NoteDocument
from .models import Userprofile
from .models import Note, Label
from rest_framework import serializers


class UserprofileSerializer(serializers.ModelSerializer):
    # Serializer to map the Model instance into JSON format.

    class Meta:
        # Meta class to map serializer's fields with the model fields.
        model = Userprofile
        fields = ('email', 'username', 'password')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class NoteSerializer(serializers.ModelSerializer):
    """
        Serializes note querysets.
    """

    class Meta:
        model = Note
        fields = '__all__'


class PaginatedNoteSerializer(pagination.PageNumberPagination):
    """
    Serializes page objects of note querysets.
    """

    class Meta:
        object_serializer_class = NoteSerializer


class LabelSerializer(serializers.ModelSerializer):
    """
       Serializes of label querysets.
    """

    class Meta:
        model = Label
        fields = ('id', 'text', 'created_by')


class NoteDocumentSerializer(DocumentSerializer):
    """
        Serializer for requesting a title, description and color search from note class.
        """
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    color = serializers.CharField(read_only=True)

    class Meta:
        document = NoteDocument
        fields = ('title', 'description', 'color', 'label')
