from django.urls import path
from tickets.api import views


urlpatterns = [
    path('',views.TicketListCreateView.as_view()),
    path('<int:pk>/', views.TicketDetailView.as_view()),
]