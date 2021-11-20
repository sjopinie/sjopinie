from django.contrib.auth.backends import ModelBackend
from .models import OrgUser


class OrgUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(OrgUser.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = OrgUser.objects.get_by_natural_key(username)
        except OrgUser.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            OrgUser().set_password(password)
        else:
            #TODO fix this (currently user passwords are stored in plain text)
            if user.password == password:
                return user