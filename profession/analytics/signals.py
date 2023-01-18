import pandas as pd
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from analytics.models import Records, RecordsWSkills, RecordsWCities


@receiver(pre_delete, sender=Records)
def records_delete(sender, instance, **kwargs):
    instance.cities_csv.delete(False)
    instance.skills_csv.delete(False)
    RecordsWCities.objects.all().delete()
    RecordsWSkills.objects.all().delete()


@receiver(post_save, sender=Records)
def records_save(sender, instance, **kwargs):
    chunk_size = 10000
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
        if len(chunk) > chunk_size:
            RecordsWSkills.objects.bulk_create(chunk)
            chunk = []
    RecordsWSkills.objects.bulk_create(chunk)
    chunk = []
    city_path = instance.cities_csv.path
    for _, i in pd.read_csv(city_path, parse_dates=['published_at'], sep=',', infer_datetime_format=True).iterrows():
        chunk.append(RecordsWCities(name=i[0],
                                    salary_from=i[1],
                                    salary_to=i[2],
                                    salary_currency=i[3],
                                    area_name=i[4],
                                    published_at=i[5]))
        if len(chunk) > chunk_size:
            RecordsWCities.objects.bulk_create(chunk)
            chunk = []
    RecordsWCities.objects.bulk_create(chunk)
