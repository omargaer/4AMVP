from django.db import models

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
    address = models.ForeignKey('BranchOfficeLocation',
                                on_delete=models.RESTRICT,
                                null=False,
                                default=None,
                                related_name='applications',
                                verbose_name='Адрес')
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
    device = models.ManyToManyField(Device,
                                    through='ApplicationSubject',
                                    related_name='applications',
                                    verbose_name='Оборудование по заявке')
    def __str__(self):
        # TODO: переделать после
        return self.address.__str__() + " " + self.shortDescription

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
    creationDate = models.DateField(null=False,
                                    verbose_name='Дата создания')
    acceptanceDate = models.DateField(null=False,
                                      verbose_name='Дата принятия')
    completionDate = models.DateField(null=False,
                                      verbose_name='Дата закрытия')
    class Meta:
        db_table = 'ApplicationSLA'
        verbose_name = 'SLA заявки'
        verbose_name_plural = 'SLA заявки'

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
    application = models.ForeignKey(Application,
                                    on_delete=models.RESTRICT,
                                    null=False,
                                    default=None,
                                    verbose_name='Заявка')
    changeTime = models.DateTimeField(null=False,
                                      default=None,
                                      verbose_name='Дата и время изменения')
    newApplicationStatus = models.ForeignKey(ApplicationStatus,
                                             on_delete=models.RESTRICT,
                                             default=None,
                                             verbose_name='Новый статус')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['application'], name='unique_application_status_history')
        ]
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
                                     default=None,
                                     verbose_name='Дата и время действия')
    content = models.TextField(null=False,
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
