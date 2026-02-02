from django.shortcuts import render
from google import genai
from google.genai import types
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import PalabraModo1, PalabraModo2
from .serializers import PalabraModo1Serializer, PalabraModo2Serializer
import json
import random
import requests
from io import BytesIO
from PIL import Image
import base64

# Configurar Gemini
def get_gemini_client():
    """Obtiene el cliente de Gemini configurado"""
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if api_key and api_key.strip():
        client = genai.Client(api_key=api_key)
        return client
    return None

def validar_imagen_con_palabra(client, imagen_url, palabra):
    """
    Valida que una imagen corresponda a la palabra usando Gemini Vision.
    Retorna True si coincide, False si no.
    """
    try:
        # Descargar la imagen
        response = requests.get(imagen_url, timeout=10)
        if response.status_code != 200:
            print(f"Error descargando imagen para '{palabra}': HTTP {response.status_code}")
            return False

        # Crear prompt de validación más estricto
        prompt = f"""Analiza cuidadosamente esta imagen y determina si muestra un/una {palabra}.

REGLAS ESTRICTAS:
- Responde "SI" SOLO si la imagen muestra CLARAMENTE un/una {palabra}
- Responde "NO" si muestra cualquier otra cosa diferente (aunque sea similar)
- La imagen debe ser inequívoca y reconocible como {palabra}
- NO aceptes objetos similares o relacionados, debe ser EXACTAMENTE un/una {palabra}

Ejemplos:
- Si busco "pelota" y veo una mochila → NO
- Si busco "pelota" y veo una pelota → SI
- Si busco "gato" y veo un perro → NO
- Si busco "gato" y veo un gato → SI

Responde ÚNICAMENTE con: SI o NO (nada más)"""

        # Guardar imagen temporalmente
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name

        # Subir imagen a Gemini usando el nuevo API
        uploaded_file = client.files.upload(path=tmp_path)

        # Usar Gemini Vision para validar
        vision_response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=[uploaded_file, prompt]
        )

        # Limpiar archivo temporal
        import os
        os.unlink(tmp_path)

        respuesta = vision_response.text.strip().upper()
        es_valida = "SI" in respuesta or "YES" in respuesta

        print(f"Validación de imagen para '{palabra}': {respuesta} → {'VÁLIDA' if es_valida else 'INVÁLIDA'}")
        return es_valida

    except Exception as e:
        print(f"Error validando imagen para '{palabra}': {e}")
        return False

