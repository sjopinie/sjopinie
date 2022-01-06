from django.contrib import admin
from .models import OrgUser


class OrgUserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']
    list_display = [
        'username', 'email', 'date_joined', 'is_active', 'is_superuser'
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        queryset &= self.model.objects.filter(tenant=request.tenant)
        return queryset, may_have_duplicates


admin.site.register(OrgUser, OrgUserAdmin)