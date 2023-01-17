import datetime

import pandas as pd
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver


class Records(models.Model):
    cities_csv = models.FileField(upload_to='files/', verbose_name='Файл с городами',
                                  validators=[FileExtensionValidator(['csv'])])
    skills_csv = models.FileField(upload_to='files/', verbose_name='Файл с навыками',
                                  validators=[FileExtensionValidator(['csv'])])

    class Meta:
        verbose_name = 'Файл с записями'
        verbose_name_plural = 'Файлы с записями'


@receiver(pre_delete, sender=Records)
def records_delete(sender, instance, **kwargs):
    instance.cities_csv.delete(False)
    instance.skills_csv.delete(False)
    RecordsWCities.objects.all().delete()
    RecordsWSkills.objects.all().delete()


@receiver(post_save, sender=Records)
def records_save(sender, instance, **kwargs):
    print(f'первый {datetime.datetime.now()}')
    skills_path = instance.skills_csv.path
    chunk = []
    for _, i in pd.read_csv(skills_path, parse_dates=['published_at'], sep=',', infer_datetime_format=True).iterrows():
        chunk.append(RecordsWSkills(name=i[0],
                                    skills=i[1],
                                    salary_from=i[2],
                                    salary_to=i[3],
                                    salary_currency=i[4],
                                    published_at=i[5]
                                    ))
        if len(chunk) > 50000:
            RecordsWSkills.objects.bulk_create(chunk)
            chunk = []
    RecordsWSkills.objects.bulk_create(chunk)
    chunk = []

    # RecordsWSkills.objects.bulk_create(
    #     RecordsWSkills(name=row[0],
    #                    skills=row[1],
    #                    salary_from=row[2],
    #                    salary_to=row[3],
    #                    salary_currency=row[4],
    #                    published_at=row[5]) for _, row in df.iterrows()
    # )

    print(f'второй {datetime.datetime.now()}')
    city_path = instance.cities_csv.path
    for _, i in pd.read_csv(city_path, parse_dates=['published_at'], sep=',', infer_datetime_format=True).iterrows():
        chunk.append(RecordsWCities(name=i[0],
                                    salary_from=i[1],
                                    salary_to=i[2],
                                    salary_currency=i[3],
                                    area_name=i[4],
                                    published_at=i[5]))
        if len(chunk) == 50000:
            RecordsWCities.objects.bulk_create(chunk)
            chunk = []
    RecordsWCities.objects.bulk_create(chunk)
    print(f'конец {datetime.datetime.now()}')
    # RecordsWCities.objects.bulk_create(
    #     RecordsWCities(name=row[0],
    #                    salary_from=row[1],
    #                    salary_to=row[2],
    #                    salary_currency=row[3],
    #                    area_name=row[4],
    #                    published_at=row[5]) for _, row in df.iterrows()
    # )


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