def buscar_imagen_validada_unsplash(client, palabra, max_intentos=5):
    """
    Busca una imagen en Unsplash que realmente corresponda a la palabra.
    Usa IA para validar cada imagen antes de aceptarla.
    Retorna la URL de la imagen validada o None si no encuentra ninguna.
    """
    try:
        # Traducir búsquedas comunes para mejorar resultados
        terminos_busqueda = {
            'pelota': ['soccer ball', 'football ball', 'sports ball'],
            'gato': ['cat face', 'domestic cat', 'kitten'],
            'perro': ['dog face', 'puppy dog', 'domestic dog'],
            'casa': ['small house', 'cottage', 'home exterior'],
            'mesa': ['wooden table', 'dining table', 'furniture table'],
            'zapato': ['shoe', 'sneaker', 'footwear'],
            'pato': ['duck bird', 'mallard duck'],
            'conejo': ['rabbit bunny', 'cute rabbit'],
            'elefante': ['elephant', 'african elephant'],
            'caballo': ['horse', 'brown horse'],
            'pajaro': ['bird', 'songbird'],
            'pez': ['fish', 'goldfish'],
            'leon': ['lion', 'male lion'],
            'tigre': ['tiger', 'bengal tiger'],
            'oso': ['bear', 'brown bear'],
            'mariposa': ['butterfly', 'colorful butterfly'],
            'tortuga': ['turtle', 'tortoise'],
            'vaca': ['cow', 'dairy cow'],
            'gallina': ['chicken', 'hen'],
            'oveja': ['sheep', 'lamb'],
            'sol': ['sun', 'sunset sun', 'sunrise'],
            'luna': ['moon', 'full moon'],
            'flor': ['flower', 'blooming flower'],
            'estrella': ['star', 'night stars'],
            'nube': ['cloud', 'white cloud'],
            'arbol': ['tree', 'oak tree'],
            'montana': ['mountain', 'mountain peak'],
            'rio': ['river', 'flowing river'],
            'playa': ['beach', 'sandy beach'],
            'mar': ['ocean', 'sea water'],
            'manzana': ['apple', 'red apple'],
            'pan': ['bread', 'fresh bread'],
            'agua': ['water', 'glass of water'],
            'leche': ['milk', 'glass of milk'],
            'queso': ['cheese', 'yellow cheese'],
            'naranja': ['orange fruit', 'orange citrus'],
            'platano': ['banana', 'yellow banana'],
            'uva': ['grapes', 'grape bunch'],
            'pera': ['pear', 'green pear'],
            'sandia': ['watermelon', 'watermelon slice'],
            'ventana': ['window', 'open window'],
            'silla': ['chair', 'wooden chair'],
        }

        palabra_normalizada = palabra.lower().strip()
        terminos = terminos_busqueda.get(palabra_normalizada, [palabra])

        print(f"\n🔍 Buscando imagen validada para '{palabra}'...")

        for termino in terminos:
            print(f"  → Probando término de búsqueda: '{termino}'")

            # Buscar en Unsplash (usando IDs aleatorios de búsqueda)
            # Nota: Unsplash requiere API key para búsquedas, por ahora usamos URLs directas
            # pero con validación IA
            base_urls = [
                f"https://source.unsplash.com/400x400/?{termino.replace(' ', ',')}",
                f"https://source.unsplash.com/featured/400x400/?{termino.replace(' ', ',')}",
            ]

            for intento, base_url in enumerate(base_urls):
                if intento >= max_intentos:
                    break

                # Agregar timestamp para obtener diferentes imágenes
                import time
                url_con_cache = f"{base_url}&t={int(time.time())}{intento}"

                print(f"    → Intento {intento + 1}: Validando imagen...")

                # Validar la imagen con IA
                if validar_imagen_con_palabra(client, url_con_cache, palabra):
                    print(f"    ✅ ¡Imagen VÁLIDA encontrada para '{palabra}'!")
                    # Obtener la URL final después de la redirección
                    try:
                        final_response = requests.get(url_con_cache, timeout=10, allow_redirects=True)
                        return final_response.url
                    except:
                        return url_con_cache

        print(f"  ❌ No se encontró imagen válida para '{palabra}' después de {max_intentos} intentos")
        return None

    except Exception as e:
        print(f"Error buscando imagen para '{palabra}': {e}")
        return None

def obtener_palabras_validadas(client, cantidad, tipo_juego='anagrama'):
    """
    Genera palabras y valida que las imágenes coincidan.
    Si una imagen no coincide, usa la del mapeo IMAGENES_UNSPLASH.
    """
    max_intentos = 3
    palabras_validas = []

    for intento in range(max_intentos):
        if len(palabras_validas) >= cantidad:
            break

        # Generar palabras según el tipo de juego
        if tipo_juego == 'anagrama':
            palabras_candidatas = generar_palabras_anagrama_raw(client, cantidad)
        else:  # silabas
            palabras_candidatas = generar_palabras_silabas_raw(client, cantidad)

        for palabra_data in palabras_candidatas:
            if len(palabras_validas) >= cantidad:
                break

            nombre = palabra_data['nombre'].lower().strip()

            # Primero intentar con imagen del mapeo (más confiable)
            if nombre in IMAGENES_UNSPLASH:
                palabra_data['imagen'] = IMAGENES_UNSPLASH[nombre]
                palabra_data['validada'] = True
                palabras_validas.append(palabra_data)
                continue

            # Si no está en el mapeo, validar la imagen generada
            # (esto requeriría obtener la imagen de Unsplash primero)
            # Por ahora, si no está en el mapeo, usar una palabra de respaldo
            print(f"Palabra '{nombre}' no está en el mapeo, saltando...")

    return palabras_validas

