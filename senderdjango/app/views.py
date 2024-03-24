from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import ScheduledTask
from .serializers import ScheduledTaskSerializer
from rest_framework import permissions
import redis
import json



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_task(request,chat_id):
    queryset = ScheduledTask.objects.filter(chat_id=int(chat_id))
    serializer = ScheduledTaskSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_all_task(request):
    queryset = ScheduledTask.objects.all()
    serializer = ScheduledTaskSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_task(request):
    ScheduledTask.objects.update_or_create(
        day_of_week= request.data["day_of_week"],
        chat_id= request.data.get('chat_id', 0),
        time= request.data["time"],
        task= request.data["task"],
        task_name= request.data["task_name"],
    )
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def delete_task(request,task_id):
    deleteObject = ScheduledTask.objects.get(id=task_id)
    ScheduledTask.delete(deleteObject)
    return Response(status=status.HTTP_200_OK)

