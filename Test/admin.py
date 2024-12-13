from django.contrib import admin
from .models.companies_models import (
    CompanyGroup,
    Company,
    Position,
    BranchOfficeType,
    BranchOfficeStatus,
    BranchOffice,
    BranchOfficeLocation,
    BranchOfficeSchedule
)
# TODO: регистрировать через декоратор @admin.register()
admin.site.register(CompanyGroup)
admin.site.register(Company)
admin.site.register(Position)
admin.site.register(BranchOfficeType)
admin.site.register(BranchOfficeStatus)
admin.site.register(BranchOffice)
admin.site.register(BranchOfficeLocation)
admin.site.register(BranchOfficeSchedule)
# Register your models here.
