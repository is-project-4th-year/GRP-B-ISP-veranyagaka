from .views import predict_view
from django.urls import path

urlpatterns = [
    path("predict/", predict_view, name="predict"),
]