from django.contrib import admin

from Test.admin.application.inlines import (ApplicationActionsInline,
                                            ApplicationSubjectInline,
                                            ApplicationStatusHistoryInline,
                                            ApplicationSLAInline,
                                            ApplicationMessagesInline,
                                            ApplicationFilesInline)
from Test.forms import ApplicationForm

from Test.models.application_models import (
    ApplicationType,
    Application,
    ApplicationSubject,
    ApplicationPriority,
    ApplicationSLA,
    ApplicationStatus,
    ApplicationActions,
    ApplicationFiles,
    ApplicationMessages,
    ApplicationStatusHistory
)

# Заявка
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationForm
    list_display = ('shortDescription',
                    'applicationType',
                    'company',
                    'branch_office',
                    'location',
                    'applicant',
                    'contractor')
    search_fields = list_display
    list_filter = ('applicationType',
                   'company',
                   'branch_office',
                   'location',
                   'applicant',
                   'contractor')
    inlines = [ApplicationSLAInline,
               ApplicationStatusHistoryInline,
               ApplicationSubjectInline,
               ApplicationActionsInline,
               ApplicationMessagesInline,
               ApplicationFilesInline]
    class Media:
        js = ('admin/js/application.js',)

# Исключены потому что инлайн

# # Тип заявки
# @admin.register(ApplicationType)
# class ApplicationTypeAdmin(admin.ModelAdmin):
#     list_display = ['name']
# Предметы
# @admin.register(ApplicationSubject)
# class ApplicationSubjectAdmin(admin.ModelAdmin):
#     list_display = ('application', 'device')
#     search_fields = ('application__shortDescription', 'device__inventoryNumber')
#     list_filter = ('application', 'device')
#
# # Приоритет
# @admin.register(ApplicationPriority)
# class ApplicationPriorityAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
#

# SLA
# @admin.register(ApplicationSLA)
# class ApplicationSLAAdmin(admin.ModelAdmin):
#     list_display = ('application', 'priority', 'creationDate', 'acceptanceDate', 'completionDate')
#     search_fields = ('application__shortDescription', 'priority__name')
#     list_filter = ('priority', 'creationDate', 'acceptanceDate', 'completionDate')

# Статус
# @admin.register(ApplicationStatus)
# class ApplicationStatusAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)


# @admin.register(ApplicationStatusHistory)
# class ApplicationStatusHistoryAdmin(admin.ModelAdmin):
#     list_display = ('application', 'changeTime', 'newApplicationStatus')
#     search_fields = ('application__shortDescription', 'newApplicationStatus__name')
#     list_filter = ('newApplicationStatus', 'changeTime')

# @admin.register(ApplicationActions)
# class ApplicationActionsAdmin(admin.ModelAdmin):
#     list_display = ('application', 'timestamp', 'content')
#     search_fields = ('application__shortDescription', 'content')
#     list_filter = ('timestamp',)

# @admin.register(ApplicationFiles)
# class ApplicationFilesAdmin(admin.ModelAdmin):
#     list_display = ('application', 'file')
#     search_fields = ('application__shortDescription', 'file')
#     list_filter = ('application',)

# @admin.register(ApplicationMessages)
# class ApplicationMessagesAdmin(admin.ModelAdmin):
#     list_display = ('application', 'sender', 'timestamp', 'content')
#     search_fields = ('application__shortDescription', 'sender__username', 'content')
#     list_filter = ('sender', 'timestamp')