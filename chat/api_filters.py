from django_filters import DateTimeFilter
from django_filters import FilterSet

from chat.models import Message


class MessageFilterSet(FilterSet):
    """
    For paginate of massages with slice lt of created_at
    p.s : Not working need fix it!!!
    """
    created_at__lt = DateTimeFilter(field_name="created_at", lookup_expr='lt')

    class Meta:
        model = Message
        fields = ['created_at__lt', ]
