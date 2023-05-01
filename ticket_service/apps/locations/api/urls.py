from django.urls import path
from locations.api import views


urlpatterns = [
    path('',views.LocationListCreateView.as_view()),
    path('<int:pk>/', views.LocationRetrieveUpdateDestroyView.as_view()),
]
