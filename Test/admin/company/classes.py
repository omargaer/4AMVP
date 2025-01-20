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
    BranchOfficeEmployees
)
from .inlines import (BranchOfficeInline,
                      CompanyInline,
                      BranchOfficeLocationInline,
                      CompanyGroupDecisionMakerInline,
                      CompanyDecisionMakerInline,
                      CompanyPositionInline,
                      BranchOfficeScheduleInline,
                      EmployeesInline,
                      AccountsInline)


@admin.register(CompanyGroup)
class CompanyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'note', 'get_related_companies')
    fields = ('name', 'note')
    search_fields = ('name', 'decisionMaker__full_name')
    list_filter = ('name',)
    inlines = [CompanyGroupDecisionMakerInline,
               CompanyInline]
    def get_related_companies(self, obj):
        related_companies = obj.companies.all()
        return ", ".join([company.name for company in related_companies])

    get_related_companies.short_description = 'Связанные компании'

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('companyGroup', 'name', 'ITN', 'note')
    search_fields = ('name', 'ITN')
    list_filter = ('companyGroup',)
    readonly_fields = ('companyGroup',)
    ordering = ('name',)
    fields = ('companyGroup', 'name', 'ITN', 'note')
    inlines = [CompanyDecisionMakerInline,
               CompanyPositionInline,
               BranchOfficeInline,]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'companyGroup':
            return db_field.formfield(required=False, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'note')
    search_fields = ('name',)
    list_filter = ('company',)
    ordering = ('name',)
    fields = ('company', 'name', 'note')

# @admin.register(BranchOfficeType)
# class BranchOfficeTypeAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
#     list_filter = ('name',)
#     ordering = ('name',)
#     fields = ('name',)

# @admin.register(BranchOfficeStatus)
# class BranchOfficeStatusAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
#     list_filter = ('name',)
#     ordering = ('name',)
#     fields = ('name',)

@admin.register(BranchOffice)
class BranchOfficeAdmin(admin.ModelAdmin):
    list_display = ('company', 'type', 'status', 'phone', 'note', 'street', 'building')
    search_fields = ('company__name', 'type__name', 'status__name', 'phone')
    list_filter = ('company', 'type', 'status')
    ordering = ('company__name', 'type__name')
    fields = ('company', 'type', 'status', 'phone', 'note', 'street', 'building')
    inlines = [BranchOfficeLocationInline,
               BranchOfficeScheduleInline,
               EmployeesInline,
               AccountsInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'company',
            'type',
            'status'
        ).prefetch_related(
            'branchofficeemployees_set__employee',
            'branchofficeemployees_set__position'
        )

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