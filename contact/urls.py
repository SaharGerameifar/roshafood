from django.urls import path
from .views import ContactMe


urlpatterns = [
    path('contact/', ContactMe.as_view(), name='contact'),
]
