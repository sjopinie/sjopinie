from django.http import HttpRequest
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress

from .forms import EmailChangeForm
from .utils import log_action


# Create your views here.
@login_required(login_url="/login")
def settings_page(request: HttpRequest):
    return render(request, "sjopinie_account/settings.html")


@login_required(login_url="/login")
def email_change_page(request: HttpRequest):
    new_email = None
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_email = EmailAddress.objects.get(user=user, primary=True)
            new_email = EmailAddress.objects.add_email(
                request, user, form.cleaned_data["email"], confirm=True)
            new_email.set_as_primary()
            old_email.delete()
            log_action(
                user,
                user,
                repr(user),
                change_message=
                f'email changed from {old_email.email} to {new_email.email}')

    else:
        form = EmailChangeForm()

    return render(request, 'sjopinie_account/email_change.html', {
        'form': form,
        'new_email': new_email
    })
