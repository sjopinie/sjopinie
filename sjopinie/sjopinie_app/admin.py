from django.contrib import admin
from .models import Lecturer, Opinion, Subject, Tag

admin.site.register(Lecturer)
admin.site.register(Opinion)
admin.site.register(Subject)
admin.site.register(Tag)
