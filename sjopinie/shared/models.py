from django.db import models
from django.db.models.fields import EmailField, Field

from tenant_schemas.models import TenantMixin

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import FieldError, ValidationError
from django.utils.translation import gettext_lazy as _


class Organization(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    domain_url = models.CharField(max_length=50, blank=False)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return f"{self.name} schema:{self.schema_name}"


def _validate_email(email: str):
    email_domain = email[email.find("@") + 1::]
    try:
        Organization.objects.get(domain_url=email_domain)
    except Organization.DoesNotExist:
        raise ValidationError(
            f"email domain: {email_domain} does not match any organization")


class OrgUser(AbstractUser):
    tenant = models.ForeignKey(Organization,
                               on_delete=models.CASCADE,
                               blank=False)
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'),
                              blank=True,
                              validators=[_validate_email])

    def save(self, *args, **kwargs):
        if not self.has_tenant():
            email_domain = self.email[self.email.find("@") + 1::]
            try:
                self.tenant = Organization.objects.get(domain_url=email_domain)
            except Organization.DoesNotExist:
                raise FieldError(
                    f"email domain: {email_domain} does not match any organization"
                )

        super(AbstractUser, self).save(*args, **kwargs)

    def has_tenant(self) -> bool:
        result = True
        try:
            self.tenant
        except Organization.DoesNotExist:
            result = False
        return result

    def __str__(self):
        return f"{self.username} tenant:{self.tenant.name}"
