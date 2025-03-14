from django.urls import path
from .views import obtener_examenes

urlpatterns = [
    path('examenes/', obtener_examenes, name='obtener_examenes'),
]
