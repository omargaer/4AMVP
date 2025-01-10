from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Test.models import BranchOfficeEmployees
from Test.models.user_models import (
    IndividualEntity,
    AccountStatus,
    AccountRole,
    Account
)

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

# class BranchOfficeEmployeesInline(admin.TabularInline):
#     model = BranchOfficeEmployees
#     extra = 1
#     autocomplete_fields = ['branchOffice']
#     verbose_name = 'Филиал сотрудника'
#     verbose_name_plural = 'Филиалы сотрудников'

@admin.register(Account)
class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('username', 'status', 'role')
    list_filter = ('status', 'role', 'groups')
    search_fields = ('username', )
    ordering = ('username',)

    # Переопределение fieldsets без first_name и last_name
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Дополнительные поля', {
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

    # Переопределение add_fieldsets без first_name и last_name
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                'individual_entity',
                'position',
                'status',
                'role',
                'phone',
                'note',
            ),
        }),
    )
    #inlines = [BranchOfficeEmployeesInline]