from django.db import models

class Examen(models.Model):
    tipo = models.CharField(max_length=100)
    datos = models.JSONField()

    
