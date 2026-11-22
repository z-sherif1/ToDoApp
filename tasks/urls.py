from django.urls import path
from .views import *

urlpatterns = [
    path('',dashboard, name='dashboard'),
    path('task_list/',task_list, name='task_list'),
    path('detail/<int:pk>/',task_detail, name='task_detail'),
    path('create/',task_create, name='task_create'),
    path('update/<int:pk>/',task_update, name='task_update'),
    path('delete/<int:pk>/',task_delete, name='task_delete'),

]
