from django.shortcuts import render
from .serializers import UserSerializer, TaskSerializer, TagSerializer
from .models import User, Task, Tag
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related('performer', 'author').prefetch_related('tags')
    serializer_class = TaskSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
