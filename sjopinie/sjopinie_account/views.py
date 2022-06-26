from django.http import HttpRequest
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .forms import EmailChangeForm


# Create your views here.
@login_required(login_url="/login")
def settings_page(request: HttpRequest):
    return render(request, "sjopinie_account/settings.html")


@login_required(login_url="/login")
def email_change_page(request: HttpRequest):
    # if this is a POST request we need to process the form data
    new_email = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmailChangeForm(request.POST, user=request.user)
        # check whether it's valid:
        if form.is_valid():
            new_email = form.cleaned_data["email"]
            # process the data in form.cleaned_data as required
            pass  #TODO

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EmailChangeForm()

    return render(request, 'sjopinie_account/email_change.html', {
        'form': form,
        'new_email': new_email
    })
