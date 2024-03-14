from django.urls import path

from .views import get_task, create_task, delete_task

urlpatterns = [
    path('get_task/', get_task),
    path('delete_task/<int:task_id>/', delete_task),
    path('create_task/', create_task),
]
