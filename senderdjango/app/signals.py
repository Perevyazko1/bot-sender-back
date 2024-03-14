from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import ScheduledTask
import json
import redis


def new_task(task, is_create: bool):
    redis_host = 'redis'
    redis_port = 6379
    redis_db = 0
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    if is_create:
        redis_client.rpush('create_tasks', task)
    else:
        redis_client.rpush('delete_tasks', task)


@receiver(post_save, sender=ScheduledTask)
def scheduled_task_created(sender, instance, created, **kwargs):
    if created:
        tasks = json.dumps({
            'id' : instance.id,
            'day_of_week' : instance.day_of_week ,
            'chat_id' : instance.chat_id ,
            'time' : instance.time,
            'task' : instance.task ,
            'task_name' : instance.task_name,
        })
        new_task(tasks,is_create=True)


@receiver(pre_delete, sender=ScheduledTask)
def scheduled_task_deleted(sender, instance, **kwargs):
    # Объект ScheduledTask будет удален
    tasks = json.dumps({
        'id': instance.id,
        'day_of_week': instance.day_of_week,
        'chat_id': instance.chat_id,
        'time': instance.time,
        'task': instance.task,
        'task_name': instance.task_name,
    })
    new_task(tasks, is_create=False)

    print(f'ScheduledTask с id {instance.id} будет удален')
