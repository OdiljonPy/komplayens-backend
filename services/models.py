import os
from tinymce.models import HTMLField
from django.db import models
from django.utils import timezone
from abstarct_model.base_model import BaseModel
from base.models import Region, District
from .utils import validate_file_type_and_size

MEDIA_TYPE_CHOICES = (
    ('PDF', 'PDF'),
    ('MP4', 'MP4'),
    ('PPT', 'PPT'),
)

REPORT_STATUS_CHOICES = (
    (1, 'Viewing'),
    (2, 'Checking'),
    (3, 'Completed')
)


class CategoryOrganization(BaseModel):
    name = models.CharField(max_length=150, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория организации'
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
    link = models.CharField(max_length=40, default='https://murojaat.gov.uz/', verbose_name='Ссылка')

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
    author = models.CharField(max_length=150, verbose_name="Автор")
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


class TrainingTest(BaseModel):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, verbose_name='Обучение')
    question = models.CharField(max_length=120, verbose_name='Вопрос')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Тест на обучение'
        verbose_name_plural = 'Тесты по обучению'
        ordering = ('-created_at',)


class TrainingTestAnswer(BaseModel):
    question = models.ForeignKey(TrainingTest, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.CharField(max_length=120, verbose_name='Ответ')
    is_true = models.BooleanField(default=False, verbose_name='Верно')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Ответ на тренировочный тест'
        verbose_name_plural = 'Ответы на тренировочные тесты'
        ordering = ('-created_at',)


class ElectronLibraryCategory(BaseModel):
    name = models.CharField(max_length=40, verbose_name='Название')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Категория Электронная библиотека'
        verbose_name_plural = 'Категория Электронная библиотека'
        ordering = ('-created_at',)


class ElectronLibrary(BaseModel):
    title = models.CharField(max_length=120, verbose_name='Название')
    file = models.FileField(upload_to='electron_libraries/', verbose_name='Файл книги')
    category = models.ForeignKey(
        ElectronLibraryCategory, on_delete=models.SET_NULL, null=True, verbose_name='Категория')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Электронная библиотека'
        verbose_name_plural = 'Электронные библиотеки'
        ordering = ('-created_at',)


class News(BaseModel):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    short_description = HTMLField(max_length=300, verbose_name="Краткое описание")
    description = HTMLField(verbose_name="Описание")
    image = models.ImageField(upload_to="news/", verbose_name="Изображение")
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")
    is_published_date = models.DateField(verbose_name="Дата публикации")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-created_at',)


class HonestyTest(BaseModel):
    question = models.CharField(max_length=120, verbose_name='Вопрос')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Тест на честность'
        verbose_name_plural = 'Тест на честность'
        ordering = ('-created_at',)


class HonestyTestAnswer(BaseModel):
    question = models.ForeignKey(HonestyTest, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.CharField(max_length=120, verbose_name='Отвечать')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Ответ на тест на честность'
        verbose_name_plural = 'Ответ на тест на честность'
        ordering = ('-created_at',)


class CorruptionRating(BaseModel):
    corruption = models.ForeignKey(to='base.CorruptionRisk', on_delete=models.CASCADE, verbose_name='Коррупция')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Рейтинг клиентов'
        verbose_name_plural = 'Рейтинг клиентов'
        ordering = ('-created_at',)


class CorruptionType(BaseModel):
    name = models.CharField(max_length=80, verbose_name='Название коррупции')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид коррупции',
        verbose_name_plural = 'коррупции'
        ordering = ('-created_at',)


class Corruption(BaseModel):
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание', max_length=350)
    type = models.ForeignKey(CorruptionType, on_delete=models.SET_NULL, null=True, verbose_name='Тип')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Коррупция'
        verbose_name_plural = 'Коррупция'
        ordering = ('-created_at',)


class CorruptionMaterial(BaseModel):
    corruption = models.ForeignKey(Corruption, on_delete=models.CASCADE, verbose_name='Коррупция')
    file = models.FileField(upload_to='corruption/material', verbose_name='Файл о коррупции')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Коррупционный материал'
        verbose_name_plural = 'Коррупционный материал'
        ordering = ('-created_at',)


class CitizenOversight(BaseModel):
    control_method = models.CharField(max_length=140, verbose_name='Метод контроля')
    control_result = models.CharField(max_length=140, verbose_name='Результат контроля')
    description = models.TextField(max_length=350, verbose_name='Описание')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Гражданский надзор'
        verbose_name_plural = 'Гражданский надзор'


class ConflictAlertType(BaseModel):
    name = models.CharField(max_length=60, verbose_name='Название')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Тип оповещения о конфликте'
        verbose_name_plural = 'Тип оповещения о конфликте'
        ordering = ('-created_at',)


class ConflictAlert(BaseModel):
    organization_name = models.CharField(max_length=80, verbose_name='Название организации')
    description = models.TextField(max_length=350, verbose_name='Описание')
    event_date = models.DateField(default=timezone.now, verbose_name='Дата события')
    action_taken = models.CharField(max_length=150, verbose_name='Принятые меры')
    type = models.ForeignKey(ConflictAlertType, on_delete=models.CASCADE, verbose_name='Тип')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Оповещение о конфликте'
        verbose_name_plural = 'Оповещение о конфликте'
        ordering = ('-created_at',)


class RelatedPerson(BaseModel):
    conflict_alert = models.ForeignKey(ConflictAlert, on_delete=models.CASCADE, verbose_name='Оповещение о конфликте')
    first_name = models.CharField(max_length=60, verbose_name='Имя')
    last_name = models.CharField(max_length=60, verbose_name='Фамилия')
    position = models.CharField(max_length=120, verbose_name='Позиция информатора')
    informant_jshshr = models.CharField(max_length=14, verbose_name='Информатор ЖШШР')
    informant = models.BooleanField(default=False, verbose_name='Является ли информатором')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Связанное лицо'
        verbose_name_plural = 'Связанное лицо'
        ordering = ('-created_at',)


class Profession(BaseModel):
    name = models.CharField(max_length=80, verbose_name='Название')
    description = models.TextField(max_length=300, verbose_name='Описание')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'
        ordering = ('-created_at',)


class ProfessionalEthics(BaseModel):
    title = models.CharField(max_length=80, verbose_name='Название')
    description = models.TextField(max_length=350, verbose_name='Описание')
    moral_dilemma = models.CharField(max_length=80, verbose_name='Моральная дилемма')
    link = models.CharField(max_length=30, verbose_name='Ссылка')
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, verbose_name='Профессия')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Профессиональная этика'
        verbose_name_plural = 'Профессиональная этика'
        ordering = ('-created_at',)


class OfficerAdvice(BaseModel):
    officer = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, verbose_name='Клиент')
    professional_ethics = models.ForeignKey(
        ProfessionalEthics, on_delete=models.CASCADE, verbose_name='Профессиональная этика')
    comment = models.TextField(max_length=350, verbose_name='Комментарий')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Советы клиентам'
        verbose_name_plural = 'Советы клиентам'
        ordering = ('-created_at',)


