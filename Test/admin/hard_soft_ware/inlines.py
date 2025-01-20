from django.contrib import admin
from Test.models import Software, Hardware, MaintenanceAction


class SoftwareInline(admin.TabularInline):
    model = Software
    extra = 0
    fields = ('type', 'name', 'license_key', 'licenseExpirationDate')

class HardwareInline(admin.TabularInline):
    model = Hardware
    extra = 0
    fields = ('type', 'modelName', 'inventoryNumber', 'factoryNumber', 'installationDate', 'warrantyExpirationDate')

class MaintenanceActionInline(admin.TabularInline):
    model = MaintenanceAction
    extra = 0
    fields = ('description', 'action_date', 'contractor', 'application')
    readonly_fields = ('description', 'action_date', 'contractor', 'application')
    max_num = 0
    can_delete = False


def get_readonly_fields(self, request, obj=None):
    if obj:  # Editing an existing object
        return self.readonly_fields + ('action_date',)
    return self.readonly_fields