from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

from chat.api_filters import MessageFilterSet
from chat.models import Message
from chat.serializers import MessageSerializer
from testChat.api_paginators import CustomPagination


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = CustomPagination
    filterset_fields = ['room', ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )

    def get_queryset(self):
        """
        For paginate of massages with slice lt of created_at
        p.s. : temporary solution, need fix filter_class
        """
        queryset = super(MessageViewSet, self).get_queryset()
        created_at__lt = self.request.GET.get('created_at__lt', None)
        if created_at__lt:
            queryset.filter(created_at__lt=created_at__lt)
        return queryset
