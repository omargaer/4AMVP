from django.db import models
from django.contrib.auth.models import AbstractUser

class IndividualEntity(models.Model):
    full_name = models.CharField(max_length=50,
                                 verbose_name='ФИО')

    # СНИЛС
    INIPA = models.CharField(max_length=11,
                             verbose_name="Снилс",
                             null=True,
                             blank=True,
                             default='')
    # ИНН
    ITN = models.CharField(max_length=12,
                           null=True,
                           default='',
                           blank=True,
                           verbose_name="ИНН")
    GENDERS = [(0, 'Мужчина'),
               (1, 'Женщина'),
               (2, 'Не указан')]
    gender = models.IntegerField(choices=GENDERS,
                                 verbose_name="Пол",
                                 null=True,
                                 blank=True,
                                 default=2)
    workplaces = models.ManyToManyField('BranchOffice',
                                        through='BranchOfficeEmployees',
                                        related_name='individual_entities',
                                        verbose_name='Филиалы')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'IndividualEntity'
        verbose_name = "Физическое лицо"
        verbose_name_plural = "Физические лица"

class AccountStatus(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            default='',
                            verbose_name="Название статуса")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'AccountStatus'
        verbose_name = "Статус учётной записи"
        verbose_name_plural = "Статусы учётной записи"


class AccountRole(models.Model):
    name = models.CharField(max_length=25,
                            null=False,
                            default='',
                            verbose_name="Название роли")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'AccountRole'
        verbose_name = "Роль учётной записи"
        verbose_name_plural = "Роли учётной записи"


class Account(AbstractUser):
    first_name = None
    last_name = None
    # username, password наследуются от AbstractUser
    individual_entity = models.ForeignKey(IndividualEntity,
                                   null=True,
                                   default=None,
                                   on_delete=models.RESTRICT,
                                   verbose_name="Связанное физическое лицо",
                                   related_name='accounts')
    status = models.ForeignKey(AccountStatus,
                               on_delete=models.RESTRICT,
                               # TODO: потом изменить
                               null=True,
                               default=None,
                               verbose_name="Статус")
    role = models.ForeignKey(AccountRole,
                             on_delete=models.RESTRICT,
                             # TODO: потом изменить
                             null=True,
                             default=None,
                             verbose_name="Роль")
    phone = models.CharField(max_length=12,
                             null=True,
                             default="",
                             verbose_name="Телефон")
    note = models.CharField(max_length=120,
                            blank=True,
                            null=True,
                            default=None,
                            verbose_name="Примечания")
    branchOffice = models.ManyToManyField('BranchOffice',
                                        through='BranchOfficeAccounts',
                                        related_name='accounts',
                                        verbose_name='Филиал')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='account_groups',
        blank=True,
        verbose_name='Группы'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='account_permissions',
        blank=True,
        verbose_name='Пользовательские разрешения'
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Account'
        verbose_name = "Учётная запись"
        verbose_name_plural = "Учётные записи"

