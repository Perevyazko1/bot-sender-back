from django.db import models


class ScheduledTask(models.Model):
    id = models.AutoField(primary_key=True)
    day_of_week = models.CharField(max_length=20)
    chat_id = models.IntegerField()
    time = models.TextField()
    task = models.TextField()
    task_name = models.CharField(max_length=100)

    def __str__(self):
        return self.task_name
