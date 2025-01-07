import os
from tinymce.models import HTMLField
from django.db import models
from abstarct_model.base_model import BaseModel
from base.models import Region, District
from .utils import validate_file_type_and_size

MEDIA_TYPE_CHOICES = (
    ('PDF', 'PDF'),
    ('MP4', 'MP4'),
    ('PPT', 'PPT'),
)

QUESTION_TYPE_CHOICES = (
    (1, 'One answer'),
    (2, 'Many answers'),
)

CONFLICT_ALERT_TYPE_CHOICES = (
    (1, "About existing conflicts of interest (notification)"),
    (2, "About the employee's possible conflict of interest (declaration)"),
    (3, "About possible conflict of interests of related persons (declaration)"),
)

Corruption_Risk_STATUS = (
    (1, 'In Progress'),
    (2, 'Closed')
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
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    phone_number2 = models.CharField(max_length=15, verbose_name='Номер телефона 2', blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="Электронная почта")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name="Регион")
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="Область")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    weblink = models.URLField(blank=True, null=True, verbose_name='Ссылка')
    instagram = models.URLField(blank=True, null=True, verbose_name='')
    telegram = models.URLField(blank=True, null=True, verbose_name='')
    facebook = models.URLField(blank=True, null=True, verbose_name='')
    twitter = models.URLField(blank=True, null=True, verbose_name='')
    youtube = models.URLField(blank=True, null=True, verbose_name='')

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


