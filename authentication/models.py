from uuid import uuid4
from django.db import models
from abstarct_model.base_model import BaseModel
from .utils import phone_number_validation

ROLE_CHOICES = (
    (1, 'SuperAdmin'),
    (2, 'Admin'),
    (3, 'Officer'),
)

OFFICER_REQUEST_STATUS = (
    (1, 'Waiting'),
    (2, 'Approved'),
    (3, 'Rejected'),
)

USER_ACTIVE_STATUS = (
    (1, 'Active'),
    (2, 'Block'),
)


class User(BaseModel):
    first_name = models.CharField(max_length=80, verbose_name='Имя')
    last_name = models.CharField(max_length=80, verbose_name='Фамилия')
    password = models.CharField(max_length=250, verbose_name="Пароль")
    phone_number = models.CharField(max_length=14, verbose_name="Номер телефона", validators=[phone_number_validation])
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3, verbose_name="Роль")
    organization = models.ForeignKey(to='services.Organization', on_delete=models.SET_NULL, null=True)
    login_time = models.DateTimeField(null=True, blank=True, verbose_name="Время входа")
    status = models.IntegerField(choices=OFFICER_REQUEST_STATUS, default=1, verbose_name='Статус')
    is_active = models.IntegerField(choices=USER_ACTIVE_STATUS, default=1)

    def __str__(self):
        return f"{self.first_name} - {self.id}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-created_at',)


class OTP(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_key = models.UUIDField(default=uuid4)
    otp_code = models.IntegerField()
    request_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'ОТП'
        verbose_name_plural = 'ОТП'
        ordering = ('-created_at',)


class Customer(BaseModel):
    user_agent = models.CharField(max_length=220, verbose_name='Пользовательский агент')
    ip_address = models.CharField(max_length=15, verbose_name='IP-адрес')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('-created_at',)
