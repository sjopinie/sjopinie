"""sjopinie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view

docs_urls = [
    path('openapi',
         get_schema_view(title="Sjopinie schema",
                         description="API for all things …"),
         name='openapi-schema'),
    path('docs/',
         TemplateView.as_view(template_name='docs.html',
                              extra_context={'schema_url': 'openapi-schema'}),
         name='docs'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sjopinie_app.urls')),
    path('', include('sjopinie_account.urls')),
]
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += docs_urls
