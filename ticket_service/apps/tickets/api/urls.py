from django.urls import path
from tickets.api import views


urlpatterns = [
    path('',views.TicketListCreateView.as_view()),
    path('ticket-count-summery/',views.TicketCountSummaryView.as_view()),
    path('ticket-cost-summery/',views.TicketCostSummeryView.as_view()),
    path('cancel/<int:pk>/', views.TicketUpdateView.as_view()),
    path('<int:pk>/',views.TicketDetailsView.as_view()),
]
