from typing import cast, Any

from django.http import Http404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_extensions.mixins import NestedViewSetMixin
from main.services.async_celery import AsyncJob, JobStatus

from main.services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin
from .serializers import (
    UserSerializer,
    TaskSerializer,
    TagSerializer,
    CountDownJobSerializer,
    JobSerializer,
)
from .models import User, Task, Tag
from rest_framework import viewsets, mixins, status
from .permissions import IsAdminDelete
import django_filters


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username", "last_name")


class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="exact")
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    performer = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ("status", "tags")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = (IsAdminDelete,)


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.all()
        .select_related("performer", "author")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = (IsAdminDelete,)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .select_related("author", "performer")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer
    permission_classes = (IsAdminDelete,)


class TaskTagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = (IsAdminDelete,)

    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminDelete,)


class CountDownJobViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CountDownJobSerializer

    def get_success_headers(self, data):
        task_id = data["task_id"]
        return {"Location": reverse("jobs-detail", args=[task_id])}


class AsyncJobViewSet(viewsets.GenericViewSet):
    serializer_class = JobSerializer

    def get_object(self) -> AsyncJob:
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        task_id = self.kwargs[lookup_url_kwargs]
        job = AsyncJob.from_id(task_id)
        if job.status == JobStatus.UNKNOWN:
            raise Http404()
        return job

    def retrieve(self, reqeust: Request, *args: Any, **kwargs: Any):
        instance = self.get_object()
        serializer_data = self.get_serializer(instance).data
        if instance.status == JobStatus.SUCCESS:
            location = self.request.build_absolute_uri(instance.result)
            return Response(
                serializer_data,
                headers={"location": location},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer_data)
