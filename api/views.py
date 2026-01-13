from django.shortcuts import render

# Create your views here.
import google.generativeai as genai
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from .models import PalabraModo1, PalabraModo2
from .serializers import PalabraModo1Serializer, PalabraModo2Serializer


@api_view(['GET'])
def juego_anagrama(request):
    # .order_by('?') desordena y [:10] toma las primeras 10 palabras únicas
    palabras = PalabraModo1.objects.order_by('?')[:2]

    if palabras.exists():
        serializer = PalabraModo1Serializer(palabras, many=True)
        return Response(serializer.data)

    return Response({'error': 'No hay suficientes palabras'}, status=404)

@api_view(['GET'])
def juego_silabas(request):
    #palabras = PalabraModo2.objects.all()
    palabras = PalabraModo2.objects.order_by('?')[:1]
    serializer = PalabraModo2Serializer(palabras, many=True)
    return Response(serializer.data)

# Configuramos la IA usando la variable que pusimos en settings
genai.configure(api_key=settings.GEMINI_API_KEY)

@api_view(['POST'])
def generar_oracion(request):
    palabra = request.data.get('palabra')

    if not palabra:
        return Response({'error': 'No se proporcionó una palabra'}, status=400)

    try:
        # Usamos el modelo exacto de tu lista con mayor disponibilidad
        model = genai.GenerativeModel('gemma-3-4b-it')

        prompt = (f"Genera una oración con máximo de 10 palabras para un niño de 7 años, "
                  f"evita poner signos de exclamación, comas y puntos. "
                  f"Dentro de la oración pon esta palabra: {palabra}")

        response = model.generate_content(prompt)

        return Response({'oracion': response.text.strip()})
    except Exception as e:
        # Si superas las 20 peticiones diarias, este bloque evitará que el juego se rompa
        return Response({
            'oracion': f"La {palabra} es muy bonita.",
            'error': 'Límite diario alcanzado'
        })