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
    name = models.CharField(max_length=150, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категоря организации'
        verbose_name_plural = 'Категории организаций'
        ordering = ('-created_at',)


class Organization(BaseModel):
    category = models.ForeignKey(CategoryOrganization, on_delete=models.PROTECT, verbose_name="Категория")
    name = models.CharField(max_length=255, verbose_name="Название")
    phone_number = models.CharField(max_length=255, verbose_name="Номер телефона")
    email = models.CharField(max_length=255, verbose_name="Электронная почта")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name="Регион")
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="Область")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ('-created_at',)


class Service(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Название")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, verbose_name="Организация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'
        ordering = ('-created_at',)


class Training(BaseModel):
    auther = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    name = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(upload_to="trainings/", verbose_name="Изображение")
    description = models.TextField(verbose_name="описание")
    number_participants = models.IntegerField(default=0, verbose_name="Количество участников")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('-created_at',)


class TrainingMedia(BaseModel):
    training = models.ForeignKey(Training, on_delete=models.SET_NULL, null=True, verbose_name="Урок")
    file = models.FileField(upload_to="trainings/media/", validators=[validate_file_type_and_size], verbose_name="Файл")
    order = models.IntegerField(verbose_name="Очередь")
    type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES, editable=False, verbose_name="Тип")

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

    class Meta:
        verbose_name = 'Видео урока'
        verbose_name_plural = 'Видео уроков'
        ordering = ('-created_at',)


class News(BaseModel):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    short_description = HTMLField(max_length=300, verbose_name="Краткое описание")
    discretion = HTMLField(verbose_name="Описание")
    image = models.ImageField(upload_to="news/", verbose_name="Изображение")
    is_published = models.BooleanField(default=True, verbose_name="Опублекован")
    is_published_date = models.DateField(verbose_name="Дата публекации")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-created_at',)
