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
from .models.user_models import (
    IndividualEntity,
    Account
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



@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('companyGroup', 'name', 'ITN', 'note')
    search_fields = ('name', 'ITN')
    list_filter = ('companyGroup',)
    ordering = ('name',)
    fields = ('companyGroup', 'name', 'ITN', 'note')


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


@admin.register(BranchOffice)
class BranchOfficeAdmin(admin.ModelAdmin):
    list_display = ('company', 'type', 'status', 'phone', 'note')
    search_fields = ('company__name', 'type__name', 'status__name', 'phone')
    list_filter = ('company', 'type', 'status')
    ordering = ('company__name', 'type__name')
    fields = ('company', 'type', 'status', 'phone', 'note')


@admin.register(BranchOfficeLocation)
class BranchOfficeLocationAdmin(admin.ModelAdmin):
    list_display = ('branchOffice', 'street', 'building', 'floor', 'room')
    search_fields = ('branchOffice__company__name', 'street', 'building', 'room')
    list_filter = ('branchOffice', 'street')
    ordering = ('branchOffice__company__name', 'street')
    fields = ('branchOffice', 'street', 'building', 'floor', 'room')


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
    ordering = ('full_name',)
    fields = ('full_name', 'INIPA', 'ITN', 'gender')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'individual_entity', 'email', 'phone', 'position', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_staff', 'is_active', 'position')
    ordering = ('username',)
    fields = (
        'username',
        'password',
        'individual',
        'email',
        'phone',
        'position',
        'note',
        'groups',
        'user_permissions',
        'is_staff',
        'is_active'
    )