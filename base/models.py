from django.db import models
from tinymce.models import HTMLField
from abstarct_model.base_model import BaseModel

FAQ_TYPE_CHOICES = (
    (1, 'FAQ System'),
    (2, 'FAQ Organization'),
    (3, 'FAQ Conflict of interest')
)

ABOUT_TYPE_CHOICES = (
    (1, 'About System'),
    (2, 'About Violation Report'),
    (3, 'About Conflict of Interest'),
    (4, 'About Corruption Risk'),
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
        verbose_name = "Область"
        verbose_name_plural = "Области"
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
    short_desc = models.TextField(max_length=300, verbose_name='Краткое описание')
    link = models.CharField(max_length=40, verbose_name='Ссылка')
    type = models.IntegerField(choices=ABOUT_TYPE_CHOICES, default=1, verbose_name='Категория')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'
        ordering = ('-created_at',)


class CorruptionRisk(BaseModel):
    name = models.CharField(max_length=80, verbose_name='Название')
    short_desc = models.TextField(max_length=120, verbose_name='Краткое описание')
    more_desc = models.TextField(max_length=350, verbose_name='больше описания')
    useful_advice = models.TextField(max_length=350, verbose_name='Полезный совет')
    legal_document = models.FileField(upload_to='corruption_risk/legal_documents/', verbose_name='Юридический документ')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Риск коррупции'
        verbose_name_plural = 'Риск коррупции'
        ordering = ('-created_at',)


class CorruptionCase(BaseModel):
    corruption = models.ForeignKey(CorruptionRisk, on_delete=models.CASCADE, verbose_name='Коррупция')
    description = HTMLField(verbose_name='Описание')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Дело о коррупции'
        verbose_name_plural = 'Дело о коррупции'
        ordering = ('-created_at',)
