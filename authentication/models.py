from tabnanny import verbose

from django.db import models
from abstarct_model.base_model import BaseModel

# from services.models import Organization

ROLE_CHOICES = (
    (0, 'SuperAdmin'),
    (1, 'Admin'),
    (2, 'Staff'),
)


class User(BaseModel):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=250, verbose_name="Полное имя")
    username = models.CharField(max_length=250, unique=True, verbose_name="Имя пользователя")
    password = models.CharField(max_length=250, verbose_name="Пароль")
    phone_number = models.CharField(max_length=14, verbose_name="Номер телефона")
    login_time = models.DateTimeField(null=True, verbose_name="Время входа")


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-created_at',)


class Employee(User):
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2, verbose_name="Роль")
    organization = models.ForeignKey('services.Organization', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Организация")

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ('-created_at',)

# class User(BaseUser):
#     pass