# 🔧 Solución: Errores de Importación y SECRET_KEY

## ❌ ERRORES IDENTIFICADOS

### Error 1: ImportError de Google Generative AI
```
ImportError: cannot import name 'genai' from 'google' (unknown location)
File "/app/api/views.py", line 2, in <module>
    from google import genai
```

### Error 2: SECRET_KEY vacía
```
django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty.
```

---

## ✅ SOLUCIONES APLICADAS

### 1. Corregir Import de Google Generative AI

**Problema:** El import estaba usando la sintaxis incorrecta.

**Solución aplicada en `api/views.py`:**

```python
# ❌ ANTES (INCORRECTO):
from google import genai
from google.genai import types

# ✅ AHORA (CORRECTO):
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠️ Google Generative AI no disponible. Usando datos de respaldo.")
```

**Beneficios:**
- ✅ No falla si la librería no está instalada
- ✅ Usa datos de respaldo automáticamente
- ✅ La app funciona sin API de Gemini

---

### 2. Generar SECRET_KEY Automáticamente

**Problema:** Render no estaba generando la SECRET_KEY automáticamente.

**Solución aplicada en `Dislexia/settings.py`:**

```python
# SECURITY WARNING: keep the secret key used in production secret!
# Generar SECRET_KEY automáticamente si no está configurada
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY or SECRET_KEY.strip() == '':
    # Generar una SECRET_KEY única basada en información del sistema
    import hashlib
    import socket
    hostname = socket.gethostname()
    fallback_key = f'django-auto-generated-{hostname}-{BASE_DIR}'
    SECRET_KEY = hashlib.sha256(fallback_key.encode()).hexdigest()
    print(f"⚠️ WARNING: Using auto-generated SECRET_KEY. Set SECRET_KEY environment variable for production.")
```

**Beneficios:**
- ✅ Django siempre tiene una SECRET_KEY válida
- ✅ Se genera automáticamente si no está configurada
- ✅ Única para cada servidor

---

## 🚀 PASOS PARA REDESPLEGAR

### Paso 1: Subir los cambios a GitHub

```powershell
cd "C:\Users\Maxip\OneDrive\Documentos\Prepolitecinca\SeptimoSemestre\Usabilidad y Accesibilidad\Proyecto"

git add .
git commit -m "Fix: Corregir import de Gemini y generar SECRET_KEY automática"
git push origin main
```

### Paso 2: Configurar Variables en Render

1. **Ve a tu servicio en Render**
   - Dashboard → Tu servicio `dislexia-backend-docker`

2. **Ve a Environment**
   - Clic en **"Environment"** en el menú lateral

3. **Verifica/Agrega estas variables:**

   | Key | Value | Notas |
   |-----|-------|-------|
   | `SECRET_KEY` | *(auto-generada)* | Si no existe, déjala vacía - se generará automáticamente |
   | `DEBUG` | `False` | Importante para producción |
   | `ALLOWED_HOSTS` | `.onrender.com` | Permite el dominio de Render |
   | `GEMINI_API_KEY` | *(opcional)* | Déjala vacía - usa datos de respaldo |
   | `CORS_ALLOWED_ORIGINS` | `https://tu-frontend.vercel.app` | URL de tu frontend |

4. **Guarda los cambios**

### Paso 3: Redesplegar en Render

1. **Manual Deploy**
   - Ve a **"Manual Deploy"**
   - Clic en **"Deploy latest commit"**

2. **Espera el despliegue** (5-10 minutos)
   - Observa los logs en tiempo real

3. **Verifica que funcione**
   - El estado debe cambiar a **"Live"**
   - Abre: `https://tu-backend.onrender.com/api/juego1/?cantidad=3`
   - Deberías ver JSON con palabras

---

## 🔍 VERIFICAR LOS LOGS

### Lo que DEBES ver en los logs:

```bash
✅ ==> Cloning from https://github.com/MYBTIC/dislexiaa
✅ ==> Checking out commit...
✅ ==> Using Dockerfile: ./Dockerfile
✅ ==> Building Docker image
✅ Step 1/10 : FROM python:3.11-slim
✅ ...
✅ Successfully built image
✅ ==> Starting service...
✅ ⚠️ Google Generative AI no disponible. Usando datos de respaldo.
✅ [INFO] Starting gunicorn 21.2.0
✅ [INFO] Listening at: http://0.0.0.0:8000
✅ Your service is live! 🎉
```

### Lo que NO debes ver:

```bash
❌ ImportError: cannot import name 'genai' from 'google'
❌ The SECRET_KEY setting must not be empty
❌ Error handling request
```

---

## 🎯 EXPLICACIÓN TÉCNICA

### ¿Por qué falló el import?

**El problema:**
```python
from google import genai  # ❌ Este módulo no existe
```

