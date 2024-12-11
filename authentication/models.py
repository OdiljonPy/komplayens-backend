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
    full_name = models.CharField(max_length=250)
    username = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=14)
    login_time = models.DateTimeField(null=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']


    def __str__(self):
        return self.username


class Employee(User):
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2)
    organization = models.ForeignKey('services.Organization', null=True, blank=True, on_delete=models.SET_NULL)


# class User(BaseUser):
#     pass