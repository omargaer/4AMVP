from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.db.models import Q

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
    name = models.CharField(max_length=40,
                            null=False,
                            blank=False,
                            default="",
                            verbose_name="Модель")
    responsiblePerson = models.ForeignKey('IndividualEntity',
                                          on_delete=models.RESTRICT,
                                          null=True,
                                          default=None,
                                          blank=True,
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
                                  blank=True,
                                  verbose_name="Метод размещения")
    inventoryNumber = models.CharField(max_length=20,
                                       null=True,
                                       default=None,
                                       blank=True,
                                       verbose_name="Инвентарный номер")
    factoryNumber = models.CharField(max_length=20,
                                     null=True,
                                     default=None,
                                     blank=True,
                                     verbose_name="Заводской номер")
    purchaseDate = models.DateField(null=True,
                                    default=None,
                                    blank=True,
                                    verbose_name='Дата покупки')
    warrantyExpirationDate = models.DateField(null=True,
                                              default=None,
                                              blank=True,
                                              verbose_name='Дата окончания гарантии')
    def __str__(self):
        return self.type.name + " " + str(self.inventoryNumber)

    class Meta:
        db_table = 'Device'
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


class SoftwareType(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            verbose_name='Тип программного обеспечения')
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'SoftwareType'
        verbose_name = 'Тип программного обеспечения'
        verbose_name_plural = 'Типы программного обеспечения'

class Software(models.Model):
    device = models.ForeignKey(Device,
                               on_delete=models.RESTRICT,
                               null=False,
                               default=None,
                               related_name='software',
                               verbose_name='Оборудование')
    type = models.ForeignKey(SoftwareType,
                             on_delete=models.RESTRICT,
                             null=False,
                             default=None,
                             verbose_name='Тип ПО')
    name = models.CharField(max_length=20,
                            null=False,
                            verbose_name='Название программного обеспечения')
    price = models.DecimalField(decimal_places=2,
                                max_digits=15,
                                null=True,
                                default=None,
                                verbose_name='Закупочная цена')
    license_key = models.CharField(max_length=200,
                                   null=True,
                                   default=None,
                                   blank=True,
                                   verbose_name='Лицензионный ключ')
    purchaseDate = models.DateField(null=True,
                                    default=None,
                                    blank=True,
                                    verbose_name='Дата покупки')
    installationDate = models.DateField(null=True,
                                        default=None,
                                        blank=True,
                                        verbose_name='Дата установки')
    licenseActivationDate = models.DateField(null=True,
                                             default=None,
                                             blank=True,
                                             verbose_name='Дата активации лицензии')
    licenseExpirationDate = models.DateField(null=True,
                                             default=None,
                                             blank=True,
                                             verbose_name='Дата окончания лицензии')
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Software'
        verbose_name = "Программное обеспечение"
        verbose_name_plural = "Программное обеспечение"

class HardwareType(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            verbose_name="Тип аппаратного обеспечения")
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'HardwareType'
        verbose_name = 'Тип аппаратного обеспечения'
        verbose_name_plural = 'Типы аппаратного обеспечения'

class Hardware(models.Model):
    device = models.ForeignKey(Device,
                               on_delete=models.RESTRICT,
                               null=True,
                               default=None,
                               related_name='hardware',
                               verbose_name='Оборудование')
    type = models.ForeignKey(HardwareType,
                             on_delete=models.RESTRICT,
                             null=False,
                             verbose_name='Тип аппаратного обеспечения')
    modelName = models.CharField(max_length=30,
                                 null=True,
                                 default='',
                                 verbose_name="Модель")
    price = models.DecimalField(decimal_places=2,
                                max_digits=15,
                                null=True,
                                default=None,
                                verbose_name='Закупочная цена')
    inventoryNumber = models.CharField(max_length=20,
                                       null=True,
                                       default=None,
                                       blank=True,
                                       verbose_name="Инвентарный номер")
    factoryNumber = models.CharField(max_length=20,
                                     null=True,
                                     default=None,
                                     blank=True,
                                     verbose_name="Заводской номер")
    purchaseDate = models.DateField(null=True,
                                    default=None,
                                    verbose_name='Дата покупки')
    installationDate = models.DateField(null=True,
                                        default=None,
                                        verbose_name='Дата установки')
    warrantyExpirationDate = models.DateField(null=True,
                                              default=None,
                                              verbose_name='Дата окончания гарантии')
    def __str__(self):
        return self.type.name + " " + self.modelName

    class Meta:
        db_table = 'Hardware'
        verbose_name = 'Аппаратное обеспечение'
        verbose_name_plural = 'Аппаратное обеспечение'

class MaintenanceAction(models.Model):
    device = models.ForeignKey(Device,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name="maintenance_actions",
                               verbose_name="Оборудование")
    hardware = models.ForeignKey(Hardware,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name="maintenance_actions",
                                 verbose_name="Аппаратное обеспечение")
    description = models.CharField(max_length=200,
                                   null=True,
                                   blank=True,
                                   verbose_name="Описание действия")
    action_date = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Дата выполнения действия")
    contractor = models.ForeignKey('IndividualEntity',
                                   on_delete=models.RESTRICT,
                                   null=True,
                                   verbose_name="Исполнитель",
                                   related_name="maintenance_actions")
    application = models.ForeignKey('Application',
                                     on_delete=models.RESTRICT,
                                     verbose_name="Заявка",
                                     null=False,
                                     default=None,
                                     related_name="application_maintenance_actions")
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                        Q(device__isnull=False, hardware__isnull=True) |
                        Q(device__isnull=True, hardware__isnull=False)
                ),
                name="device_or_hardware_only"
            )
        ]
        db_table = 'MaintenanceAction'
        verbose_name = 'Действие по ремонту и обслуживанию'
        verbose_name_plural = 'Действия по ремонту и обслуживанию'


    def __str__(self):
        target = self.device or self.hardware
        return f"{self.action_date} - {target}"