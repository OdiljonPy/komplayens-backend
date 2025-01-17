from django.db import models
from tinymce.models import HTMLField
from abstarct_model.base_model import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

FAQ_TYPE_CHOICES = (
    (1, 'FAQ System'),
    (2, 'FAQ Organization'),
    (3, 'FAQ Conflict of interest')
)

ABOUT_TYPE_CHOICES = (
    (1, 'About Conflict of Interest'),
    (2, 'About Corruption Risk'),
    (3, 'About Promotion and Useful Information')
)


class Region(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ('-created_at',)


class District(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Регион")
    name = models.CharField(max_length=150, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Округ"
        verbose_name_plural = "Округи"
        ordering = ('-created_at',)


class FAQ(BaseModel):
    question = models.CharField(max_length=250, verbose_name='Вопрос')
    answer = HTMLField(verbose_name='Отвечать')
    type = models.IntegerField(choices=FAQ_TYPE_CHOICES, default=1, verbose_name='Тип')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Часто задаваемый вопрос'
        verbose_name_plural = 'Часто задаваемые вопросы'
        ordering = ('-created_at',)


class AboutUs(BaseModel):
    title = models.CharField(max_length=200, verbose_name='Название', null=True, blank=True)
    short_description = models.TextField(max_length=500, verbose_name='Краткое описание', null=True, blank=True)
    image = models.ImageField(upload_to='about/', verbose_name='Изображение', null=True, blank=True)
    type = models.IntegerField(choices=ABOUT_TYPE_CHOICES, default=1, verbose_name='Категория')
    is_published = models.BooleanField(default=True, verbose_name='Oпубликован')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'
        ordering = ('-created_at',)


class Banner(BaseModel):
    title = models.CharField(max_length=200, verbose_name='Название')
    short_description = models.CharField(max_length=300, verbose_name='Краткое описание')
    image = models.ImageField(upload_to='banner/', verbose_name='Изображение')
    is_published = models.BooleanField(default=False, verbose_name='Oпубликован')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ('-created_at',)


class StatisticYear(BaseModel):
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(timezone.now().year)], unique=True, verbose_name='Год')

    def __str__(self):
        return str(self.year)

    class Meta:
        verbose_name = 'Статистика по году'
        verbose_name_plural = 'Статистика по годам'
        ordering = ('-year',)


class RainbowStatistic(BaseModel):
    year = models.ForeignKey(StatisticYear, on_delete=models.SET_NULL, null=True, verbose_name='Год')
    high = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                             verbose_name='Высокий процент')
    satisfactory = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                     verbose_name='Удовлетворительный процент')
    unsatisfactory = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                       verbose_name='Неудовлетворительный процент')

    def __str__(self):
        return f'Статистика за {self.year}'

    def clean(self):
        if self.year and RainbowStatistic.objects.filter(year=self.year).exists():
            raise ValidationError(f"Для года {self.year} уже существует запись статистики по радуге.")

    class Meta:
        verbose_name = 'Статистика по радуге'
        verbose_name_plural = 'Статистика по радуге'
        ordering = ('-year',)


class LinerStatistic(BaseModel):
    year = models.ForeignKey(StatisticYear, on_delete=models.SET_NULL, null=True, verbose_name='Год')
    name = models.CharField(max_length=300, verbose_name='Наименование')
    percentage = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                verbose_name='Процент')

    def __str__(self):
        return str(self.name)

    def clean(self):
        if self.year and LinerStatistic.objects.filter(year=self.year).count() >= 10:
            raise ValidationError(f"Для года {self.year} уже существует 10 записей линейной статистики.")

    class Meta:
        verbose_name = 'Линейная статистика'
        verbose_name_plural = 'Линейная статистика'
        ordering = ('-year',)
