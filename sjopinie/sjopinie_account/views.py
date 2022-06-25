from django.http import HttpRequest
from django.shortcuts import render

from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/login")
def settings_page(request: HttpRequest):
    return render(request, "sjopinie_account/settings.html")