def generar_palabras_anagrama_raw(client, cantidad):
    """Genera palabras para anagrama sin validación"""
    categoria = random.choice(CATEGORIAS_PALABRAS)

    prompt = f"""Genera exactamente {cantidad} palabras en español para un juego educativo de niños de 7 años.
    Categoría: {categoria}

    REGLAS IMPORTANTES:
    - Palabras de 3 a 6 letras solamente
    - Sin tildes ni caracteres especiales
    - Palabras comunes que un niño conoce
    - Todas las letras en minúscula
    - SOLO USA PALABRAS DE ESTA LISTA: gato, perro, pato, conejo, elefante, caballo, pajaro, pez, leon, tigre, oso, mariposa, tortuga, vaca, gallina, oveja, casa, mesa, pelota, zapato, ventana, silla, sol, luna, flor, estrella, nube, arbol, montana, rio, playa, mar, manzana, pan, agua, leche, queso, naranja, platano, uva, pera, sandia

    Responde SOLO con un JSON válido con este formato exacto, sin texto adicional:
    [
        {{"nombre": "gato"}},
        {{"nombre": "perro"}},
        {{"nombre": "manzana"}}
    ]
    """

    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=prompt
    )

    texto = response.text.strip()
    if texto.startswith("```json"):
        texto = texto[7:]
    if texto.startswith("```"):
        texto = texto[3:]
    if texto.endswith("```"):
        texto = texto[:-3]
    texto = texto.strip()

    return json.loads(texto)

def generar_palabras_silabas_raw(client, cantidad):
    """Genera palabras para sílabas sin validación"""
    categoria = random.choice(CATEGORIAS_PALABRAS)

    prompt = f"""Genera exactamente {cantidad} palabras en español para un juego educativo de sílabas para niños de 7 años.
    Categoría: {categoria}

    REGLAS IMPORTANTES:
    - Palabras de 2 a 4 sílabas
    - Sin tildes ni caracteres especiales
    - Palabras comunes que un niño conoce
    - Todas las letras en minúscula
    - SOLO USA PALABRAS DE ESTA LISTA: gato, perro, pato, conejo, elefante, caballo, pajaro, pez, leon, tigre, oso, mariposa, tortuga, vaca, gallina, oveja, casa, mesa, pelota, zapato, ventana, silla, sol, luna, flor, estrella, nube, arbol, montana, rio, playa, mar, manzana, pan, agua, leche, queso, naranja, platano, uva, pera, sandia

    Para cada palabra incluye:
    - Las sílabas separadas
    - El índice de una sílaba para ocultar (0, 1, 2...)
    - 4 opciones de sílabas (la correcta + 3 incorrectas similares)

    Responde SOLO con un JSON válido con este formato exacto, sin texto adicional:
    [
        {{
            "nombre": "mariposa",
            "silabas": ["ma", "ri", "po", "sa"],
            "silaba_oculta": 2,
            "opciones": ["po", "pe", "pa", "pi"]
        }}
    ]
    """

    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=prompt
    )

    texto = response.text.strip()
    if texto.startswith("```json"):
        texto = texto[7:]
    if texto.startswith("```"):
        texto = texto[3:]
    if texto.endswith("```"):
        texto = texto[:-3]
    texto = texto.strip()

    return json.loads(texto)

def obtener_imagen_palabra(palabra, client=None):
    """
    Obtiene la URL de imagen para una palabra
    Si client (Gemini) está disponible, valida que la imagen coincida con la palabra.
    Si no coincide, busca una imagen alternativa validada.
    """
    # Normalizar la palabra (quitar tildes y convertir a minúsculas)
    palabra_normalizada = palabra.lower().strip()

    # Primero intentar con el mapeo directo
    if palabra_normalizada in IMAGENES_UNSPLASH:
        url_mapeo = IMAGENES_UNSPLASH[palabra_normalizada]

        # Si tenemos client de Gemini, validar la imagen
        if client:
            print(f"\n🔍 Validando imagen del mapeo para '{palabra}'...")
            if validar_imagen_con_palabra(client, url_mapeo, palabra):
                print(f"✅ Imagen del mapeo es válida para '{palabra}'")
                return url_mapeo
            else:
                print(f"❌ Imagen del mapeo NO es válida para '{palabra}', buscando alternativa...")
                # Buscar imagen alternativa validada
                url_validada = buscar_imagen_validada_unsplash(client, palabra, max_intentos=3)
                if url_validada:
                    return url_validada
                else:
                    print(f"⚠️ No se encontró alternativa, usando imagen del mapeo de todas formas")
                    return url_mapeo
        else:
            # Sin client, confiar en el mapeo
            return url_mapeo

    # Si no está en el mapeo y tenemos client, buscar con validación
    if client:
        print(f"\n🔍 Palabra '{palabra}' no está en mapeo, buscando con validación IA...")
        url_validada = buscar_imagen_validada_unsplash(client, palabra, max_intentos=5)
        if url_validada:
            return url_validada

    # Imagen de respaldo genérica
    print(f"⚠️ Usando imagen de respaldo genérica para '{palabra}'")
    return "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=400&h=400&fit=crop"

