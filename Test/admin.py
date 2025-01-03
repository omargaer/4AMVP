from django import forms
from django.core.exceptions import ValidationError
from django.urls import path
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django import forms
from .models.hard_soft_ware_models import Device

from .models.companies_models import (
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
from .models.user_models import (
    IndividualEntity,
    AccountStatus,
    AccountRole,
    Account
)
from .models.hard_soft_ware_models import (
    BranchOfficeLocation,
    DeviceType,
    DevicePlacementMethod,
    Device,
    SoftwareType,
    Software,
    HardwareType,
    Hardware,
    MaintenanceAction
)
from .models.application_models import (
    ApplicationType,
    Application,
    ApplicationSubject,
    ApplicationPriority,
    ApplicationSLA,
    ApplicationStatus,
    ApplicationStatusHistory,
    ApplicationActions,
    ApplicationFiles,
    ApplicationMessages
)

# list_display: Определяет поля, отображаемые в списке объектов.
# search_fields: Позволяет осуществлять поиск по указанным полям.
# list_filter: Добавляет возможность фильтрации по выбранным полям.
# ordering: Задает порядок сортировки объектов по умолчанию.
# fields: Указывает, какие поля будут отображены в форме редактирования объекта.

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

@admin.register(IndividualEntity)
class IndividualEntityAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'INIPA', 'ITN', 'gender')
    search_fields = ('full_name', 'INIPA', 'ITN')
    list_filter = ('gender',)
    fields = ('full_name', 'INIPA', 'ITN', 'gender')

@admin.register(AccountStatus)
class AccountStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

@admin.register(AccountRole)
class AccountRoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

class AccountOfBranchEmployeesInline(admin.TabularInline):
    model = AccountOfBranchEmployees
    extra = 1
    autocomplete_fields = ['branchOffice']
    verbose_name = 'Филиал сотрудника'
    verbose_name_plural = 'Филиалы сотрудников'

@admin.register(Account)
class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('username', 'email', 'first_name', 'last_name', 'status', 'role')
    list_filter = ('status', 'role', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
                'individual_entity',
                'position',
                'status',
                'role',
                'phone',
                'note',
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'individual_entity',
                'position',
                'status',
                'role',
                'phone',
                'note',
            ),
        }),
    )
    inlines = [AccountOfBranchEmployeesInline]

@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

@admin.register(DevicePlacementMethod)
class DevicePlacementMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'type',
        'inventoryNumber',
        'factoryNumber',
        'responsiblePerson',
        'branchOfficeLocation',
        'placement'
    )
    search_fields = (
        'type__name',
        'inventoryNumber',
        'factoryNumber',
        'responsiblePerson__full_name',
        'branchOfficeLocation__street'
    )
    list_filter = ('type', 'placement', 'branchOfficeLocation')
    fields = (
        'type',
        'inventoryNumber',
        'factoryNumber',
        'responsiblePerson',
        'branchOfficeLocation',
        'placement'
    )

@admin.register(SoftwareType)
class SoftwareTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
        'device',
        'price',
        'license_key',
        'purchaseDate',
        'licenseActivationDate',
        'licenseExpirationDate'
    )
    search_fields = (
        'name',
        'type__name',
        'device__type__name',
        'license_key'
    )
    list_filter = ('type', 'purchaseDate', 'licenseExpirationDate')
    fields = (
        'device',
        'type',
        'name',
        'price',
        'license_key',
        'purchaseDate',
        'licenseActivationDate',
        'licenseExpirationDate'
    )

@admin.register(HardwareType)
class HardwareTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = (
        'type',
        'modelName',
        'price',
        'inventoryNumber',
        'factoryNumber',
        'purchaseDate',
        'installationDate',
        'warrantyExpirationDate',
        'device'
    )
    search_fields = (
        'type__name',
        'modelName',
        'inventoryNumber',
        'factoryNumber',
        'device__type__name'
    )
    list_filter = ('type', 'purchaseDate', 'warrantyExpirationDate')
    fields = (
        'device',
        'type',
        'modelName',
        'price',
        'inventoryNumber',
        'factoryNumber',
        'purchaseDate',
        'installationDate',
        'warrantyExpirationDate'
    )

