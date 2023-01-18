from django.core.validators import FileExtensionValidator
from django.db import models


class Records(models.Model):
    cities_csv = models.FileField(upload_to='files/', verbose_name='Файл с городами',
                                  validators=[FileExtensionValidator(['csv'])])
    skills_csv = models.FileField(upload_to='files/', verbose_name='Файл с навыками',
                                  validators=[FileExtensionValidator(['csv'])])

    class Meta:
        verbose_name = 'Файл с записями'
        verbose_name_plural = 'Файлы с записями'


class RecordsWSkills(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    skills = models.CharField(max_length=500, verbose_name='Навыки')
    salary_from = models.FloatField(verbose_name='Зарплата от')
    salary_to = models.FloatField(verbose_name='Зарплата до')
    salary_currency = models.CharField(max_length=20, verbose_name='Валюта')
    published_at = models.DateTimeField(verbose_name='Время публикации')

    class Meta:
        verbose_name = 'Запись с навыками'
        verbose_name_plural = 'Записи с навыками'

    def __str__(self):
        return f"Запись: №{self.pk}"


class RecordsWCities(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    salary_from = models.FloatField(verbose_name='Зарплата от')
    salary_to = models.FloatField(verbose_name='Зарплата до')
    salary_currency = models.CharField(max_length=20, verbose_name='Валюта')
    area_name = models.CharField(max_length=70, verbose_name='Город')
    published_at = models.DateTimeField(verbose_name='Время публикации')

    class Meta:
        verbose_name = 'Запись с городами'
        verbose_name_plural = 'Записи с городами'

    def __str__(self):
        return f"Запись: №{self.pk}"
