from django.urls import path
from .views import LandingAPI, LandingAPIDetail

urlpatterns = [
    # Ruta general (GET todos, POST)
    path("index/", LandingAPI.as_view(), name="landing-api-index"),
    
    # Ruta específica con ID (GET uno, PUT, DELETE)
    path("index/<str:pk>/", LandingAPIDetail.as_view(), name="landing-api-detail"),
]
