from django_filters import rest_framework as filters
from tickets.models import Ticket
from ticket_service.common.filters import DateRangeBaseFilter
import django_filters

class TicketFilter(filters.FilterSet):
    source = filters.CharFilter(field_name='source__name', lookup_expr='icontains')
    destination = filters.CharFilter(field_name='destination__name', lookup_expr='icontains')
    passenger_name = filters.CharFilter(field_name='passenger_name', lookup_expr='icontains')
    journey_start_date = filters.DateFilter(field_name='journey_start_time', lookup_expr='date')
    journey_end_date = filters.DateFilter(field_name='journey_end_time', lookup_expr='date')

    class Meta:
        model = Ticket
        fields = ['source', 'destination', 'passenger_name', 'journey_start_date', 'journey_end_date']

class TicketSummeryFilter(filters.FilterSet,DateRangeBaseFilter):

    class Meta:
        model = Ticket
        fields = ['source__name',"is_cancelled"]


    journey_start_time_after = django_filters.DateFilter(
        field_name="journey_start_time", method="start_range"
    )
    journey_start_time_before = django_filters.DateFilter(
        field_name="journey_start_time", method="end_range"
    )
