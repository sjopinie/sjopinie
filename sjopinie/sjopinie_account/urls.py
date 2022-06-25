from django.urls import path
from . import views

from allauth.account.urls import urlpatterns as account_urlpatterns

urlpatterns = [
    path('settings/', views.settings_page, name='account_settings'),
] + account_urlpatterns
