from django.contrib import admin
from Test.models.companies_models import (
    CompanyGroup,
    CompanyGroupDecisionMaker,
    Company,
    CompanyDecisionMaker,
    Position,
    BranchOfficeType,
    BranchOfficeStatus,
    BranchOffice,
    BranchOfficeLocation,
    BranchOfficeSchedule,
    AccountOfBranchEmployees
)

# Отображение компаний при редактировании группы компаний
class CompanyInline(admin.TabularInline):
    model = Company
    extra = 1  # Количество дополнительных форм для добавления
@admin.register(CompanyGroup)
class CompanyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'note', 'get_related_companies')
    search_fields = ('name',)
    list_filter = ('name',)
    fields = ('name', 'note')
    inlines = [CompanyInline]
    # Отображение связанных компаний в списке групп компаний отдельным столбцом
    def get_related_companies(self, obj):
        related_companies = obj.companies.all()
        return ", ".join([company.name for company in related_companies])

    get_related_companies.short_description = 'Связанные компании'

class BranchOfficeInline(admin.TabularInline):
    """
    Inline-класс для отображения и редактирования филиалов компании в интерфейсе админки.
    """
    model = BranchOffice
    extra = 1  # Количество дополнительных пустых форм для добавления
    fields = ('type', 'status', 'phone', 'note', 'street', 'building')
    show_change_link = True  # Добавляет ссылку на редактирование филиала отдельно

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('companyGroup', 'name', 'ITN', 'note')
    search_fields = ('name', 'ITN')
    list_filter = ('companyGroup',)
    ordering = ('name',)
    fields = ('companyGroup', 'name', 'ITN', 'note')
    inlines = [BranchOfficeInline]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'companyGroup':
            return db_field.formfield(required=False, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# не нужно регистрировать m2m таблицы (возможно)
# @admin.register(CompanyGroupDecisionMaker)
# class CompanyGroupDecisionMakerAdmin(admin.ModelAdmin):
#     list_display = ('companyGroup', 'decisionMaker')
#     search_fields = ('companyGroup__name', 'decisionMaker__full_name')
#     list_filter = ('companyGroup', 'decisionMaker')
#     fields = ('companyGroup', 'decisionMaker')
# @admin.register(CompanyDecisionMaker)
# class CompanyDecisionMakerAdmin(admin.ModelAdmin):
#     list_display = ('company', 'decisionMaker')
#     search_fields = ('company__name', 'decisionMaker__full_name')
#     list_filter = ('company', 'decisionMaker')
#     fields = ('company', 'decisionMaker')
# @admin.register(AccountOfBranchEmployees)
# class AccountOfBranchEmployeesAdmin(admin.ModelAdmin):
#     list_display = ('get_employee', 'get_branch', 'get_account_status')
#     search_fields = ('account__individual_entity__full_name', 'branchOffice__name')
#     list_filter = ('branchOffice', 'account__status')
#     fields = ('account', 'branchOffice', 'account__status', 'created_at', 'updated_at')
#
#     def get_employee(self, obj):
#         return obj.account.individual_entity.full_name
#     get_employee.short_description = 'Сотрудник'
#
#     def get_branch(self, obj):
#         return obj.branchOffice.name
#     get_branch.short_description = 'Филиал'
#
#     def get_account_status(self, obj):
#         return obj.account.status.name
#     get_account_status.short_description = 'Статус учётной записи'

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'note')
    search_fields = ('name',)
    list_filter = ('company',)
    ordering = ('name',)
    fields = ('company', 'name', 'note')

@admin.register(BranchOfficeType)
class BranchOfficeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    fields = ('name',)

@admin.register(BranchOfficeStatus)
class BranchOfficeStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    fields = ('name',)

class BranchOfficeLocationInline(admin.TabularInline):
    model = BranchOfficeLocation
    extra = 1
    fields = ('floor', 'room', 'room_name')

@admin.register(BranchOffice)
class BranchOfficeAdmin(admin.ModelAdmin):
    list_display = ('company', 'type', 'status', 'phone', 'note', 'street', 'building')
    search_fields = ('company__name', 'type__name', 'status__name', 'phone')
    list_filter = ('company', 'type', 'status')
    ordering = ('company__name', 'type__name')
    fields = ('company', 'type', 'status', 'phone', 'note', 'street', 'building')
    inlines = [BranchOfficeLocationInline]

@admin.register(BranchOfficeLocation)
class BranchOfficeLocationAdmin(admin.ModelAdmin):
    list_display = ('branchOffice',  'floor', 'room', 'room_name')
    search_fields = ('branchOffice__company__name', 'room', 'floor', 'room_name')
    list_filter = ['branchOffice']
    ordering = ['branchOffice__company__name']
    fields = ('branchOffice', 'floor', 'room', 'room_name')

@admin.register(BranchOfficeSchedule)
class BranchOfficeScheduleAdmin(admin.ModelAdmin):
    list_display = ('branchOffice', 'day_of_week', 'opening_time', 'closing_time')
    list_filter = ('branchOffice', 'day_of_week')
    ordering = ('branchOffice', 'day_of_week')
    fields = ('branchOffice', 'day_of_week', 'opening_time', 'closing_time')