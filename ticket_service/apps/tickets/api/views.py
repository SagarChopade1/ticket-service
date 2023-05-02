from rest_framework import permissions, generics
from users.permissions import IsAdminTypeUser,IsManagerTypeUser
from rest_framework import generics, status
from rest_framework.response import Response
from tickets.models import Ticket
from .serializers import TicketSerializer
from rest_framework.permissions import IsAdminUser 
from tickets.utils import  QrCode
from .filters import TicketFilter
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
