from django.shortcuts import render
from .serializers import UserSerializer, TaskSerializer, TagSerializer
from .models import User, Task, Tag
from rest_framework import viewsets
import django_filters


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ('username',)


class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="exact")
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    performer = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ('status', 'tags')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related('performer', 'author').prefetch_related('tags')
    serializer_class = TaskSerializer
    filterset_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
