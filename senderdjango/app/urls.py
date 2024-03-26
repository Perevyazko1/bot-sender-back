from django.urls import path

from .views import get_task, create_task, delete_task,get_all_task

urlpatterns = [
    path('get_task/<str:chat_id>/', get_task),
    path('get_all_task/', get_all_task),
    path('delete_task/<int:task_id>/', delete_task),
    path('create_task/<str:chat_id>/', create_task),
]
