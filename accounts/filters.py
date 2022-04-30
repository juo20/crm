import django_filters
from . import models


class OrderFilter(django_filters.FilterSet):

    product = django_filters.CharFilter(
        field_name='product__name',
        label='Product',
        lookup_expr='icontains'
    )

    start_date = django_filters.DateFilter(
        field_name='date_created',
        label='Start Date',
        lookup_expr='gte',
        input_formats=["%d/%m/%Y"]
    )

    end_date = django_filters.DateFilter(
        field_name='date_created',
        label='End Date',
        lookup_expr='lte',
        input_formats=["%d/%m/%Y"]
    )

    class Meta:
        model = models.Order
        fields = ['product', 'status', 'start_date', 'end_date']
