from django.contrib import admin
from Test.models import (BranchOfficeEmployees)
class CompanyEmployeesInline(admin.TabularInline):
    model = BranchOfficeEmployees
    extra = 1
    fields = ('company', 'branchOffice', 'position')
    readonly_fields = ('company',)

    verbose_name = "Компания"
    verbose_name_plural = "Компании и должности"
    def company(self, obj):
        if obj and obj.branchOffice and obj.branchOffice.company:
            return obj.branchOffice.company.name
        return "-"
    
    # Указываем название столбца в административной панели
    company.short_description = "Компания"