from django.urls import path, include
from iot.views import response
urlpatterns = [
    path(r'', response)
]