from django.db import models

from tenant_schemas.models import TenantMixin

from django.contrib.auth.models import AbstractUser


class Organization(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class OrgUser(AbstractUser):
    tenant = models.ForeignKey(Organization,
                               on_delete=models.CASCADE,
                               blank=False)
    first_name = None
    last_name = None
