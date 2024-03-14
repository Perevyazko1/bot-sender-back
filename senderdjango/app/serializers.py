from rest_framework import serializers

from .models import ScheduledTask


class ScheduledTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledTask
        fields = [
            'id',
            'day_of_week',
            'chat_id',
            'time',
            'task',
            'task_name',

        ]