class ReportType(BaseModel):
    name = models.CharField(max_length=120, verbose_name='Название')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Тип отчета'
        verbose_name_plural = 'Тип отчета'
        ordering = ('-created_at',)


class ViolationReport(BaseModel):
    organization = models.ForeignKey(
        to='services.Organization', on_delete=models.SET_NULL, null=True, verbose_name='Организация')
    event_time = models.DateField(verbose_name='Время события')
    region = models.ForeignKey(to='base.Region', on_delete=models.SET_NULL, null=True, verbose_name='Область')
    district = models.ForeignKey(to='base.District', on_delete=models.SET_NULL, null=True, verbose_name='Округ')
    status = models.IntegerField(choices=REPORT_STATUS_CHOICES, verbose_name='Статус')
    report_type = models.ForeignKey(ReportType, on_delete=models.SET_NULL, null=True, verbose_name='Тип отчета')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Отчет о нарушении'
        verbose_name_plural = 'Отчет о нарушении'
        ordering = ('-created_at',)


class ViolationReportFile(BaseModel):
    report = models.ForeignKey(ViolationReport, on_delete=models.CASCADE, verbose_name='Отчет о нарушении')
    file = models.FileField(upload_to='violation_report/', verbose_name='Файл')
    comment = models.TextField(max_length=350, verbose_name='Комментарий')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Файл отчета о нарушении'
        verbose_name_plural = 'Файл отчета о нарушении'
        ordering = ('-created_at',)


class OrganizationSummary(BaseModel):
    organization = models.ForeignKey(
        to='services.Organization', on_delete=models.SET_NULL, null=True, verbose_name='Организация')
    report = models.ForeignKey(ViolationReport, on_delete=models.CASCADE, verbose_name='Отчет о нарушении')
    comment = models.TextField(max_length=350, verbose_name='Комментарий')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Краткое описание организации'
        verbose_name_plural = 'Краткое описание организации'
        ordering = ('-created_at',)


class GuiltyPerson(BaseModel):
    report = models.ForeignKey(ViolationReport, on_delete=models.CASCADE, verbose_name='Отчет о нарушении')
    first_name = models.CharField(max_length=80, verbose_name='Имя')
    last_name = models.CharField(max_length=80, verbose_name='Фамилия')
    position = models.CharField(max_length=150, verbose_name='Позиция')
    contact = models.CharField(max_length=80, verbose_name='Контакт')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Виновное лицо'
        verbose_name_plural = 'Виновное лицо'
        ordering = ('-created_at',)


class TechnicalSupport(BaseModel):
    image = models.FileField(upload_to='technical_support/')
    comment = models.TextField(max_length=300, verbose_name='Комментарий')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Техническая поддержка'
        verbose_name_plural = 'Техническая поддержка'
        ordering = ('-created_at',)
