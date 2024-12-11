from django.contrib import admin
from .models.companies_models import (
    CompanyGroup,
    Company,
    Position,
    BranchOfficeType,
    BranchOfficeStatus,
    BranchOffice
)
# TODO: регистрировать через декоратор @admin.register()
admin.site.register(CompanyGroup)
admin.site.register(Company)
admin.site.register(Position)
admin.site.register(BranchOfficeType)
admin.site.register(BranchOfficeStatus)
admin.site.register(BranchOffice)
# Register your models here.
