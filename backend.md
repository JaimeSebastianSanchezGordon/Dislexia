# Backend - Django REST API

## 🚀 Instalación y configuración

### 1. Configurar el entorno virtual e instalar dependencias

```bash
# 1. Crear el entorno virtual (solo la primera vez)
python -m venv .venv

# 2. Activar entorno (Windows PowerShell)
.venv\Scripts\Activate.ps1
# (Windows CMD)
.venv\Scripts\activate.bat
# (GitBash)
source .venv/Scripts/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar la API de Google Gemini (OPCIONAL)

La aplicación puede funcionar sin API key usando palabras y oraciones de respaldo. Si quieres usar la generación dinámica con IA:

1. **Obtén tu API key** en [Google AI Studio](https://makersuite.google.com/app/apikey)

2. **Configura la key** en `Dislexia/settings.py`:
   ```python
   GEMINI_API_KEY = 'tu-api-key-aqui'
   ```

**Nota:** Sin API key configurada, el sistema usará automáticamente palabras y oraciones predefinidas. La aplicación funcionará perfectamente.

### 3. Ejecutar migraciones y servidor

```bash
# 4. Ejecutar migraciones (solo la primera vez o después de cambios en modelos)
python manage.py migrate

# 5. Iniciar el servidor de desarrollo
python manage.py runserver
```

## 📋 Endpoints disponibles

El servidor corre en: `http://127.0.0.1:8000/`

### 🎮 Juego de Anagramas
```
GET http://127.0.0.1:8000/api/juego1/?cantidad=3
```
Devuelve palabras aleatorias para el modo anagrama.
- **Parámetro opcional:** `cantidad` (2-8, por defecto 3)

### 🔤 Juego de Sílabas
```
GET http://127.0.0.1:8000/api/juego2/?cantidad=3
```
Devuelve palabras aleatorias para el modo sílabas.
- **Parámetro opcional:** `cantidad` (2-8, por defecto 3)
- **Mejora reciente:** Imágenes verificadas y consistentes con URLs directas de Unsplash

### 💬 Generar Oración (mejorado con IA + Coherencia Lógica)
```
POST http://127.0.0.1:8000/api/oracion/
Content-Type: application/json

{
  "palabra": "gato"
}
```
Genera una oración simple, natural, gramaticalmente correcta **y lógicamente coherente** para niños usando Google Gemini AI.

**Características:**
- ✅ Gramática perfecta con artículos correctos (el/la/un/una)
- ✅ **Concordancia de género perfecta** (favorita/favorito, nueva/nuevo, hermosa/hermoso, etc.)
- ✅ **COHERENCIA LÓGICA** - Usa características reales de cada palabra
- ✅ **23+ palabras con oraciones específicas verificadas** manualmente
- ✅ Lenguaje apropiado para niños de 7-12 años
- ✅ Oraciones de 5-10 palabras
- ✅ Sistema inteligente de respaldo con oraciones por categorías
- ✅ Detección automática de género de la palabra

**Ejemplos de coherencia lógica:**
- 🐢 "La tortuga camina despacio por el jardín" (tortugas son lentas)
- 🐇 "El conejo salta muy rápido" (conejos son rápidos)
- 🦋 "La mariposa vuela entre las flores" (mariposas vuelan)
- 🐠 "El pez nada en el agua" (peces nadan)
- ☀️ "El sol brilla en el cielo" (el sol da luz)

**Mejoras recientes:**
- ❌ Antes: "La tortuga corre muy rápido" (incorrecto)
- ✅ Ahora: "La tortuga camina despacio por el jardín" (correcto)

## 🎨 Sistema de Imágenes (NUEVO - Validación con IA)

El sistema ahora incluye **validación inteligente de imágenes usando Gemini Vision AI** para garantizar que las imágenes coincidan exactamente con las palabras:

### ✨ Características principales:
- **Validación automática con IA**: Cada imagen se verifica usando Gemini Vision antes de mostrarse
- **Detección de inconsistencias**: Si una imagen NO coincide con la palabra, busca automáticamente una alternativa
- **Mapeo estático de 50+ palabras** con imágenes verificadas manualmente
- **Búsqueda inteligente en Unsplash** con términos optimizados en inglés
- **Sistema de fallback robusto** para garantizar que siempre haya una imagen

### 🔍 Cómo funciona:
1. Primero intenta usar la imagen del mapeo estático
2. **Valida con IA** que la imagen realmente muestre lo que dice la palabra
3. Si la imagen NO es válida, busca alternativas en Unsplash
4. Valida cada alternativa con IA antes de aceptarla
5. Retorna la primera imagen que pase la validación

