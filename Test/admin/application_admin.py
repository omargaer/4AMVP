from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from Test.models import BranchOffice, IndividualEntity
from Test.models.application_models import (
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