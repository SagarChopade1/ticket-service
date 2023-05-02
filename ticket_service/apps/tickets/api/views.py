from rest_framework import  generics
from users.permissions import IsAdminTypeUser,IsManagerTypeUser
from rest_framework import generics, status
from rest_framework.response import Response
from tickets.models import Ticket
from .serializers import TicketSerializer,TicketSummarySerializer,TicketCostSummarySerializer
from rest_framework.permissions import IsAdminUser 
from tickets.utils import  QrCode
from .filters import TicketFilter,TicketSummeryFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Count,  F,Sum
from django.db.models.functions import ExtractYear,ExtractMonth
from calendar import month_abbr
class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser,IsAdminTypeUser, IsManagerTypeUser]
    filterset_class = TicketFilter 
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save(created_by=request.user)
        if ticket.passenger:
            ticket.passenger.name=ticket.passenger.full_name
        qr_code_bytes=QrCode.generate_qr_code(ticket.id,ticket.source.name, ticket.destination.name, ticket.journey_start_time,ticket.journey_end_time, ticket.price,ticket.currency_type, ticket.passenger_name,ticket.transportation_type.type)
        ticket.qr_code=qr_code_bytes
        ticket.price = serializer.data['price']
        ticket.is_qr_code_valid = True
        ticket.is_cancelled = False
        ticket.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if self.request.user.is_manager:
            return self.queryset.filter(created_by=self.request.user)
        if self.request.user.is_personnel:
            return self.queryset.filter(passenger=self.request.user)
        return self.queryset
class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser,IsAdminTypeUser, IsManagerTypeUser]


class TicketCountSummaryView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketSummeryFilter 

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            location_name=F('source__name'),
            year=ExtractYear('journey_start_time'),
            month=ExtractMonth('journey_start_time'),
        ).values('location_name', 'year', 'month').annotate(count=Count('*'))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class TicketCostSummeryView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCostSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketSummeryFilter

    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset= queryset.values(location_name=F('source__name'),
            year=ExtractYear('journey_start_time'),
            month=ExtractMonth('journey_start_time')).annotate(
            price=Sum('price')
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        summary = {}
        for ticket in queryset:
            location = ticket['location_name']
            month = ticket['month']
            year = ticket['year']
            price = ticket['price']
            month_name = month_abbr[month] + '-' + str(year)
            if location not in summary:
                summary[location] = {month_name: price}
            else:
                summary[location][month_name] = price
        data = []
        for location, values in summary.items():
            location_data = {'location': location}
            for i in range(1, 13):
                first_key = next(iter(values))
                month_name = month_abbr[i] + '-' + first_key.split('-')[1]
                if month_name in values:
                    location_data[month_name] = '$ ' + str(values[month_name])
                else:
                    location_data[month_name] = '0 $'
            data.append(location_data)
        return Response(data)
