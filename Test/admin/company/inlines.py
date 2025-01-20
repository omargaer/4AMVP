from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.utils.html import format_html

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
    BranchOfficeEmployees,
    BranchOfficeAccounts
)

# region Инлайны группы компаний
class CompanyInline(admin.StackedInline):
    model = Company
    extra = 0
    can_delete = False
    show_change_link = False
    readonly_fields = ('name', 'ITN', 'decisionMaker')
    fields = ('name', 'ITN', 'decisionMaker')

class CompanyGroupDecisionMakerInline(admin.StackedInline):
    model = CompanyGroupDecisionMaker
    extra = 0
    max_num = 1  # Ограничить до одного ЛПР
    verbose_name = 'ЛПР'
    verbose_name_plural = 'ЛПР'
# endregion Инлайны группы компаний

# region Инлайны компаний
class BranchOfficeInline(admin.TabularInline):
    """
    Inline-класс для отображения и редактирования филиалов компании в интерфейсе админки.
    """
    extra = 0
    model = BranchOffice
    fields = ('type', 'status', 'phone', 'street', 'building')


class CompanyDecisionMakerInline(admin.StackedInline):
    model = CompanyDecisionMaker
    extra = 0
    max_num = 1  # Ограничить до одного ЛПР
    verbose_name = 'ЛПР'
    verbose_name_plural = 'ЛПР'

class CompanyPositionInline(admin.TabularInline):
    model = Position
    fields = ('name', 'note')
    extra = 0
    can_delete = False
    verbose_name = 'Должность'
    verbose_name_plural = 'Должности'


# endregion Инлайны компаний

# region Инлайны филиалов

class BranchOfficeLocationInline(admin.TabularInline):
    model = BranchOfficeLocation
    extra = 0
    fields = ('floor', 'room', 'room_name')


class UniqueDayFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        days = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                day = form.cleaned_data.get('day_of_week')
                if day in days:
                    raise ValidationError('Дублирующийся день недели.')
                days.append(day)

class BranchOfficeScheduleForm(forms.ModelForm):
    class Meta:
        model = BranchOfficeSchedule
        fields = ['day_of_week', 'opening_time', 'closing_time']

    def clean(self):
        cleaned_data = super().clean()
        opening_time = cleaned_data.get('opening_time')
        closing_time = cleaned_data.get('closing_time')

        if (opening_time and not closing_time) or (closing_time and not opening_time):
            raise ValidationError('Если указано время открытия, то время закрытия должно также быть указано, и наоборот.')

        return cleaned_data

class BranchOfficeScheduleInline(admin.TabularInline):
    model = BranchOfficeSchedule
    form = BranchOfficeScheduleForm
    extra = 0
    fields = ('day_of_week', 'opening_time', 'closing_time')
    verbose_name = "Расписание"
    verbose_name_plural = "Расписания"
    show_change_link = True
    formset = UniqueDayFormSet
    ordering = ['day_of_week']

class EmployeesInline(admin.TabularInline):
    model = BranchOfficeEmployees
    extra = 0
    fields = ('employee', 'position',)
    verbose_name = 'Работник'
    verbose_name_plural = 'Работники'

    def position(self, obj):
        return obj.position.name

class AccountsInline(admin.TabularInline):
    model = BranchOfficeAccounts
    extra = 0
    verbose_name = 'Аккаунт работника'
    verbose_name_plural = 'Аккаунты работников'
# endregion Инлайны филиалов