from django.urls import path

from analytics import views

urlpatterns = [
    path('', views.index, name='index'),
    path('demand/task_1', views.demand_task_1, name='demand_task_1'),
    path('demand/task_2', views.demand_task_2, name='demand_task_2'),
    path('demand/task_3', views.demand_task_1, name='demand_task_3'),
    path('demand/task_4', views.demand_task_1, name='demand_task_4'),
    path('geography/', views.geography, name='geography'),
    path('skills/', views.skills, name='skills'),
    path('recent/', views.recent, name='recent'),
]
