import imghdr
import boto3
import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.serializers import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django_redis.serializers import pickle
from rest_framework.generics import CreateAPIView
from rest_framework import generics, pagination

from .decorators import note_login_required
from .documents import NoteDocument
from .redis import RedisMethods
from .forms import UserForm
from .models import Userprofile, Note, Label
from .serializers import UserprofileSerializer, UserSerializer, NoteSerializer, LabelSerializer, NoteDocumentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

import json


from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
    CompoundSearchFilterBackend, FunctionalSuggesterFilterBackend)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet


@login_required
def home(request):
    return render(request, 'home.html')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
    else:
        user_form = UserForm()
    return render(request, 'register.html',
                  {'user_form': user_form,
                   'registered': registered})


class UserprofileList(generics.ListCreateAPIView):
    # This class defines the create behavior of our rest api.
    queryset = Userprofile.objects.all()
    serializer_class = UserprofileSerializer


class UserprofileDetail(generics.RetrieveUpdateDestroyAPIView):  # Userprofile detail view
    queryset = Userprofile.objects.all()
    serializer_class = UserprofileSerializer


class UserList(generics.ListAPIView):  # new abstract user view
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):  # new user details view
    queryset = User.objects.all()
    serializer_class = UserSerializer


# provide a mechanism for clients to obtain a token given the username and password """
r = RedisMethods()


class ApiLogin(CreateAPIView):
    # account and create the JWT token
    serializer_class = UserprofileSerializer

    def post(self, request, *args, **kwargs):
        res = {"message": "something bad happened",  # give the element what you want in rest api
               "data": {},
               "success": False,
               "username": {}}
        try:
            username = request.data['username']
            if username is None:  # if username is None
                raise Exception("Username is required")  # raise exception Username is required
            password = request.data['password']
            if password is None:
                raise Exception("password is required")
            user = authenticate(username=username, password=password)  # validate the password
            print('user-', user)
            if user:
                if user.is_active:  # check if the user is active or not.
                    payload = {'username': username, 'password': password}
                    jwt_token = {
                        'token': jwt.encode(payload, "Cypher", algorithm='HS256').decode('utf-8')
                    }
                    print(jwt_token)  # print JWT Token

                    """ JWT token stored in cache"""
                    token = jwt_token['token']
                    r.set_token("p2", token)  # set the token in redis cache
                    token_val = r.get_token("p2")  # get the value of token from cache
                    print("Display The Tokens using get_token()")
                    print(token_val)  # print the cache token
                    print("Display the length of Token")
                    len_str = r.length_str("p2")
                    print(len_str)  # returns the length of token
                    res['message'] = "Logged in Successfully"
                    res['data'] = token
                    res['success'] = True
                    res['username'] = username
                    return Response(res)  # if active then return response with jWT Token
                else:
                    return Response(res)  # else user is not active
            if user is None:
                return Response(res)  # else user is not exist
        except Exception as e:
            print(e)
            return Response(res)  # print response as is


# All Notes List
class NoteList(APIView):
    @method_decorator(note_login_required)
    def get(self, request):
        notes = Note.objects.all()[:20]
        data = NoteSerializer(notes, many=True).data
        return Response(data)


# Creating Notes
class CreateNote(CreateAPIView):
    serializer_class = NoteSerializer

    def post(self, request, *args, **kwargs):
        res = {"message": "something bad happened",  # give the element what you want in rest api
               "success": False,
               "data": {}}
        try:
            data = request.data
            serializer = NoteSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                res["message"] = "Successfully created note"
                res['success'] = True
                res["data"] = serializer.data
                res['mail'] = "mail send successfully"
                notes = json.dump(res)
                # print(serializer.data)
                for i in serializer.data['collaborate']:
                    user = User.objects.get(id=i)
                    print(i)
                    if user:

                        send_mail('Subject here',
                                  notes,
                                  request.user.email,
                                  [str(user.email)],
                                  fail_silently=False)
            return Response(res, status=200)
        except:
            return Response(res, status=400)


# Displaying all notes
class NoteDetail(APIView):
    def get(self, request, pk):
        try:
            notes = get_object_or_404(Note, pk=pk)
            data = NoteSerializer(notes).data
            # send_feedback_email_task.delay()

            return JsonResponse(data)
        except:
            return Response({"Message Failed"}, status=400)


