from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from Test.models import (Application,
                         ApplicationSubject,
                         ApplicationActions,
                         ApplicationStatusHistory,
                         ApplicationSLA,
                         MaintenanceAction)

# Переопределённая форма изменения\создания заявки
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application  # Указываем модель формы
        fields = '__all__'  # Используем все поля модели

class ApplicationSubjectForm(forms.ModelForm):
    class Meta:
        model = ApplicationSubject  # Указываем модель формы
        fields = ['device']  # Поля формы

    def clean_device(self):
        device = self.cleaned_data.get('device')
        if not device:
            raise forms.ValidationError('Необходимо выбрать устройство.')
        return device

# Переопределённая форма изменения\создания истории статусов заявки
class ApplicationStatusHistoryForm(forms.ModelForm):
    class Meta:
        model = ApplicationStatusHistory  # Указываем модель формы
        fields = ['newApplicationStatus']  # Поля формы
        widgets = {
            'newApplicationStatus': forms.Select(attrs={'class': 'vForeignKeySelector'})
        }
        labels = {
            'newApplicationStatus': 'Новый статус'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем пользователя из kwargs
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Если запись уже существует, делаем поля только для чтения
            for field in self.fields.values():
                field.disabled = True

    def save(self, commit=True):
        if self.instance and self.instance.pk:
            # Не сохраняем изменения существующих записей
            return self.instance

        instance = super().save(commit=False)

        if commit:
            try:
                # Получаем предыдущий статус **до** сохранения нового статуса
                previous_status_instance = ApplicationStatusHistory.objects.filter(
                    application=instance.application
                ).order_by('-changeTime', '-pk').first()

                if previous_status_instance:
                    old_status = previous_status_instance.newApplicationStatus.name
                else:
                    old_status = 'Неизвестно'

                # Сохраняем текущую запись
                instance.save()

                # Получаем новый статус после сохранения
                new_status = instance.newApplicationStatus.name

                # Обновление дат SLA
                sla = instance.application.applicationsla_set.first()
                if new_status == 'В работе' and sla and sla.acceptanceDate is None:
                    sla.acceptanceDate = timezone.now().date()
                    sla.save()
                elif new_status == 'Закрыта' and sla and sla.completionDate is None:
                    sla.completionDate = timezone.now().date()
                    sla.save()

                # Определяем имя пользователя
                username = self.user.username if self.user else 'Система'

                # Создание действия по заявке
                ApplicationActions.objects.create(
                    application=instance.application,
                    content=f"Статус заявки изменён {username} с {old_status} на {new_status}"
                )
            except Exception as e:
                raise ValidationError(f"Ошибка при сохранении статуса заявки: {e}")

        return instance

# Кастомная форма для ApplicationSLA
class ApplicationSLAForm(forms.ModelForm):
    class Meta:
        model = ApplicationSLA  # Указываем модель формы
        fields = ['priority', 'creationDate', 'acceptanceDate', 'completionDate']  # Поля формы

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем пользователя из kwargs
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        creation_date = cleaned_data.get('creationDate')  # Получаем дату создания
        acceptance_date = cleaned_data.get('acceptanceDate')  # Получаем дату принятия
        completion_date = cleaned_data.get('completionDate')  # Получаем дату завершения

        if acceptance_date and creation_date and acceptance_date < creation_date:
            raise forms.ValidationError('Дата принятия не может быть раньше даты создания.')  # Проверка дат

        if completion_date and acceptance_date and completion_date < acceptance_date:
            raise forms.ValidationError('Дата завершения не может быть раньше даты принятия.')  # Проверка дат

        return cleaned_data  # Возвращаем очищенные данные

    def save(self, commit=True):
        instance = super().save(commit=False)  # Получаем объект без сохранения
        if not self.instance.pk:
            # При создании заявки установить дату создания SLA
            instance.creationDate = timezone.now().date()  # Устанавливаем текущую дату создания
        if self.instance.pk:
            # При изменении приоритета заявки
            previous = ApplicationSLA.objects.get(pk=self.instance.pk)  # Получаем предыдущий объект SLA
            if previous.priority != instance.priority:
                # Создаём запись в действиях по заявке при изменении приоритета
                ApplicationActions.objects.create(
                    application=instance.application,
                    content=f"{self.user.username} изменил(а) приоритет заявки с {previous.priority.name} на {instance.priority.name}"
                )
        if commit:
            instance.save()  # Сохраняем объект
        return instance  # Возвращаем сохранённый объект

# Форма для действий с оборудованием по заявке
class MaintenanceActionForm(forms.ModelForm):
    class Meta:
        model = MaintenanceAction
        fields = ['device', 'hardware', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }

    def clean(self):
        cleaned_data = super().clean()
        device = cleaned_data.get('device')
        hardware = cleaned_data.get('hardware')

        # Проверяем, что заполнено только одно из полей
        if device and hardware:
            raise ValidationError(
                'Нельзя одновременно выбрать устройство и оборудование. Выберите что-то одно.'
            )

        if not device and not hardware:
            raise ValidationError(
                'Необходимо выбрать либо устройство, либо оборудование.'
            )

        return cleaned_data