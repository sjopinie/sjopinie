from django.contrib import admin
from .models import OrgUser


class OrgUserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']
    list_display = ['username', 'tenant', 'date_joined']
    list_filter = ['tenant']


admin.site.register(OrgUser, OrgUserAdmin)