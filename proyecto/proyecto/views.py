from django.shortcuts import render
from django.http import JsonResponse
from examenes.models import Examen
import json

def index(request):
    return render(request, 'index.html')

def lista_pacientes(request):
    try:
        examen = Examen.objects.first()
        if isinstance(examen.datos, str):  # Solo cargar si es un string
            datos = json.loads(examen.datos)
        else:
            datos = examen.datos
        
        pacientes = [{"nombre": nombre, "id": nombre} for nombre in datos.keys()]
        return render(request, "pacientes.html", {"pacientes": pacientes})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def calcular_probabilidad_epilepsia_refractaria(eeg, mri, mirna, historia_clinica, test_neuropsicologico):
    probabilidad = 0
    
    for patron in eeg.get('patrones', []):
        frecuencia = float(patron['frecuencia'].replace(" Hz", ""))
        if frecuencia >= 2.5:
            probabilidad += 15
        elif frecuencia >= 1.5:
            probabilidad += 10
        else:
            probabilidad += 5
        
        if patron['tipo'] in ["Descargas Periódicas (PDs)", "Actividad Rítmica Delta (RDA)", "Descargas Rítmicas Potencialmente Ictales Breves (BIRDs)"]:
            probabilidad += 10
        
        if any(mod in patron['modificadores'] for mod in ["+F", "+R", "+S"]):
            probabilidad += 5
        if "evolución" in patron['modificadores']:
            probabilidad += 10
    
    for crisis in eeg.get('crisis', []):
        frecuencia_crisis = float(crisis['frecuencia'].replace(" Hz", ""))
        if frecuencia_crisis >= 2.5:
            probabilidad += 20
        else:
            probabilidad += 10
    
    for hallazgo in mri.get('hallazgos', []):
        if hallazgo['gravedad'] == "Moderada":
            probabilidad += 10
        elif hallazgo['gravedad'] == "Severa":
            probabilidad += 20
    
    for biomarcador in mirna.get('biomarcadores', []):
        if biomarcador['nivel_expresión'] == "Sobreexpresado":
            probabilidad += 5
    
    if historia_clinica['info_paciente']['historia_familiar']['epilepsia'] == "Si":
        probabilidad += 10
    if any(tratamiento['respuesta'] == "Ninguna" for tratamiento in historia_clinica.get('historia_tratamiento', [])):
        probabilidad += 20
    
    for funcion in test_neuropsicologico.get('funciones_cognitivas', []):
        if funcion['puntuación'] == "Por debajo del promedio":
            probabilidad += 5
    if test_neuropsicologico['evaluación_conductual']['depresión'] == "Moderada":
        probabilidad += 5
    
    return min(probabilidad, 100)

def detalle_paciente(request, paciente_id):
    try:
        paciente_id = paciente_id.replace("%20", " ")
        examen = Examen.objects.first()
        if isinstance(examen.datos, str):  # Solo cargar si es un string
            datos = json.loads(examen.datos)
        else:
            datos = examen.datos
        print(paciente_id)
        if paciente_id not in datos:
            return JsonResponse({"error": "Paciente no encontrado"})
        
        paciente_data = datos[paciente_id]
        print(paciente_data)
        probabilidad = calcular_probabilidad_epilepsia_refractaria(
            paciente_data['EEG'],
            paciente_data['MRI'],
            paciente_data['miRNA'],
            paciente_data['Historia Clínica'],
            paciente_data['Test Neuropsicológico']
        )
        
        diagnostico = f"Epilepsia refractaria probable ({probabilidad:.2f}%)" if probabilidad > 50 else f"Epilepsia no refractaria ({probabilidad:.2f}%)"

        return JsonResponse({"nombre": paciente_id, "probabilidad": probabilidad, "diagnostico": diagnostico})
    except Exception as e:
        return JsonResponse({"error": str(e)})
