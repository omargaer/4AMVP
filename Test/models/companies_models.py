from django.db import models


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
                            verbose_name="Название")
    ITN = models.CharField(max_length=10,
                           verbose_name="ИНН")
    note = models.TextField(blank=True,
                            null=True,
                            default=None,
                            verbose_name="Примечания")
    def __str__(self):
        return self.name

    class Meta:
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
                            verbose_name='Название должности')
    note = models.TextField(blank=True,
                            null=True,
                            default=None,
                            verbose_name='Примечания')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Должность в компании"
        verbose_name_plural = "Должности компании"

class BranchOfficeType(models.Model):
    name = models.CharField(max_length=30,
                            null=False,
                            verbose_name="Название типа филиала")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип филиала"
        verbose_name_plural = "Типы филиалов"

class BranchOfficeStatus(models.Model):
    name = models.CharField(max_length=30,
                            null=False,
                            verbose_name="Название статуса филиала")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус филиала"
        verbose_name_plural = "Статусы филиалов"

class BranchOffice(models.Model):
    company = models.ForeignKey(Company,
                                on_delete=models.RESTRICT,
                                related_name='branches',
                                null=False,
                                verbose_name="Принадлежит к компании")
    type = models.ForeignKey(BranchOfficeType,
                             on_delete=models.RESTRICT,
                             null=False,
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
        verbose_name = "Филиал компании"
        verbose_name_plural = "Филиалы компании"