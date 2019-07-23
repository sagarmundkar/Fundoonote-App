from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from . import views

from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

urlpatterns = [
    path('userprofile/', views.UserprofileList.as_view()),
    path('userprofile/<int:pk>/', views.UserprofileDetail.as_view()),
    path('User/list/', views.UserList.as_view()),  # new url for user list
    path('User/detail/<int:pk>/', views.UserDetail.as_view()),
    path('apidocs/', get_swagger_view(title='API Deatils'), name='apidocs'),  # url for schema format data
    path('register/', views.register, name='register'),  # url for signup
    path('User/login/', views.ApiLogin.as_view(), name='login'),  # url is rest_Login user

    # apis for note crud
    path('Notes/show', views.NoteList.as_view()),  # all notes url
    path('Notes/details/<int:pk>', views.NoteDetail.as_view()),
    path('Notes/create/', views.CreateNote.as_view()),  # new note url
    path('Notes/List', views.NoteListView.as_view()),
    path('Notes/edit/<int:pk>', views.NoteUpdate.as_view()),
    path('Notes/delete/<int:pk>', views.NoteDelete.as_view()),
    path('Notes/trash/<int:pk>', views.TrashView.as_view()),
    path('Notes/archive/<int:pk>', views.ArchiveNote.as_view()),
    path('Notes/pin/<int:pk>', views.PinNote.as_view()),

    # apis for label crud
    path('Label/list', views.LabelList.as_view()),
    path('Label/create/', views.CreateLabel.as_view()),
    path('Label/details/<int:pk>', views.LabelDetail.as_view()),
    path('Label/edit/<int:pk>', views.LabelUpdate.as_view()),
    # user authentication login
    #  path('Rest/user/login', LoginView.as_view(), name='rest_login'),
    # path('Rest/user/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    # path('Rest/user/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),

    # URLs that require a user to be logged in with a valid session / token.
    # path('logout/', LogoutView.as_view(), name='rest_logout'),
    # path('Reset/user/list', UserDetailsView.as_view(), name='rest_user_details'),
    # path('Reset/user/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),

    path('upload/<int:pk>/', views.UploadImage.as_view()),

]
