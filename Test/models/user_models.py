from django.db import models
from django.contrib.auth.models import AbstractUser

class IndividualEntity(models.Model):
    full_name = models.CharField(max_length=50,
                                 verbose_name='ФИО')
    # TODO: потом как-нибудь
    # photo = models.ImageField(verbose_name='Аватарка')

    # СНИЛС
    INIPA = models.CharField(max_length=11,
                             verbose_name="Снилс",
                             null=True,
                             default='')
    # ИНН
    ITN = models.CharField(max_length=10,
                           null=True,
                           default='',
                           verbose_name="ИНН")
    GENDERS = [(0, 'Мужчина'),
               (1, 'Женщина'),
               (2, 'Не указан')]
    gender = models.IntegerField(choices=GENDERS,
                                 verbose_name="Пол",
                                 null=False,
                                 default=2)

    def __str__(self):
        return (self.full_name + " " +
                self.INIPA)

    class Meta:
        db_table = 'IndividualEntity'
        verbose_name = "Физическое лицо"
        verbose_name_plural = "Физические лица"

class Account(AbstractUser):
    # username, password наследуются от AbstractUser
    individual = models.ForeignKey(IndividualEntity,
                                   null=True,
                                   default=None,
                                   on_delete=models.RESTRICT,
                                   verbose_name="Связанное физическое лицо",
                                   related_name='accounts')
    email = models.CharField(max_length=40,
                             null=True,
                             default="",
                             verbose_name="Электронная почта")
    phone = models.CharField(max_length=12,
                             null=True,
                             default="",
                             verbose_name="Телефон")
    position = models.ForeignKey('Position',
                                 on_delete=models.RESTRICT,
                                 null=True,
                                 default=None,
                                 verbose_name="Должность")
    note = models.TextField(blank=True,
                            null=True,
                            default=None,
                            verbose_name="Примечания")
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
