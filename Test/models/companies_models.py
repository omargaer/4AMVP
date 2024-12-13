from django.db import models as models
# from django.contrib.gis.db import models as gis_models
# TODO: UniqueConstraint
class CompanyGroup(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Название группы компаний')
    note = models.TextField(blank=True,
                            null=True,
                            default=None,
                            verbose_name='Примечания')
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'CompanyGroup'
        verbose_name = "Группа компаний"
        verbose_name_plural = "Группы компаний"

class Company(models.Model):
    companyGroup = models.ForeignKey(CompanyGroup,
                                     on_delete=models.RESTRICT,
                                     related_name='companies',
                                     null=True,
                                     default=None,
                                     verbose_name="Принадлежит к группе компаний")
    name = models.CharField(max_length=100,
                            null=False,
                            default='',
                            verbose_name="Название")
    ITN = models.CharField(max_length=10,
                           null=True,
                           default='',
                           verbose_name="ИНН")
    note = models.TextField(blank=True,
                            null=True,
                            default=None,
                            verbose_name="Примечания")
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Company'
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

class Position(models.Model):
    company = models.ForeignKey(Company,
                                on_delete=models.SET_NULL,
                                related_name='positions',
                                null=True,
                                verbose_name="Должности в компании",
                                default=None)
    name = models.CharField(max_length=30,
                            null=False,
                            default='',
                            verbose_name='Название должности')
    note = models.TextField(blank=True,
                            null=True,
                            default='',
                            verbose_name='Примечания')
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Position'
        verbose_name = "Должность в компании"
        verbose_name_plural = "Должности компании"

#region Филиал
class BranchOfficeType(models.Model):
    name = models.CharField(max_length=30,
                            null=False,
                            default='',
                            verbose_name="Название типа филиала")
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'BranchOfficeType'
        verbose_name = "Тип филиала"
        verbose_name_plural = "Типы филиалов"

class BranchOfficeStatus(models.Model):
    name = models.CharField(max_length=30,
                            null=False,
                            default='',
                            verbose_name="Название статуса филиала")
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'BranchOfficeStatus'
        verbose_name = "Статус филиала"
        verbose_name_plural = "Статусы филиалов"

class BranchOffice(models.Model):
    company = models.ForeignKey(Company,
                                on_delete=models.RESTRICT,
                                related_name='branches',
                                null=False,
                                default=None,
                                verbose_name="Компания")
    type = models.ForeignKey(BranchOfficeType,
                             on_delete=models.RESTRICT,
                             null=False,
                             default=None,
                             verbose_name="Тип филиала")
    status = models.ForeignKey(BranchOfficeStatus,
                               on_delete=models.RESTRICT,
                               null=True,
                               default=None,
                               verbose_name="Статус филиала")
    phone = models.CharField(max_length=11,
                             null=True,
                             default=None,
                             verbose_name="Телефон филиала")
    note = models.TextField(blank=True,
                            null=True,
                            default=None,
                            verbose_name="Примечания")
    def __str__(self):
        return (self.company.name + " "
                + self.type.name + " "
                + self.status.name)

    class Meta:
        db_table = 'BranchOffice'
        verbose_name = "Филиал компании"
        verbose_name_plural = "Филиалы компании"

class BranchOfficeLocation(models.Model):
    branchOffice = models.ForeignKey(BranchOffice,
                                     on_delete=models.RESTRICT,
                                     null=False,
                                     default=None,
                                     related_name='locations',
                                     verbose_name="Локация филиала")
    # TODO: потом как-нибудь
    # location = gis_models.PointField(geography=True,
    #                                  null=True,
    #                                  default=None,
    #                                  blank=True,
    #                                  verbose_name="Местоположение")
    street = models.CharField(max_length=20,
                                  null=False,
                                  default='',
                                  verbose_name="Улица")
    building = models.CharField(max_length=20,
                                null=False,
                                default='',
                                verbose_name="Строение\здание")
    floor = models.IntegerField(null=True,
                                verbose_name="Этаж",
                                default=0)
    room = models.CharField(max_length=5,
                            null=False,
                            default='',
                            verbose_name="Помещение")
    def __str__(self):
        return (self.branchOffice.__str__() + " "
                + self.street)

    class Meta:
        db_table = 'BranchOfficeLocation'
        verbose_name = "Адрес филиала"
        verbose_name_plural = "Адреса филиала"

class BranchOfficeSchedule(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ]
    branchOffice = models.ForeignKey(BranchOffice,
                                     on_delete=models.RESTRICT,
                                     related_name='schedules',
                                     verbose_name="Филиал")
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK,
                                      verbose_name="День недели")
    opening_time = models.TimeField(verbose_name="Время открытия")
    closing_time = models.TimeField(verbose_name="Время закрытия")

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.opening_time} - {self.closing_time}"

    class Meta:
        db_table = 'BranchOfficeSchedule'
        verbose_name = "Расписание филиала"
        verbose_name_plural = "Расписания филиалов"
        unique_together = ('branchOffice', 'day_of_week')


#endregion Филиал