class TrainingCategory(BaseModel):
    name = models.CharField(max_length=40, verbose_name='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ('-created_at',)


class Training(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(upload_to="trainings/", verbose_name="Изображение")
    description = HTMLField(verbose_name="описание")
    video = models.URLField(default='https://www.youtube.com/', verbose_name='')
    category = models.ForeignKey(to='TrainingCategory', on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('-created_at',)


class TrainingMedia(BaseModel):
    training = models.ForeignKey(Training, on_delete=models.SET_NULL, null=True, verbose_name="Урок")
    filename = models.CharField(max_length=100, verbose_name='')
    file = models.FileField(
        upload_to="trainings/media/", validators=[validate_file_type_and_size],
        verbose_name="Файл", blank=True, null=True)
    video = models.URLField(default='https://www.youtube.com/', verbose_name='', blank=True, null=True)
    video_title = models.CharField(verbose_name='', blank=True, null=True)
    order = models.IntegerField(verbose_name="Очередь")
    type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES, editable=False, verbose_name="Тип")

    def save(self, *args, **kwargs):
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()

            if ext == '.pdf':
                self.type = 'PDF'
            elif ext in ['.ppt', '.pptx']:
                self.type = 'PPT'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.id)} {self.training.name or ''}"

    class Meta:
        verbose_name = 'Видео урока'
        verbose_name_plural = 'Видео уроков'
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
    name = models.CharField(max_length=80, verbose_name='Имя')
    author = models.CharField(max_length=100, verbose_name='Автор')
    edition_author = models.CharField(max_length=100, verbose_name='')
    edition_type = models.CharField(max_length=100, verbose_name='')
    edition_year = models.DateField(null=True, verbose_name='')
    file = models.FileField(upload_to='electron_libraries/', verbose_name='Файл книги')
    category = models.ForeignKey(
        ElectronLibraryCategory, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Электронная библиотека'
        verbose_name_plural = 'Электронные библиотеки'
        ordering = ('-created_at',)


class NewsCategory(BaseModel):
    name = models.CharField(max_length=30, verbose_name='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ('-created_at',)


class News(BaseModel):
    title = models.CharField(max_length=300, verbose_name="Заголовок")
    short_description = models.CharField(max_length=150, verbose_name='')
    description = HTMLField(verbose_name="Описание")
    image = models.ImageField(upload_to="news/", verbose_name="Изображение")
    category = models.ForeignKey(to='NewsCategory', on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    published_date = models.DateField(null=True, blank=True, verbose_name="Дата публикации")
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-created_at',)


class HonestyTestCategory(BaseModel):
    name = models.CharField(max_length=40, verbose_name='')
    image = models.ImageField(upload_to='honesty_test/category', verbose_name='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ('-created_at',)


class HonestyTest(BaseModel):
    question = HTMLField(verbose_name='Вопрос')
    advice = models.CharField(max_length=300, verbose_name='')
    category = models.ForeignKey(to='HonestyTestCategory', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Тест на честность'
        verbose_name_plural = 'Тест на честность'
        ordering = ('-created_at',)


class HonestyTestAnswer(BaseModel):
    question = models.ForeignKey(HonestyTest, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.CharField(max_length=120, verbose_name='Отвечать')
    image = models.ImageField(upload_to='honesty_test/answer', verbose_name='')
    is_true = models.BooleanField(default=False, verbose_name='')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Ответ на тест на честность'
        verbose_name_plural = 'Ответ на тест на честность'
        ordering = ('-created_at',)


class HonestyTestResult(BaseModel):
    customer = models.ForeignKey(to='authentication.Customer', on_delete=models.CASCADE, verbose_name='')
    test = models.ForeignKey(to='HonestyTest', on_delete=models.CASCADE, verbose_name='')
    answer = models.ForeignKey(to='HonestyTestAnswer', on_delete=models.CASCADE, verbose_name='')
    result = models.BooleanField(default=False, verbose_name='')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ('-created_at',)


class CorruptionRisk(BaseModel):
    name = models.CharField(max_length=80, verbose_name='Название')
    short_desc = models.TextField(max_length=120, verbose_name='Краткое описание')
    image = models.ImageField(upload_to='corruption_risk/', verbose_name='')

    form_url = models.URLField(verbose_name='')
    excel_url = models.URLField(verbose_name='')

    start_date = models.DateTimeField(verbose_name='')
    end_date = models.DateTimeField(verbose_name='')
    result = HTMLField(blank=True, verbose_name='Результат')
    status = models.IntegerField(choices=Corruption_Risk_STATUS, default=1, verbose_name='')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Риск коррупции'
        verbose_name_plural = 'Риск коррупции'
        ordering = ('-created_at',)


class ConflictAlert(BaseModel):
    organization_name = models.CharField(max_length=80, verbose_name='Название организации')
    organization_director_full_name = models.CharField(max_length=150, verbose_name='ФИО директора организации',
                                                       null=True, blank=True)
    organization_director_position = models.CharField(max_length=80, verbose_name='Должность директора организации',
                                                      null=True, blank=True)
    description = models.TextField(max_length=1000, verbose_name='Описание', blank=True, null=True)
    additional_description = models.TextField(max_length=1000, verbose_name='Дополнительное описание', blank=True,
                                              null=True)
    filled_date = models.DateField(null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=CONFLICT_ALERT_TYPE_CHOICES, verbose_name='Тип')

    employee_full_name = models.CharField(max_length=150, verbose_name='Полное имя')
    employee_position = models.CharField(max_length=120, verbose_name='Позиция информатора')
    employee_passport_number = models.CharField(max_length=14, verbose_name='Информатор ЖШШР')
    employee_passport_series = models.CharField(max_length=9, verbose_name='Серия паспортов информатора')
    employee_passport_taken_date = models.DateField(verbose_name='Дата получения паспорта')
    employee_legal_entity_name = models.CharField(max_length=300, verbose_name='Название юридического лица', blank=True,
                                                  null=True)
    employee_legal_entity_data = models.CharField(max_length=300,
                                                  verbose_name='Персональные данные сотрудников и юридических лиц')
    employee_stir_number = models.CharField(max_length=120, verbose_name='Номер STIR', blank=True, null=True)

    related_persons_full_name = models.CharField(max_length=150, verbose_name='Полное имя')
    related_persons_passport_number = models.CharField(max_length=14, verbose_name='Информатор ЖШШР', blank=True,
                                                       null=True)
    related_persons_passport_series = models.CharField(max_length=9, verbose_name='Серия паспортов информатора',
                                                       blank=True, null=True)
    related_persons_passport_taken_date = models.DateField(verbose_name='Дата получения паспорта', blank=True,
                                                           null=True)
    related_persons_legal_entity_name = models.CharField(max_length=300, verbose_name='Название юридического лица',
                                                         blank=True, null=True)
    related_persons_stir_number = models.CharField(max_length=120, verbose_name='Номер STIR', blank=True, null=True)
    related_persons_kinship_data = models.CharField(max_length=200, verbose_name='Данные о родстве', blank=True,
                                                    null=True)

    def __str__(self):
        return str(self.employee_full_name)

    class Meta:
        verbose_name = 'Оповещение о конфликте'
        verbose_name_plural = 'Оповещение о конфликте'
        ordering = ('-created_at',)


class Profession(BaseModel):
    name = models.CharField(max_length=80, verbose_name='Название')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'
        ordering = ('-created_at',)


class ProfessionalEthics(BaseModel):
    title = models.CharField(max_length=300, verbose_name='Название')
    description = HTMLField(verbose_name='Описание')
    case = models.CharField(max_length=300, verbose_name='')
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
    event_time = models.DateTimeField(verbose_name='Время события')
    region = models.ForeignKey(to='base.Region', on_delete=models.SET_NULL, null=True, verbose_name='Область')
    district = models.ForeignKey(to='base.District', on_delete=models.SET_NULL, null=True, verbose_name='Округ')
    report_type = models.ForeignKey(ReportType, on_delete=models.SET_NULL, null=True, verbose_name='Тип отчета')
    comment = models.TextField(verbose_name='Комментарий')

    informant_full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='')
    informant_phone_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='')
    informant_email = models.EmailField(blank=True, null=True, verbose_name='')
    is_anonim = models.BooleanField(default=False, verbose_name='')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Отчет о нарушении'
        verbose_name_plural = 'Отчет о нарушении'
        ordering = ('-created_at',)


class GuiltyPerson(BaseModel):
    report = models.ForeignKey(to='ViolationReport', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, verbose_name='')
    position = models.CharField(max_length=100, verbose_name='')
    phone_number = models.CharField(max_length=100, verbose_name='')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ('-created_at',)


class ViolationFile(BaseModel):
    report = models.ForeignKey(to='ViolationReport', on_delete=models.CASCADE, verbose_name='')
    file = models.FileField(upload_to='violation_report/', verbose_name='Файл')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
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