### 📝 Ejemplo de validación:
```
🔍 Validando imagen del mapeo para 'pelota'...
Validación: NO → INVÁLIDA (mostraba mochila)
❌ Buscando alternativa...
✅ ¡Imagen VÁLIDA encontrada!
```

### 🛠️ Dependencias necesarias:
- `Pillow==11.1.0` - Procesamiento de imágenes
- `requests==2.33.0` - Descarga y validación de imágenes
- `google-genai==1.10.1` - Gemini Vision AI (nuevo paquete oficial)
- `whitenoise==6.8.2` - Servir archivos estáticos en producción

**Nota:** El paquete `google-generativeai` está obsoleto y ha sido reemplazado por `google-genai`.

**Ventajas:**
- ✅ Imágenes consistentes y precisas (elimina errores como "pelota" mostrando mochila)
- ✅ Validación automática con IA (sin intervención manual)
- ✅ Mejora la experiencia educativa (niños ven imágenes correctas)
- ✅ Sistema robusto con múltiples fallbacks

Ver más detalles en: `VALIDACION_IMAGENES_IA.md`

## 🔧 Configuración

- **Base de datos**: SQLite (local, archivo `db.sqlite3`)
- **API Key de Gemini**: OPCIONAL - Configurable en `Dislexia/settings.py`
  - Con API key: Genera palabras y oraciones dinámicamente con IA
  - Sin API key: Usa palabras y oraciones predefinidas (funciona igual de bien)
- **CORS**: Habilitado para todos los orígenes (desarrollo)

## 🐳 Despliegue con Docker

El proyecto incluye configuración completa de Docker para desarrollo y producción.

### Usar Docker Compose

```bash
# Iniciar todos los servicios (backend + frontend + base de datos)
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### Script de ayuda (Windows PowerShell)

```powershell
# Ver todos los comandos disponibles
.\docker-helper.ps1 help

# Comandos principales
.\docker-helper.ps1 start          # Iniciar servicios
.\docker-helper.ps1 logs-api       # Ver logs del backend
.\docker-helper.ps1 migrate        # Ejecutar migraciones
.\docker-helper.ps1 createsuperuser # Crear usuario admin
.\docker-helper.ps1 clean          # Limpiar todo
```

**Puertos**:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- Base de datos: Puerto 5432 (PostgreSQL)

## 🚀 Despliegue en Render.com

El proyecto está configurado para desplegarse en Render.com usando Docker.

### Archivo de configuración: `render.yaml`

```yaml
services:
  - type: web
    name: dislexia-backend-docker
    env: docker
    dockerfilePath: ./Dockerfile
```

### Variables de entorno necesarias:
- `SECRET_KEY`: Clave secreta de Django (se genera automáticamente)
- `DEBUG`: False (en producción)
- `ALLOWED_HOSTS`: .onrender.com
- `GEMINI_API_KEY`: Tu API key de Google Gemini (opcional)
- `CORS_ALLOWED_ORIGINS`: URL de tu frontend (ej: https://tu-app.vercel.app)

### Script de build: `build.sh`

```bash
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Este script se ejecuta automáticamente en Render durante el despliegue.

## 📦 Dependencias de producción

El archivo `requirements.txt` incluye todas las dependencias necesarias:

```
Django>=5.0,<6.0              # Framework principal
djangorestframework>=3.14     # API REST
django-cors-headers>=4.0      # CORS para frontend
google-genai>=1.10.0          # Google Gemini AI
Pillow>=10.0                  # Procesamiento de imágenes
requests>=2.31.0              # HTTP requests
whitenoise>=6.0               # Servir archivos estáticos
```

**Nota**: Para despliegue con PostgreSQL, descomentar `psycopg2-binary>=2.9`

## ⚠️ Notas importantes

1. **El proyecto funciona sin necesidad de configurar la API key de Gemini**
   - Si `GEMINI_API_KEY` está vacía, usa contenido de respaldo automáticamente
   - No afecta la funcionalidad del juego
2. La ruta raíz `/` no tiene contenido - es normal ver un 404
3. El admin de Django está en: `http://127.0.0.1:8000/admin/`
4. Todas las rutas de la API están bajo `/api/`
5. El límite de Google Gemini es ~20 peticiones diarias (versión gratuita)
6. **Docker Helper** (`docker-helper.ps1`): Script útil para gestionar contenedores en Windows
7. **Build Script** (`build.sh`): Script de despliegue para Render.com/Railway