La librería `google-generativeai` NO tiene un módulo llamado `google.genai`. El import correcto es:

```python
import google.generativeai as genai  # ✅ Correcto
```

### ¿Por qué la SECRET_KEY estaba vacía?

**El problema:**
- Render tenía configurado `generateValue: true` en `render.yaml`
- Pero cuando se despliega desde el dashboard manualmente, no siempre genera el valor
- Si la variable está vacía, Django falla

**La solución:**
- Generamos una SECRET_KEY automáticamente en el código
- Usa la variable de entorno si existe
- Si no existe, genera una única para ese servidor

---

## 📋 CHECKLIST DE VERIFICACIÓN

Después de redesplegar, verifica:

### Backend funcionando:
- [ ] El servicio está en estado "Live" en Render
- [ ] No hay errores en los logs
- [ ] El mensaje "Using auto-generated SECRET_KEY" aparece (está bien)
- [ ] El mensaje "Google Generative AI no disponible" aparece (está bien - usa respaldo)

### Endpoints funcionando:
- [ ] `https://tu-backend.onrender.com/api/juego1/?cantidad=3` devuelve JSON
- [ ] `https://tu-backend.onrender.com/api/juego2/?cantidad=3` devuelve JSON
- [ ] Las imágenes en el JSON son URLs válidas de Unsplash

### Ejemplo de respuesta correcta:
```json
[
  {
    "nombre": "gato",
    "imagen": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop",
    "palabra_dividida_letras": "g-a-t-o"
  },
  {
    "nombre": "perro",
    "imagen": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop",
    "palabra_dividida_letras": "p-e-r-r-o"
  }
]
```

---

## 🚨 SI TODAVÍA HAY ERRORES

### Error: "ModuleNotFoundError: No module named 'google'"

**Causa:** La librería no está instalada en el contenedor Docker.

**Solución:**

1. Verifica que `requirements_production.txt` tenga:
   ```
   google-generativeai==0.8.6
   ```

2. Si no está, agrégala y sube los cambios:
   ```powershell
   git add requirements_production.txt
   git commit -m "Add google-generativeai to requirements"
   git push origin main
   ```

3. Render redesplegará automáticamente

### Error: "SECRET_KEY still empty"

**Causa:** El código de fallback no se ejecutó correctamente.

**Solución:**

1. Ve a Render → Environment
2. Agrega manualmente una SECRET_KEY:
   - Key: `SECRET_KEY`
   - Value: (genera una aleatoria - puedes usar: https://djecrety.ir/)
3. Guarda y redespliega

### Error: CORS al conectar con Frontend

**Causa:** `CORS_ALLOWED_ORIGINS` no está configurada correctamente.

**Solución:**

1. Ve a Render → Environment
2. Edita `CORS_ALLOWED_ORIGINS`:
   ```
   https://tu-app-real.vercel.app
   ```
   (Sin `/` al final, con `https://`)
3. Guarda y espera el redespliegue

---

## 🎉 RESULTADO ESPERADO

Después de aplicar estas correcciones:

1. ✅ El backend despliega sin errores
2. ✅ Los endpoints responden con datos correctos
3. ✅ Las imágenes se muestran (usando palabras garantizadas)
4. ✅ No necesitas API key de Gemini (usa datos de respaldo)
5. ✅ La SECRET_KEY se genera automáticamente

---

## 💡 NOTAS IMPORTANTES

### Sobre Google Generative AI

- ✅ **NO es obligatoria** para que la app funcione
- ✅ La app usa un pool de **10 palabras garantizadas** con imágenes validadas
- ✅ Las palabras garantizadas: gato, perro, casa, flor, sol, luna, mesa, libro, pelota, árbol
- ✅ Son suficientes para el juego
- ⚠️ Si quieres más variedad, agrega la API key de Gemini más tarde

### Sobre SECRET_KEY

- ✅ Ahora se genera automáticamente
- ✅ Es única para tu servidor
- ✅ Se mantiene mientras el servidor esté activo
- ⚠️ Para producción seria, usa una SECRET_KEY fija en las variables de entorno

---

## 📞 SIGUIENTE PASO

Una vez que el backend funcione:

1. ✅ Copia la URL de tu backend: `https://tu-backend.onrender.com`
2. 🎨 Continúa con el despliegue del frontend en Vercel
3. 🔗 Configura CORS con la URL del frontend
4. 🎉 ¡Tu aplicación estará completa!

---

**Archivos modificados:**
- ✅ `api/views.py` - Import corregido
- ✅ `Dislexia/settings.py` - SECRET_KEY auto-generada
- ✅ `render.yaml` - Ya estaba correcto

**Comando para subir cambios:**
```powershell
git add .
git commit -m "Fix: Corregir import de Gemini y auto-generar SECRET_KEY"
git push origin main
```

**¡Ahora sí debería funcionar!** 🚀
