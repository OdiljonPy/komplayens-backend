from uuid import uuid4
from django.db import models
from abstarct_model.base_model import BaseModel

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


class User(BaseModel):
    first_name = models.CharField(max_length=80, verbose_name='Имя')
    last_name = models.CharField(max_length=80, verbose_name='Фамилия')
    password = models.CharField(max_length=250, verbose_name="Пароль")
    phone_number = models.CharField(max_length=14, verbose_name="Номер телефона")
    email = models.EmailField(blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3, verbose_name="Роль")
    login_time = models.DateTimeField(null=True, verbose_name="Время входа")
    status = models.IntegerField(choices=OFFICER_REQUEST_STATUS, default=1, verbose_name='Статус')
    is_verify = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-created_at',)


class OTP(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_key = models.UUIDField(default=uuid4)
    otp_code = models.IntegerField()
    count = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ('-created_at',)
