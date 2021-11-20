from django.db import models

from tenant_schemas.models import TenantMixin

from django.contrib.auth.models import AbstractUser


class Organization(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    domain_url = None  # OGarnąc to

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return f"{self.name} schema:{self.schema_name}"


class OrgUser(AbstractUser):
    tenant = models.ForeignKey(Organization,
                               on_delete=models.CASCADE,
                               blank=False)
    first_name = None
    last_name = None

    def __str__(self):
        return f"{self.username} tenant:{self.tenant.name}"
