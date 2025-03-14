from django.shortcuts import render
from django.http import JsonResponse
from .models import Examen

def obtener_examenes(request):
    examenes = Examen.objects.all().values()
    return JsonResponse(list(examenes), safe=False)

