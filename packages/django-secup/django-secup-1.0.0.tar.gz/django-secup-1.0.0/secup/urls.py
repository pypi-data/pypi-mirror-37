"""fileshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.views.generic import TemplateView
from .settings import SECURE_MEDIA_URL_PREFIX, SECURE_MEDIA_ROOT
from . import views


app_name = 'secup'
urlpatterns = [
    path('files/<path:email>/', views.files, name='files_signed'),
    path('files/', views.files, name='files'),
    path('create-invite/', views.invite, name='invite'),
    path('thanks/', TemplateView.as_view(template_name='secup/thanks.html'), name='thanks'),
    path('upload-with-invite/<path:signed_id>/', views.upload, name='upload'),
    path('upload-to-secup/', views.upload_to_secup, name='upload_to_secup'),
    re_path(r'^%s(?P<path>.*)$' % SECURE_MEDIA_URL_PREFIX,
            views.protected_serve, {'document_root': SECURE_MEDIA_ROOT}),
]