# Updating notes
class NoteUpdate(APIView):
    """ API endpoint that allows users to be viewed or edited."""
    serializer_class = NoteSerializer

    def put(self, request, pk):
        res = {"message": "something bad happened",  # give the element what you want in rest api
               "success": False}
        try:
            notes = Note.objects.get(pk=pk)  # get the note
            data = request.data
            serializer = NoteSerializer(notes, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()  # if valid save
                res["message"] = "Successfully updated note"
                res['success'] = True
            return Response(res, status=200)
        except:
            return Response(res, status=400)


# deleting the note
class NoteDelete(generics.DestroyAPIView):
    def get(self, request, pk):
        note = Note.objects.get(pk=pk)
        note.delete()
        return Response("Note is deleted")


# checking the note is in trash or not
class TrashView(APIView):
    def get(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
            if note.is_trash == False:
                note.trash = True  # if trash = false
                note.save()
            return Response("Note is Trash")
        except Exception as e:
            print(e)


# Note is archive or not
class ArchiveNote(APIView):
    try:
        def get(self, request, pk):
            note = Note.objects.get(pk=pk)
            try:
                if note.delete == False and note.is_trash == False:
                    if note.is_archive == False:  # Check if trash is false or true
                        note.is_archive = True  # if false then set True
                        note.save()  # save the note
                    else:
                        return Response("Already archive")
                    return Response("Archive is set")
                else:
                    return Response("Note is already in trash and deleted")
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


# Checking note is pin or not
class PinNote(APIView):
    try:
        def get(self, request, pk):
            note = Note.objects.get(pk=pk)
            try:
                if note.is_pin == False:  # check if pin is false or true
                    note.is_pin = True  # if false then set True
                    note.save()  # save the note
                else:
                    return Response("Already Pin")
                return Response("Pin is set")
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


# Pagination of notes
class NotePagination(pagination.PageNumberPagination):
    page_size = 5  # page min size
    page_size_query_param = 'page_size'
    max_page_size = 1000  # define page max size

    def get_paginated_response(self, data):
        try:
            return Response({
                'links': {
                    'next': self.get_next_link(),  # getting next page link
                    'previous': self.get_previous_link()  # getting previous page link
                },
                'count': self.page.paginator.count,  # count the all notes in page
                'results': data
            })
        except Exception as e:
            print(e)


# pagination of note list
class NoteListView(generics.ListAPIView):
    serializer_class = NoteSerializer  # serialize class of note serializer
    pagination_class = NotePagination  # defining pagination class
    queryset = Note.objects.all()  # getting all object of notes


# label list
class LabelList(APIView):
    def get(self, request):
        labels = Label.objects.all()[:20]
        data = LabelSerializer(labels, many=True).data
        return Response(data)


# creating labels
class CreateLabel(APIView):
    serializer_class = LabelSerializer

    def post(self, request):
        res = {"message": "something bad happened",  # give the element what you want in rest api
               "success": False,
               "data": {}}
        try:
            data = request.data
            print(data)
            serializer = LabelSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                res["message"] = "Successfully created label"
                res['success'] = True
                res["data"] = serializer.data
            return Response(res, status=200)
        except:
            return Response(res, status=400)


# label details
class LabelDetail(APIView):
    try:
        def get(self, request, pk):
            labels = get_object_or_404(Label, pk=pk)
            data = LabelSerializer(labels).data
            dict = pickle.dumps(data)  # Stored data into cache
            r.set_token('dict', dict)
            print("set data 1")
            read_dict = r.get_token('dict')
            data1 = pickle.loads(read_dict)
            print(data1)
            return JsonResponse(data)
    except Exception as e:
        print(e)


class LabelUpdate(APIView):
    """ API endpoint that allows users to be viewed or edited."""
    serializer_class = LabelSerializer

    def put(self, request, pk):
        res = {"message": "something bad happened",  # give the element what you want in rest api
               "success": False}
        try:
            labels = Label.objects.get(pk=pk)  # get the note
            data = request.data
            serializer = LabelSerializer(labels, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()  # if valid save
                res["message"] = "Successfully updated label"
                res['success'] = True
            return Response(res, status=200)
        except:
            return Response(res, status=400)


class UploadImage(APIView):
    """ create bucket using boto3 services method"""

    def post(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)  # get the note
            images = request.FILES['image']
            images_name = images.name
            val = imghdr.what(images)
            if val:
                note.images = images
                print(note.images)
                s3 = boto3.client('s3')
                bucket_name = "s3profilebucket1"
                s3.upload_file(Bucket=bucket_name, Key=images_name, Body=images)
            return Response("Upload Image")
        except:
            return ("cant upload image")


class NoteDocumentViewSet(DocumentViewSet):
    """
    Using the note document and note serializer class
    search the note model field and
    filter and order the fields
    """
    document = NoteDocument
    serializer_class = NoteDocumentSerializer

    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        FunctionalSuggesterFilterBackend
    ]

    # Define search fields
    search_fields = (
        'title',
        'description',
        'color',
        'reminder',
        'label',

    )

    # Filter fields
    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'title': 'title.raw',
        'description': 'description.raw',
        'color': 'color.raw',
        'reminder': 'reminder.raw',
        'label': 'label.raw'

    }

    # Define ordering fields
    ordering_fields = {
        'title': 'title.raw',
        'description': 'description.raw',
        'color': 'color.raw',
        'reminder': 'reminder.raw',
        'label': 'label.raw',

    }

    # define functional suggester fields
    functional_suggester_fields = {
        'title': 'title.raw',
        'description': 'description.raw',
        'color': 'description.raw',
        'reminder': 'reminder.raw',
        'label': 'label.raw',
    }
