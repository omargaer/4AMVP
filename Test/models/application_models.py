from django.db import models
from django.utils import timezone
from Test.models import Device


class ApplicationType(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            verbose_name='Тип заявки')
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ApplicationType'
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Типы заявки'

class Application(models.Model):
    shortDescription = models.CharField(null=False,
                               default='',
                               max_length=100,
                               verbose_name='Тема обращения')
    content = models.TextField(null=False,
                               blank=False,
                               verbose_name='Содержимое заявки')
    applicationType = models.ForeignKey(ApplicationType,
                                        on_delete=models.RESTRICT,
                                        null=False,
                                        default=None,
                                        verbose_name="Тип заявки")
    company = models.ForeignKey('Company',
                                on_delete=models.CASCADE,
                                verbose_name="Компания",
                                null=False)
    branch_office = models.ForeignKey('BranchOffice',
                                      on_delete=models.CASCADE,
                                      verbose_name="Филиал",
                                      null=False)
    location = models.ForeignKey('BranchOfficeLocation',
                                 on_delete=models.CASCADE,
                                 verbose_name="Помещение",
                                 null=False)
    applicant = models.ForeignKey('IndividualEntity',
                                  on_delete=models.RESTRICT,
                                  null=False,
                                  default=None,
                                  related_name='open_applications',
                                  verbose_name='Заявитель')
    contractor = models.ForeignKey('IndividualEntity',
                                   on_delete=models.RESTRICT,
                                   null=False,
                                   default=None,
                                   related_name='applications',
                                   verbose_name='Исполнитель')
    device = models.ManyToManyField('Device',
                                    through='ApplicationSubject',
                                    related_name='applications',
                                    verbose_name='Оборудование по заявке')
    status = models.ManyToManyField('ApplicationStatus',
                                    through='ApplicationStatusHistory',
                                    related_name='applications',
                                    verbose_name='Статусы заявки')
    def __str__(self):
        return self.location.__str__() + " " + self.shortDescription

    def save(self, *args, **kwargs):
        # Определяем, является ли объект новым
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Создаём действие "Заявка создана"
            ApplicationActions.objects.create(
                application=self,
                content="Заявка создана"
            )
            try:
                # Получаем или создаём статус 'Новая'
                new_status, created = ApplicationStatus.objects.get_or_create(name='Новая')
                # Создаём запись в истории статусов
                ApplicationStatusHistory.objects.create(
                    application=self,
                    newApplicationStatus=new_status,
                    changeTime=timezone.now()
                )
                # Получаем или создаём приоритет 'Средний'
                medium_priority, created = ApplicationPriority.objects.get_or_create(name='Средний')
                # Создаём SLA с приоритетом 'Средний' и текущей датой создания
                ApplicationSLA.objects.create(
                    application=self,  # Связываем с текущей заявкой
                    priority=medium_priority,  # Устанавливаем приоритет 'Средний'
                    creationDate=timezone.now().date()  # Устанавливаем текущую дату создания
                )
            except Exception as e:
                # Обработка ошибок (например, логирование)
                pass  # Можно заменить на логирование ошибки

    class Meta:
        db_table = 'Application'
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

class ApplicationSubject(models.Model):
    application = models.ForeignKey(Application,
                                    on_delete=models.RESTRICT,
                                    null=False,
                                    verbose_name='Заявка')
    device = models.ForeignKey('Device',
                               on_delete=models.RESTRICT,
                               null=False,
                               verbose_name='Оборудование')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['application', 'device'], name='unique_application_device')
        ]
        db_table = 'ApplicationsSubjects'
        verbose_name = 'Предмет заявки'
        verbose_name_plural = 'Предметы заявки'

class ApplicationPriority(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            default='',
                            verbose_name='Название приоритета')
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ApplicationPriority'
        verbose_name = 'Приоритет заявки'
        verbose_name_plural = 'Приоритеты заявки'

class ApplicationSLA(models.Model):
    application = models.ForeignKey(Application,
                                    on_delete=models.RESTRICT,
                                    null=False,
                                    default=None,
                                    verbose_name='Заявка')
    priority = models.ForeignKey(ApplicationPriority,
                                 on_delete=models.RESTRICT,
                                 null=False,
                                 default=None,
                                 verbose_name='Приоритет')
    creationDate = models.DateField(null=True,
                                    verbose_name='Дата создания')
    acceptanceDate = models.DateField(null=True,
                                      verbose_name='Дата принятия')
    completionDate = models.DateField(null=True,
                                      verbose_name='Дата закрытия')
    class Meta:
        db_table = 'ApplicationSLA'
        verbose_name = 'SLA заявки'
        verbose_name_plural = 'SLA заявки'

    def __str__(self):
        return f"SLA для заявки {self.application.shortDescription}"

class ApplicationStatus(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name='Статус заявки')
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ApplicationStatus'
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявки'

class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey('Application',
                                    on_delete=models.RESTRICT,
                                    null=False,
                                    default=None,
                                    verbose_name='Заявка')
    changeTime = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата и время изменения')
    newApplicationStatus = models.ForeignKey(ApplicationStatus,
                                             on_delete=models.RESTRICT,
                                             default=None,
                                             verbose_name='Новый статус')
    class Meta:
        db_table = 'ApplicationStatusHistory'
        verbose_name = 'История изменения статусов заявки'
        verbose_name_plural = 'Истории изменения статусов заявок'

class ApplicationActions(models.Model):
    application = models.ForeignKey(Application,
                                    on_delete=models.RESTRICT,
                                    null=False,
                                    default=None,
                                    verbose_name='Заявка')
    timestamp = models.DateTimeField(null=False,
                                     verbose_name='Дата и время действия',
                                     auto_now_add=True)
    content = models.CharField(max_length=300,
                               null=False,
                               blank=False,
                               default='',
                               verbose_name='Описание действия')

    def __str__(self):
        return self.application.__str__() + " " + self.timestamp.__str__()

    class Meta:
        db_table = 'ApplicationActions'
        verbose_name = 'Действие по заявке'
        verbose_name_plural = 'Действия по заявке'

class ApplicationFiles(models.Model):
    application = models.ForeignKey(Application,
                                    on_delete=models.RESTRICT,
                                    null=False,
                                    default=None,
                                    verbose_name='Заявка')
    file = models.FileField(null=False,
                            default='',
                            verbose_name='Файл в заявке')
    def __str__(self):
        return self.application.__str__() + " " + self.file.name

    class Meta:
        db_table = 'ApplicationFiles'
        verbose_name = 'Файл в заявке'
        verbose_name_plural = 'Файлы в заявке'

class ApplicationMessages(models.Model):
    application = models.ForeignKey(Application,
                                    on_delete=models.RESTRICT,
                                    null=False,
                                    default=None,
                                    verbose_name='Заявка')
    sender = models.ForeignKey('Account',
                               on_delete=models.RESTRICT,
                               null=False,
                               default=None,
                               verbose_name='Отправитель')
    timestamp = models.DateTimeField(null=False,
                                     default=None,
                                     verbose_name='Время отправления')
    content = models.TextField(null=False,
                               blank=False,
                               default='',
                               verbose_name='Содержимое сообщения')

    def __str__(self):
        return self.application.__str__() + " " + self.sender.__str__() + " " + self.timestamp.__str__()

    class Meta:
        db_table = 'ApplicationMessages'
        verbose_name = 'Сообщение заявки'
        verbose_name_plural = 'Сообщения заявки'
