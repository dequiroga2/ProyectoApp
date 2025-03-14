from django.db import models

class Examen(models.Model):
    tipo = models.CharField(max_length=100)
    datos = models.JSONField()

    def tiene_epilepsia(self):
        if "EEG" in self.datos:
            for categoria in self.datos["EEG"].values():
                if isinstance(categoria, list):
                    for examen in categoria:
                        if examen.get("frecuencia") == "5 Hz":
                            return "Tiene epilepsia"
        return "No tiene epilepsia"

