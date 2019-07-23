from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from noteapp import views
from rest_framework.authtoken import views as authviews

router = routers.DefaultRouter()
router.register(r'search/note', views.NoteDocumentViewSet, basename='search/note')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('noteapp.urls')),
    path('api-auth/', include('rest_framework.urls')),  # new
    path('accounts/', include('django.contrib.auth.urls')),
    # urls for authtentication view login,logot,password management
    path('', TemplateView.as_view(template_name='home.html'), name='home'),  # new view url  for template
    path('auth/', include('social_django.urls', namespace='social')),  # url for social account
    path('docs/', include_docs_urls(title='noteapi')),
    path('api-token-auth/', authviews.obtain_auth_token),
    path('', include(router.urls))


]
