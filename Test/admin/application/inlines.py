from django.contrib import admin
from Test.models import (ApplicationActions,
                         ApplicationSubject,
                         ApplicationStatusHistory,
                         ApplicationSLA,
                         ApplicationFiles,
                         ApplicationMessages)
from Test.forms import (ApplicationSubjectForm,
                       ApplicationStatusHistoryForm,
                       ApplicationSLAForm)

# Действия
class ApplicationActionsInline(admin.TabularInline):
    model = ApplicationActions
    fields = ('timestamp', 'content')
    readonly_fields = ('timestamp',)
    can_delete = False
    show_change_link = False
    verbose_name = 'Действие заявки'
    verbose_name_plural = 'Действия заявки'
    extra = 0

# Предметы
class ApplicationSubjectInline(admin.TabularInline):
    model = ApplicationSubject  # Указываем модель для инлайна
    form = ApplicationSubjectForm  # Указываем кастомную форму
    extra = 0  # Количество дополнительных пустых форм
    fields = ('device',)  # Поля, отображаемые в инлайне
    can_delete = False

# Статусы
class ApplicationStatusHistoryInline(admin.TabularInline):
    model = ApplicationStatusHistory
    form = ApplicationStatusHistoryForm  # Используем кастомную форму
    extra = 1  # Позволяет добавить одну новую запись
    verbose_name = 'История статуса заявки'
    verbose_name_plural = 'Истории статусов заявок'
    readonly_fields = ('changeTime',)  # Поле даты и времени только для чтения
    can_delete = False  # Запрещаем удаление записей

    def get_queryset(self, request):
        """Отображаем все записи истории статусов, отсортированные по времени изменения."""
        qs = super().get_queryset(request)
        return qs.order_by('changeTime')

# SLA
class ApplicationSLAInline(admin.TabularInline):
    model = ApplicationSLA  # Указываем модель для инлайна
    form = ApplicationSLAForm  # Указываем кастомную форму
    extra = 0  # Убираем дополнительные пустые формы
    max_num = 1  # Ограничиваем до одной записи
    can_delete = False  # Запрещаем удаление SLA
    readonly_fields = ('creationDate', 'acceptanceDate', 'completionDate')  # Делаем поля даты только для чтения
    verbose_name = 'SLA заявки'  # Имя для единственного числа
    verbose_name_plural = 'SLA заявки'  # Имя для множественного числа
    fields = ('priority', 'creationDate', 'acceptanceDate', 'completionDate')  # Поля, отображаемые в инлайне

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)  # Получаем стандартный formset
        class FormSet(formset):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)  # Инициализируем родительский класс
                for form in self.forms:
                    form.user = request.user  # Устанавливаем пользователя для каждой формы
        return FormSet  # Возвращаем кастомный formset

# Сообщения
class ApplicationMessagesInline(admin.TabularInline):
    model = ApplicationMessages
    fields = ('sender', 'timestamp', 'content')
    readonly_fields = ('sender', 'timestamp')
    can_delete = False
    show_change_link = False
    verbose_name = 'Сообщение заявки'
    verbose_name_plural = 'Сообщения заявки'
    extra = 0

# Файлы
class ApplicationFilesInline(admin.TabularInline):
    model = ApplicationFiles
    fields = ('file',)
    readonly_fields = ('file',)
    can_delete = False
    show_change_link = False
    verbose_name = 'Файл заявки'
    verbose_name_plural = 'Файлы заявки'
    extra = 0
