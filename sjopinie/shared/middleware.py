from tenant_schemas.middleware import BaseTenantMiddleware

from .models import Organization

from tenant_schemas.utils import get_public_schema_name


class OrgUserMiddleware(BaseTenantMiddleware):
    def get_tenant(self, model, hostname, request):
        u = request.user
        if hasattr(u, "tenant"):
            return u.tenant
        else:
            return Organization.objects.get(
                schema_name=get_public_schema_name())