@admin.register(MaintenanceAction)
class MaintenanceActionAdmin(admin.ModelAdmin):
    list_display = (
        'action_type',
        'device',
        'hardware',
        'action_date',
        'contractor'
    )
    search_fields = (
        'action_type',
        'device__type__name',
        'hardware__modelName',
        'contractor__full_name'
    )
    list_filter = ('action_type', 'contractor')
    readonly_fields = ('action_date',)  # Make action_date read-only
    fields = (
        'device',
        'hardware',
        'action_type',
        'description',
        'contractor',
        'action_date',  # Optional: Include in fields to display it
    )

@admin.register(ApplicationType)
class ApplicationTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        branch_office = self.initial.get('branch_office') or self.data.get('branch_office')
        if branch_office:
            try:
                branch_office_instance = BranchOffice.objects.get(pk=branch_office)
                self.fields['applicant'].queryset = IndividualEntity.objects.filter(
                    accounts__branchOffices=branch_office_instance
                ).distinct()
            except BranchOffice.DoesNotExist:
                self.fields['applicant'].queryset = IndividualEntity.objects.none()
        else:
            self.fields['applicant'].queryset = IndividualEntity.objects.none()
        self.fields['applicant'].required = True if branch_office else False

    def clean(self):
        cleaned_data = super().clean()
        branch_office = cleaned_data.get('branch_office')
        applicant = cleaned_data.get('applicant')

        if branch_office and not applicant:
            raise ValidationError('Заявитель обязателен при выборе филиала.')

        if applicant and branch_office:
            if not IndividualEntity.objects.filter(
                id=applicant.id,
                accounts__branchOffices=branch_office
            ).exists():
                raise ValidationError('Заявитель должен принадлежать выбранному филиалу.')

        if not branch_office and applicant:
            raise ValidationError('Невозможно выбрать заявителя без выбора филиала.')

class ApplicationActionsInline(admin.TabularInline):
    model = ApplicationActions
    extra = 1
    fields = ('timestamp', 'content')
    readonly_fields = ('timestamp',)
    can_delete = False
    show_change_link = False

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationForm
    list_display = (
        'shortDescription',
        'applicationType',
        'company',
        'branch_office',
        'location',
        'applicant',
        'contractor',
    )
    search_fields = ('shortDescription', 'content')
    list_filter = ('applicationType', 'company', 'branch_office', 'location', 'applicant', 'contractor')
    inlines = [ApplicationActionsInline]
    class Media:
        js = ('admin/js/application_admin.js',)

@admin.register(ApplicationSubject)
class ApplicationSubjectAdmin(admin.ModelAdmin):
    list_display = ('application', 'device')
    search_fields = ('application__shortDescription', 'device__inventoryNumber')
    list_filter = ('application', 'device')

@admin.register(ApplicationPriority)
class ApplicationPriorityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ApplicationSLA)
class ApplicationSLAAdmin(admin.ModelAdmin):
    list_display = ('application', 'priority', 'creationDate', 'acceptanceDate', 'completionDate')
    search_fields = ('application__shortDescription', 'priority__name')
    list_filter = ('priority', 'creationDate', 'acceptanceDate', 'completionDate')

@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ApplicationStatusHistory)
class ApplicationStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'changeTime', 'newApplicationStatus')
    search_fields = ('application__shortDescription', 'newApplicationStatus__name')
    list_filter = ('newApplicationStatus', 'changeTime')

@admin.register(ApplicationActions)
class ApplicationActionsAdmin(admin.ModelAdmin):
    list_display = ('application', 'timestamp', 'content')
    search_fields = ('application__shortDescription', 'content')
    list_filter = ('timestamp',)

@admin.register(ApplicationFiles)
class ApplicationFilesAdmin(admin.ModelAdmin):
    list_display = ('application', 'file')
    search_fields = ('application__shortDescription', 'file')
    list_filter = ('application',)

@admin.register(ApplicationMessages)
class ApplicationMessagesAdmin(admin.ModelAdmin):
    list_display = ('application', 'sender', 'timestamp', 'content')
    search_fields = ('application__shortDescription', 'sender__username', 'content')
    list_filter = ('sender', 'timestamp')