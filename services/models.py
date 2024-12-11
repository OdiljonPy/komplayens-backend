import os
from tinymce.models import HTMLField
from django.db import models

from abstarct_model.base_model import BaseModel
from authentication.models import Employee
from base.models import Region, District
from .utils import validate_file_type_and_size

MEDIA_TYPE_CHOICES = (
    ('PDF', 'PDF'),
    ('MP4', 'MP4'),
    ('PPT', 'PPT'),
)


class CategoryOrganization(BaseModel):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Organization(BaseModel):
    category = models.ForeignKey(CategoryOrganization, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Service(BaseModel):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Training(BaseModel):
    auther = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="trainings/")
    description = models.TextField()
    number_participants = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TrainingMedia(BaseModel):
    training = models.ForeignKey(Training, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="trainings/media/", validators=[validate_file_type_and_size])
    order = models.IntegerField()
    type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES, editable=False)

    def save(self, *args, **kwargs):
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()

            if ext == '.pdf':
                self.type = 'PDF'
            elif ext in ['.mp4', '.mov', '.avi', '.mkv', '.flv']:
                self.type = 'MP4'
            elif ext in ['.ppt', '.pptx']:
                self.type = 'PPT'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.id)} {self.training.name or ''}"


class News(BaseModel):
    title = models.CharField(max_length=150)
    short_description = HTMLField(max_length=300)
    discretion = HTMLField()
    image = models.ImageField(upload_to="news/")
    is_published = models.BooleanField(default=True)
    is_published_date = models.DateField()

    def __str__(self):
        return self.title
