from django.urls import path
from django.views.decorators.cache import cache_page

from analytics import views
from profession.settings import CACHE_TIME

urlpatterns = [
    path('', views.index, name='index'),
    path('demand/task_1', cache_page(CACHE_TIME)(views.demand_task_1), name='demand_task_1'),
    path('demand/task_2', cache_page(CACHE_TIME)(views.demand_task_2), name='demand_task_2'),
    path('demand/task_3', cache_page(CACHE_TIME)(views.demand_task_3), name='demand_task_3'),
    path('demand/task_4', cache_page(CACHE_TIME)(views.demand_task_4), name='demand_task_4'),
    path('geography/task_1', cache_page(CACHE_TIME)(views.geography_task_1), name='geography_task_1'),
    path('geography/task_2', cache_page(CACHE_TIME)(views.geography_task_2), name='geography_task_2'),
    path('skills/', views.skills, name='skills'),
    path('recent/', views.recent, name='recent'),
]
