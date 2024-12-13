from django.db import models
from abstarct_model.base_model import BaseModel

ROLE_CHOICES = (
    (1, 'SuperAdmin'),
    (2, 'Admin'),
    (3, 'Officer'),
    (4, 'Employee'),
)


class User(BaseModel):
    first_name = models.CharField(max_length=80, verbose_name='Имя')
    last_name = models.CharField(max_length=80, verbose_name='Фамилия')
    username = models.CharField(max_length=250, unique=True, verbose_name="Имя пользователя")
    password = models.CharField(max_length=250, verbose_name="Пароль")
    phone_number = models.CharField(max_length=14, verbose_name="Номер телефона")
    organization = models.ForeignKey(
        to='services.Organization', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Организация")
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2, verbose_name="Роль")
    login_time = models.DateTimeField(null=True, verbose_name="Время входа")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-created_at',)
