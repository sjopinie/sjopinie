from django.urls import path
from . import views

from allauth.account.urls import urlpatterns as account_urlpatterns

email_endpoint = [x for x in account_urlpatterns if x.name == "account_email"]
account_urlpatterns.remove(email_endpoint[0])

urlpatterns = [
    path('settings/', views.settings_page, name='account_settings'),
    path('email/', views.email_change_page, name='account_email'),
] + account_urlpatterns
