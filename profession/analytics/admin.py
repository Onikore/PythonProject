from django.contrib import admin

from analytics.models import RecordsWCities, RecordsWSkills, Records

admin.site.register([RecordsWSkills, RecordsWCities,Records])
