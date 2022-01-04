from django.contrib import admin
from .models import Lecturer, Opinion, Subject, Tag


class LecturerAdmin(admin.ModelAdmin):
    search_fields = ['full_name']


class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name']


class OpinionAdmin(admin.ModelAdmin):
    search_fields = ['opinion_text', 'author__username']
    list_display = [
        'author', 'publish_time', 'subject_of_opinion', 'lecturer_of_opinion',
        'note_interesting', 'note_easy', 'note_useful', 'opinion_text'
    ]


admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Opinion, OpinionAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Tag)
