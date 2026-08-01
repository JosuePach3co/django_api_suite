from django.urls import path
from . import views

urlpatterns = [
   # Dejar las comillas vacías para que la ruta sea solo /demo/rest/api/
   path("", views.DemoRestApi.as_view(), name="demo_rest_api_resources" ),
   path("<str:item_id>/", views.DemoRestApiItem.as_view(), name="demo_rest_api_item"),
]