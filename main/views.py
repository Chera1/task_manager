from typing import cast

from rest_framework_extensions.mixins import NestedViewSetMixin

from main.services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin
from .serializers import UserSerializer, TaskSerializer, TagSerializer
from .models import User, Task, Tag
from rest_framework import viewsets
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


class UserTasksViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .select_related("author", "performer")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer


class TaskTagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminDelete,)
