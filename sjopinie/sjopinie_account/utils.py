from django.conf import settings
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured


def log_action(user: User,
               object,
               object_repr: str = None,
               action_flag: ADDITION | CHANGE | DELETION = CHANGE,
               change_message=''):
    # limit log size
    log_count = LogEntry.objects.count()

    if log_count > settings.LOG_MAX_NUMBER:
        LogEntry.objects.all()[log_count - 100:log_count].delete()
    if object_repr is None:
        object_repr = repr(object)
    LogEntry.objects.log_action(user.pk,
                                ContentType.objects.get_for_model(object).pk,
                                object.id, object_repr, action_flag,
                                change_message)
