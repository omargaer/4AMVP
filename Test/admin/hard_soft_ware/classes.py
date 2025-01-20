from django.contrib import admin
from Test.models.hard_soft_ware_models import (
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
from .inlines import *

# @admin.register(DeviceType)
# class DeviceTypeAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
#     fields = ('name',)
#
# @admin.register(DevicePlacementMethod)
# class DevicePlacementMethodAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
#     fields = ('name',)
#
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'type',
        'inventoryNumber',
        'factoryNumber',
        'responsiblePerson',
        'branchOfficeLocation',
        'placement',
        'purchaseDate',
        'warrantyExpirationDate'
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
        'name',
        'branchOfficeLocation',
        'type',
        'responsiblePerson',
        'placement',
        'inventoryNumber',
        'factoryNumber',
        'purchaseDate',
        'warrantyExpirationDate'
    )
    inlines = [SoftwareInline, HardwareInline, MaintenanceActionInline]
#
# @admin.register(SoftwareType)
# class SoftwareTypeAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
#     fields = ('name',)

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
        'device',
        'price',
        'license_key',
        'purchaseDate',
        'installationDate',
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
        'installationDate',
        'licenseActivationDate',
        'licenseExpirationDate'
    )

# @admin.register(HardwareType)
# class HardwareTypeAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
#     fields = ('name',)

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
    inlines= [MaintenanceActionInline]

# @admin.register(MaintenanceAction)
# class MaintenanceActionAdmin(admin.ModelAdmin):
#     list_display = (
#         'device',
#         'hardware',
#         'action_date',
#         'contractor'
#     )
#     search_fields = (
#         'device__type__name',
#         'hardware__modelName',
#         'contractor__full_name'
#     )
#     list_filter = ['contractor']
#     readonly_fields = ('action_date',)
#     fields = (
#         'device',
#         'hardware',
#         'description',
#         'contractor',
#         'action_date',
#     )