# Lista de categorías para palabras de niños
CATEGORIAS_PALABRAS = [
    "animales domésticos", "animales de granja", "frutas", "verduras",
    "colores", "juguetes", "partes del cuerpo", "ropa", "alimentos",
    "objetos de la casa", "medios de transporte", "naturaleza"
]

# Palabras de respaldo por si falla la API
PALABRAS_RESPALDO_ANAGRAMA = [
    {"nombre": "gato", "imagen": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400", "palabra_dividida_letras": "g-a-t-o"},
    {"nombre": "perro", "imagen": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400", "palabra_dividida_letras": "p-e-r-r-o"},
    {"nombre": "casa", "imagen": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400", "palabra_dividida_letras": "c-a-s-a"},
    {"nombre": "mesa", "imagen": "https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=400", "palabra_dividida_letras": "m-e-s-a"},
    {"nombre": "luna", "imagen": "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=400", "palabra_dividida_letras": "l-u-n-a"},
    {"nombre": "sol", "imagen": "https://images.unsplash.com/photo-1496450681664-3df85efbd29f?w=400", "palabra_dividida_letras": "s-o-l"},
    {"nombre": "flor", "imagen": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400", "palabra_dividida_letras": "f-l-o-r"},
    {"nombre": "pato", "imagen": "https://images.unsplash.com/photo-1459682687441-7761439a709d?w=400", "palabra_dividida_letras": "p-a-t-o"},
]

PALABRAS_RESPALDO_SILABAS = [
    {"nombre": "mariposa", "imagen": "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=400", "silabas": ["ma", "ri", "po", "sa"], "silaba_oculta": 2, "opciones": ["po", "pe", "pa", "pi"]},
    {"nombre": "elefante", "imagen": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=400", "silabas": ["e", "le", "fan", "te"], "silaba_oculta": 1, "opciones": ["le", "la", "lo", "li"]},
    {"nombre": "conejo", "imagen": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400", "silabas": ["co", "ne", "jo"], "silaba_oculta": 1, "opciones": ["ne", "na", "no", "ni"]},
    {"nombre": "tortuga", "imagen": "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=400", "silabas": ["tor", "tu", "ga"], "silaba_oculta": 2, "opciones": ["ga", "go", "gu", "ge"]},
    {"nombre": "pelota", "imagen": "https://images.unsplash.com/photo-1614632537197-38a17061c2bd?w=400", "silabas": ["pe", "lo", "ta"], "silaba_oculta": 1, "opciones": ["lo", "la", "le", "lu"]},
    {"nombre": "zapato", "imagen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "silabas": ["za", "pa", "to"], "silaba_oculta": 0, "opciones": ["za", "ze", "zo", "zu"]},
    {"nombre": "caballo", "imagen": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400", "silabas": ["ca", "ba", "llo"], "silaba_oculta": 1, "opciones": ["ba", "be", "bi", "bo"]},
    {"nombre": "ventana", "imagen": "https://images.unsplash.com/photo-1509644851169-2acc08aa25b5?w=400", "silabas": ["ven", "ta", "na"], "silaba_oculta": 2, "opciones": ["na", "ne", "no", "nu"]},
]

# Mapeo de palabras a URLs específicas de Unsplash (IDs confiables)
IMAGENES_UNSPLASH = {
    # Animales
    "gato": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop",
    "perro": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop",
    "pato": "https://images.unsplash.com/photo-1459682687441-7761439a709d?w=400&h=400&fit=crop",
    "conejo": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400&h=400&fit=crop",
    "elefante": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=400&h=400&fit=crop",
    "caballo": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400&h=400&fit=crop",
    "pájaro": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400&h=400&fit=crop",
    "pajaro": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400&h=400&fit=crop",
    "pez": "https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=400&h=400&fit=crop",
    "león": "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=400&fit=crop",
    "leon": "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=400&fit=crop",
    "tigre": "https://images.unsplash.com/photo-1551492910-2f0acb2e8115?w=400&h=400&fit=crop",
    "oso": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=400&h=400&fit=crop",
    "mariposa": "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=400&h=400&fit=crop",  # Mariposa monarca naranja
    "tortuga": "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=400&h=400&fit=crop",
    "vaca": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=400&h=400&fit=crop",
    "gallina": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400&h=400&fit=crop",
    "oveja": "https://images.unsplash.com/photo-1551913902-c92207b5dc7c?w=400&h=400&fit=crop",
    # Objetos
    "casa": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400&h=400&fit=crop",
    "mesa": "https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=400&h=400&fit=crop",
    "pelota": "https://images.unsplash.com/photo-1614632537197-38a17061c2bd?w=400&h=400&fit=crop",  # Pelota de fútbol real
    "zapato": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
    "ventana": "https://images.unsplash.com/photo-1509644851169-2acc08aa25b5?w=400&h=400&fit=crop",
    "silla": "https://images.unsplash.com/photo-1503602642458-232111445657?w=400&h=400&fit=crop",
    # Naturaleza
    "sol": "https://images.unsplash.com/photo-1496450681664-3df85efbd29f?w=400&h=400&fit=crop",
    "luna": "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=400&h=400&fit=crop",
    "flor": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400&h=400&fit=crop",
    "estrella": "https://images.unsplash.com/photo-1519810755548-39cd217da494?w=400&h=400&fit=crop",
    "nube": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=400&h=400&fit=crop",
    "árbol": "https://images.unsplash.com/photo-1541516160071-4bb0c5af65ba?w=400&h=400&fit=crop",
    "arbol": "https://images.unsplash.com/photo-1541516160071-4bb0c5af65ba?w=400&h=400&fit=crop",
    "montaña": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop",
    "montana": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop",
    "río": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400&h=400&fit=crop",
    "rio": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400&h=400&fit=crop",
    "playa": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=400&fit=crop",
    "mar": "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400&h=400&fit=crop",
    # Alimentos
    "manzana": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&h=400&fit=crop",
    "pan": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop",
    "agua": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400&h=400&fit=crop",
    "leche": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&h=400&fit=crop",
    "queso": "https://images.unsplash.com/photo-1452195100486-9cc805987862?w=400&h=400&fit=crop",
    "naranja": "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=400&h=400&fit=crop",
    "plátano": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=400&fit=crop",
    "platano": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=400&fit=crop",
    "uva": "https://images.unsplash.com/photo-1596363505729-4190a9506133?w=400&h=400&fit=crop",
    "pera": "https://images.unsplash.com/photo-1568570935644-e9c96a60b7f2?w=400&h=400&fit=crop",
    "sandía": "https://images.unsplash.com/photo-1589984662646-e7b2e4962f18?w=400&h=400&fit=crop",
    "sandia": "https://images.unsplash.com/photo-1589984662646-e7b2e4962f18?w=400&h=400&fit=crop",
}


@api_view(['GET'])
def juego_anagrama(request):
    """Genera palabras aleatorias para el juego de anagramas usando Gemini con validación de imágenes"""
    # Obtener cantidad desde query params, por defecto 3
    cantidad = int(request.GET.get('cantidad', 3))
    # Limitar entre 2 y 8 palabras
    cantidad = max(2, min(8, cantidad))

    try:
        client = get_gemini_client()
        if not client:
            raise ValueError("Gemini API key not configured")

        # Obtener palabras validadas
        palabras_validadas = obtener_palabras_validadas(client, cantidad, tipo_juego='anagrama')

        # Procesar palabras validadas
        palabras_procesadas = []
        for palabra_data in palabras_validadas:
            nombre = palabra_data['nombre'].lower().strip()

            # Usar imagen validada con IA
            imagen_url = obtener_imagen_palabra(nombre, client=client)

            palabras_procesadas.append({
                "nombre": nombre,
                "imagen": imagen_url,
                "palabra_dividida_letras": "-".join(list(nombre))
            })

        # Si no se obtuvieron suficientes palabras validadas, completar con respaldo
        if len(palabras_procesadas) < cantidad:
            faltantes = cantidad - len(palabras_procesadas)
            palabras_respaldo = random.sample(
                PALABRAS_RESPALDO_ANAGRAMA,
                min(faltantes, len(PALABRAS_RESPALDO_ANAGRAMA))
            )
            palabras_procesadas.extend(palabras_respaldo)

        return Response(palabras_procesadas[:cantidad])

    except Exception as e:
        print(f"Error en juego_anagrama: {e}")
        # Usar palabras de respaldo
        palabras = random.sample(PALABRAS_RESPALDO_ANAGRAMA, min(cantidad, len(PALABRAS_RESPALDO_ANAGRAMA)))
        return Response(palabras)


@api_view(['GET'])
def juego_silabas(request):
    """Genera palabras aleatorias para el juego de sílabas usando Gemini con validación de imágenes"""
    # Obtener cantidad desde query params, por defecto 3
    cantidad = int(request.GET.get('cantidad', 3))
    # Limitar entre 2 y 8 palabras
    cantidad = max(2, min(8, cantidad))

    try:
        client = get_gemini_client()
        if not client:
            raise ValueError("Gemini API key not configured")

        # Obtener palabras validadas
        palabras_validadas = obtener_palabras_validadas(client, cantidad, tipo_juego='silabas')

        # Procesar palabras validadas
        palabras_procesadas = []
        for palabra_data in palabras_validadas:
            nombre = palabra_data['nombre'].lower().strip()

            # Usar imagen validada con IA
            imagen_url = obtener_imagen_palabra(nombre, client=client)

            # Asegurar que las opciones incluyan la sílaba correcta
            silaba_correcta = palabra_data['silabas'][palabra_data['silaba_oculta']]
            opciones = palabra_data['opciones']
            if silaba_correcta not in opciones:
                opciones[0] = silaba_correcta
            random.shuffle(opciones)

            palabras_procesadas.append({
                "nombre": nombre,
                "imagen": imagen_url,
                "silabas": palabra_data['silabas'],
                "silaba_oculta": palabra_data['silaba_oculta'],
                "opciones": opciones
            })

        # Si no se obtuvieron suficientes palabras validadas, completar con respaldo
        if len(palabras_procesadas) < cantidad:
            faltantes = cantidad - len(palabras_procesadas)
            palabras_respaldo = random.sample(
                PALABRAS_RESPALDO_SILABAS,
                min(faltantes, len(PALABRAS_RESPALDO_SILABAS))
            )
            palabras_procesadas.extend(palabras_respaldo)

        return Response(palabras_procesadas[:cantidad])

    except Exception as e:
        print(f"Error en juego_silabas: {e}")
        # Usar palabras de respaldo
        palabras = random.sample(PALABRAS_RESPALDO_SILABAS, min(cantidad, len(PALABRAS_RESPALDO_SILABAS)))
        return Response(palabras)


@api_view(['POST'])
def generar_oracion(request):
    """Genera una oración usando la palabra proporcionada"""
    palabra = request.data.get('palabra')

    if not palabra:
        return Response({'error': 'No se proporcionó una palabra'}, status=400)

    try:
        client = get_gemini_client()
        if not client:
            raise ValueError("Gemini API key not configured")

        prompt = f"""Genera UNA SOLA oración simple, natural y LÓGICA para un niño de 7 años que incluya la palabra: {palabra}

REGLAS IMPORTANTES:
- La oración debe tener entre 5 y 10 palabras
- Usa un lenguaje claro y sencillo apropiado para niños
- Utiliza correctamente los artículos (el/la/un/una) según el género de la palabra
- La oración debe describir características REALES y VERDADERAS de la palabra
- USA SENTIDO COMÚN: describe la palabra con atributos que realmente tenga
- NO uses signos de exclamación, comas ni puntos al final
- Asegúrate de que la gramática sea perfecta
- La oración debe sonar natural cuando un niño la lea en voz alta

IMPORTANTE - COHERENCIA LÓGICA:
- Si es un animal lento (tortuga, caracol), NO digas que es rápido
- Si es un animal rápido (conejo, león), NO digas que es lento
- Si vuela (pájaro, mariposa), menciona que vuela
- Si nada (pez, ballena), menciona que nada
- Usa las características VERDADERAS de cada cosa

Ejemplos de oraciones CORRECTAS con sentido común:
- "El gato duerme tranquilo en su cama" ✓
- "La mariposa vuela entre las flores del jardín" ✓
- "La tortuga camina despacio por el jardín" ✓ (tortugas son lentas)
- "El conejo salta muy rápido" ✓ (conejos son rápidos)
- "El sol brilla en el cielo azul" ✓

Ejemplos de oraciones INCORRECTAS (NO hacer):
- "La tortuga corre muy rápido" ✗ (las tortugas son lentas)
- "El caracol es muy veloz" ✗ (los caracoles son lentos)
- "El pez camina en el parque" ✗ (los peces nadan)

Responde SOLO con la oración, sin texto adicional."""

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )

        # Limpiar la respuesta
        oracion = response.text.strip()
        # Remover puntos finales si los hay
        oracion = oracion.rstrip('.,!?')

        return Response({'oracion': oracion})

    except Exception as e:
        # Sistema inteligente de oraciones de respaldo
        print(f"Error generando oración: {e}")

        # Diccionario de oraciones específicas con sentido común para cada palabra
        oraciones_especificas = {
            # Animales rápidos
            'gato': [
                "El gato duerme tranquilo en su cama",
                "Mi gato juega con una pelota",
                "El gato salta sobre la mesa",
                "Veo un gato que camina en el jardín"
            ],
            'perro': [
                "El perro corre rápido en el parque",
                "Mi perro mueve la cola cuando me ve",
                "El perro ladra cuando alguien llega",
                "Veo un perro que juega con su pelota"
            ],
            'conejo': [
                "El conejo salta muy rápido",
                "Mi conejo come zanahorias",
                "El conejo tiene orejas largas",
                "Veo un conejo blanco en el jardín"
            ],
            'caballo': [
                "El caballo corre muy rápido",
                "Mi caballo galopa en el campo",
                "El caballo es grande y fuerte",
                "Veo un caballo café en la granja"
            ],
            # Animales lentos
            'tortuga': [
                "La tortuga camina despacio por el jardín",
                "Mi tortuga nada en el agua",
                "La tortuga tiene un caparazón duro",
                "Veo una tortuga que descansa al sol"
            ],
            # Animales que vuelan
            'pájaro': [
                "El pájaro vuela alto en el cielo",
                "Mi pájaro canta en su jaula",
                "El pájaro tiene plumas de colores",
                "Veo un pájaro en el árbol"
            ],
            'pajaro': [
                "El pájaro vuela alto en el cielo",
                "Mi pájaro canta en su jaula",
                "El pájaro tiene plumas de colores",
                "Veo un pájaro en el árbol"
            ],
            'mariposa': [
                "La mariposa vuela entre las flores",
                "Mi mariposa tiene alas de colores",
                "La mariposa se posa en una flor",
                "Veo una mariposa bonita en el jardín"
            ],
            # Animales que nadan
            'pez': [
                "El pez nada en el agua",
                "Mi pez vive en la pecera",
                "El pez tiene escamas brillantes",
                "Veo un pez de colores nadando"
            ],
            # Otros animales
            'pato': [
                "El pato nada en el lago",
                "Mi pato hace cuac cuac",
                "El pato tiene plumas amarillas",
                "Veo un pato nadando en el agua"
            ],
            'elefante': [
                "El elefante es grande y fuerte",
                "Mi elefante tiene trompa larga",
                "El elefante vive en la selva",
                "Veo un elefante en el zoológico"
            ],
            'león': [
                "El león es el rey de la selva",
                "Mi león ruge muy fuerte",
                "El león corre rápido cuando caza",
                "Veo un león descansando"
            ],
            'leon': [
                "El león es el rey de la selva",
                "Mi león ruge muy fuerte",
                "El león corre rápido cuando caza",
                "Veo un león descansando"
            ],
            'vaca': [
                "La vaca nos da leche",
                "Mi vaca come pasto en el campo",
                "La vaca hace muuu",
                "Veo una vaca en la granja"
            ],
            'gallina': [
                "La gallina pone huevos",
                "Mi gallina cacarea en el corral",
                "La gallina tiene plumas suaves",
                "Veo una gallina con sus pollitos"
            ],
            # Naturaleza
            'sol': [
                "El sol brilla en el cielo",
                "El sol nos da luz y calor",
                "El sol sale todas las mañanas",
                "Veo el sol muy brillante hoy"
            ],
            'luna': [
                "La luna brilla en la noche",
                "La luna sale cuando oscurece",
                "La luna es redonda y blanca",
                "Veo la luna en el cielo nocturno"
            ],
            'flor': [
                "La flor huele muy rico",
                "Mi flor tiene pétalos de colores",
                "La flor crece en el jardín",
                "Veo una flor roja muy bonita"
            ],
            'estrella': [
                "La estrella brilla en la noche",
                "Mi estrella favorita está en el cielo",
                "La estrella titila muy bonito",
                "Veo muchas estrellas en la noche"
            ],
            # Alimentos
            'manzana': [
                "La manzana es roja y dulce",
                "Mi manzana está muy rica",
                "La manzana es mi fruta favorita",
                "Como una manzana en el recreo"
            ],
            'pan': [
                "El pan está caliente y suave",
                "Mi pan huele muy rico",
                "El pan es mi alimento favorito",
                "Como pan con mantequilla"
            ],
        }

        # Si existe oración específica, usarla
        palabra_lower = palabra.lower()
        if palabra_lower in oraciones_especificas:
            return Response({
                'oracion': random.choice(oraciones_especificas[palabra_lower])
            })

        # Diccionario de palabras comunes con su género
        palabras_femeninas = {
            'casa', 'mesa', 'flor', 'luna', 'pelota', 'mariposa',
            'tortuga', 'ventana', 'silla', 'manzana', 'pera', 'uva',
            'estrella', 'nube', 'montaña', 'playa', 'vaca', 'gallina',
            'oveja', 'abeja', 'hormiga', 'araña', 'rana', 'ballena'
        }

        # Determinar género
        es_femenina = palabra.lower().endswith('a') or palabra.lower() in palabras_femeninas
        articulo_def = 'la' if es_femenina else 'el'
        articulo_indef = 'una' if es_femenina else 'un'
        adjetivo_bonito = 'bonita' if es_femenina else 'bonito'
        adjetivo_favorito = 'favorita' if es_femenina else 'favorito'
        adjetivo_nuevo = 'nueva' if es_femenina else 'nuevo'
        adjetivo_hermoso = 'hermosa' if es_femenina else 'hermoso'
        adjetivo_delicioso = 'deliciosa' if es_femenina else 'delicioso'
        adjetivo_rico = 'rica' if es_femenina else 'rico'

        # Plantillas genéricas (solo para palabras sin oraciones específicas)
        oraciones_animales = [
            f"Veo {articulo_indef} {palabra} en el jardín",
            f"Mi {palabra} {adjetivo_favorito} vive cerca de mi casa",
            f"Me gusta observar a {articulo_def} {palabra}",
            f"{articulo_def.capitalize()} {palabra} es muy {adjetivo_bonito}"
        ]

        oraciones_objetos = [
            f"Tengo {articulo_indef} {palabra} {adjetivo_bonito} en mi cuarto",
            f"Mi mamá me compró {articulo_indef} {palabra} {adjetivo_nuevo}",
            f"{articulo_def.capitalize()} {palabra} está sobre la mesa",
            f"Me gusta jugar con mi {palabra}",
            f"Veo {articulo_indef} {palabra} de color azul"
        ]

        oraciones_naturaleza = [
            f"{articulo_def.capitalize()} {palabra} brilla en el cielo",
            f"Miro {articulo_def} {palabra} desde mi ventana",
            f"Me encanta {articulo_def} {palabra} de la mañana",
            f"{articulo_def.capitalize()} {palabra} es {adjetivo_hermoso} hoy",
            f"Dibujé {articulo_indef} {palabra} en mi cuaderno"
        ]

        oraciones_alimentos = [
            f"Me gusta comer {palabra} en el desayuno",
            f"{articulo_def.capitalize()} {palabra} está muy {adjetivo_rico}",
            f"Mi mamá prepara {palabra} {adjetivo_delicioso}",
            f"Compré {articulo_indef} {palabra} en el mercado",
            f"{articulo_def.capitalize()} {palabra} es mi {adjetivo_favorito}"
        ]

        # Intentar categorizar la palabra
        palabra_lower = palabra.lower()

        if palabra_lower in ['gato', 'perro', 'pato', 'conejo', 'elefante', 'caballo',
                             'pájaro', 'pez', 'león', 'tigre', 'oso', 'mariposa',
                             'tortuga', 'vaca', 'gallina', 'oveja']:
            oraciones_pool = oraciones_animales
        elif palabra_lower in ['sol', 'luna', 'estrella', 'nube', 'flor', 'árbol',
                               'montaña', 'río', 'playa', 'mar']:
            oraciones_pool = oraciones_naturaleza
        elif palabra_lower in ['manzana', 'pan', 'agua', 'leche', 'queso', 'naranja',
                               'plátano', 'uva', 'pera', 'sandía']:
            oraciones_pool = oraciones_alimentos
        else:
            oraciones_pool = oraciones_objetos

        return Response({
            'oracion': random.choice(oraciones_pool),
            'info': 'Oración generada automáticamente'
        })
