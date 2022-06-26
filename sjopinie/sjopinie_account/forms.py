from django import forms

from allauth.account.utils import filter_users_by_email
from django.utils.translation import gettext as _


class EmailChangeForm(forms.Form):
    email = forms.EmailField(label='Nowy email', max_length=100, required=True)

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        errors = {
            "this_account":
            _("This e-mail address is already associated with this account."),
            "different_account":
            _("This e-mail address is already associated with another account."
              )
        }
        users = filter_users_by_email(email)
        on_this_account = [u for u in users if u.pk == self.user.pk]
        on_diff_account = [u for u in users if u.pk != self.user.pk]

        if on_this_account:
            raise forms.ValidationError(errors["this_account"])
        if on_diff_account:
            raise forms.ValidationError(errors["different_account"])
        return email