from django.db import models
from abstarct_model.base_model import BaseModel


class Region(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Назавние')

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
