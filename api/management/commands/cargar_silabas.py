from django.core.management.base import BaseCommand
from api.models import PalabraModo2


class Command(BaseCommand):
    help = 'Carga las palabras de ejemplo para el juego de silabas'

    def handle(self, *args, **options):
        # Eliminar datos existentes
        PalabraModo2.objects.all().delete()
        self.stdout.write('Datos anteriores eliminados.')

        # Datos de ejemplo
        palabras_silabas = [
            {
                "nombre": "gato",
                "palabra_incompleta": "__to",
                "respuesta_correcta": "ga",
                "opciones": ["ga", "ca", "ta", "pa"],
                "imagen": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop",
                "audio": None
            },
            {
                "nombre": "perro",
                "palabra_incompleta": "pe__o",
                "respuesta_correcta": "rr",
                "opciones": ["rr", "ll", "ss", "nn"],
                "imagen": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop",
                "audio": None
            },
            {
                "nombre": "casa",
                "palabra_incompleta": "ca__",
                "respuesta_correcta": "sa",
                "opciones": ["sa", "za", "ta", "ma"],
                "imagen": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400&h=400&fit=crop",
                "audio": None
            },
            {
                "nombre": "sol",
                "palabra_incompleta": "__l",
                "respuesta_correcta": "so",
                "opciones": ["so", "sa", "se", "si"],
                "imagen": "https://images.unsplash.com/photo-1506596338381-f1c581d96c2c?w=400&h=400&fit=crop",
                "audio": None
            },
            {
                "nombre": "flor",
                "palabra_incompleta": "f__r",
                "respuesta_correcta": "lo",
                "opciones": ["lo", "la", "li", "le"],
                "imagen": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400&h=400&fit=crop",
                "audio": None
            },
            {
                "nombre": "mesa",
                "palabra_incompleta": "me__",
                "respuesta_correcta": "sa",
                "opciones": ["sa", "ta", "da", "na"],
                "imagen": "https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?w=400&h=400&fit=crop",
                "audio": None
            },
            {
                "nombre": "libro",
                "palabra_incompleta": "li__o",
                "respuesta_correcta": "br",
                "opciones": ["br", "pr", "tr", "cr"],
                "imagen": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=400&fit=crop",
                "audio": None
            },
            {
                "nombre": "arbol",
                "palabra_incompleta": "ar__l",
                "respuesta_correcta": "bo",
                "opciones": ["bo", "ba", "be", "bi"],
                "imagen": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=400&fit=crop",
                "audio": None
            },
            {
                "nombre": "luna",
                "palabra_incompleta": "lu__",
                "respuesta_correcta": "na",
                "opciones": ["na", "ma", "pa", "ta"],
                "imagen": "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=400&h=400&fit=crop",
                "audio": None
            },
            {
                "nombre": "pajaro",
                "palabra_incompleta": "pa__ro",
                "respuesta_correcta": "ja",
                "opciones": ["ja", "sa", "ca", "ra"],
                "imagen": "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400&h=400&fit=crop",
                "audio": None
            }
        ]

        # Crear las palabras
        for palabra_data in palabras_silabas:
            PalabraModo2.objects.create(**palabra_data)
            self.stdout.write(f'  Creada: {palabra_data["nombre"]}')

        self.stdout.write(self.style.SUCCESS(f'Se cargaron {len(palabras_silabas)} palabras exitosamente!'))
