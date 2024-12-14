from django.contrib.auth.tokens import default_token_generator
from django.db import models

from Test.models import BranchOfficeLocation


class DeviceType(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'DeviceType'
        verbose_name = "Тип оборудования"
        verbose_name_plural = "Типы оборудования"

class DevicePlacementMethod(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'DevicePlacementType'
        verbose_name = "Тип размещения оборудования"
        verbose_name_plural = "Типы размещения оборудования"

class Device(models.Model):
    responsiblePerson = models.ForeignKey('IndividualEntity',
                                          on_delete=models.RESTRICT,
                                          null=True,
                                          default=None,
                                          related_name='devices',
                                          verbose_name="Ответственное лицо")
    branchOfficeLocation = models.ForeignKey(BranchOfficeLocation,
                                             on_delete=models.RESTRICT,
                                             null=False,
                                             default=None,
                                             related_name='devices',
                                             verbose_name="Локация")
    type = models.ForeignKey(DeviceType,
                             on_delete=models.RESTRICT,
                             null=False,
                             verbose_name="Тип оборудования")
    placement = models.ForeignKey(DevicePlacementMethod,
                                  on_delete=models.RESTRICT,
                                  null=True,
                                  verbose_name="Метод размещения")
    inventoryNumber = models.CharField(max_length=20,
                                       null=True,
                                       default=None,
                                       verbose_name="Инвентарный номер")
    factoryNumber = models.CharField(max_length=20,
                                     null=True,
                                     default=None,
                                     verbose_name="Заводской номер")
    def __str__(self):
        return self.type.name + " " + self.inventoryNumber

    class Meta:
        db_table = 'Device'
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"


class SoftwareType(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            verbose_name="Тип программного обеспечения")
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'SoftwareType'
        verbose_name = "Тип программного обеспечения"
        verbose_name_plural = "Типы программного обеспечения"

class Software(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            verbose_name="Название программного обеспечения")
    price = models.DecimalField(decimal_places=2,
                                max_digits=15,
                                null=True,
                                default=None,
                                verbose_name="Закупочная цена")
    license_key = models.CharField(max_length=200,
                                   null=True,
                                   default=None,
                                   verbose_name="Лицензионный ключ")
    purchaseDate = models.DateField(null=True,
                                    default=None,
                                    verbose_name="Дата покупки")
    licenseActivationDate = models.DateField(null=True,
                                             default=None,
                                             verbose_name="Дата активации лицензии")
    licenseExpirationDate = models.DateField(null=True,
                                             default=None,
                                             verbose_name="Дата окончания лицензии")
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Software'
        verbose_name = "Программное обеспечение"
        verbose_name_plural = "Программное обеспечение"
