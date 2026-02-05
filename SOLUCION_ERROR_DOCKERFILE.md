# 🔧 Solución: Error "Root directory Dockerfile does not exist"

## ❌ Error Completo
```
==> Root directory "Dockerfile" does not exist. Verify the Root Directory configured in your service settings.
error: invalid local: stat /opt/render/project/src/Dockerfile: not a directory
```

## 🎯 CAUSA DEL PROBLEMA
Render está intentando usar `Dockerfile` (que es un archivo) como directorio raíz del proyecto. Esto ocurre cuando se configura incorrectamente el campo **Root Directory** en Render.

---

## ✅ SOLUCIÓN RÁPIDA

### Método 1: Configurar en Render Dashboard (RECOMENDADO)

1. **Ve a tu servicio en Render.com**
   - Dashboard → Selecciona tu servicio `dislexia-backend-docker`

2. **Ve a Settings**
   - Haz clic en la pestaña **"Settings"** en el menú lateral

3. **Busca la sección "Build & Deploy"**

4. **Configura estos campos EXACTOS:**

   | Campo | Valor Correcto | ⚠️ NO uses |
   |-------|----------------|------------|
   | **Root Directory** | `.` (o déjalo VACÍO) | ❌ `Dockerfile` |
   | **Dockerfile Path** | `./Dockerfile` o `Dockerfile` | ✅ |
   | **Docker Context** | `.` | ✅ |
   | **Docker Command** | (dejar vacío - usa el del Dockerfile) | ✅ |

5. **Guarda los cambios**
   - Haz clic en **"Save Changes"**

6. **Redesplegar**
   - Ve a **"Manual Deploy"**
   - Haz clic en **"Deploy latest commit"**
   - Espera a que termine (5-10 minutos)

---

### Método 2: Usar Configuración Manual (Sin render.yaml)

Si estás creando el servicio por primera vez:

#### Paso 1: Elimina o ignora render.yaml
El archivo `render.yaml` puede causar conflictos si está mal configurado.

#### Paso 2: Crea el servicio manualmente

1. **En Render Dashboard**
   - **New +** → **Web Service**

2. **Conecta tu repositorio**
   - Busca: `MYBTIC/dislexiaa`
   - Clic en **"Connect"**

3. **Configura el servicio:**

   ```
   Name: dislexia-backend
   Environment: Docker
   Region: Oregon (US West)
   Branch: main
   Root Directory: (DEJAR VACÍO o poner .)
   Dockerfile Path: ./Dockerfile
   Docker Context: .
   ```

4. **Variables de Entorno:**
   ```
   SECRET_KEY = (dejar vacío - auto-generar)
   DEBUG = False
   ALLOWED_HOSTS = .onrender.com
   CORS_ALLOWED_ORIGINS = (tu URL de frontend)
   ```

5. **Crear el servicio**

---

## 🔍 VERIFICACIÓN

Después de configurar correctamente, los logs de Render deben mostrar:

```
==> Cloning from https://github.com/MYBTIC/dislexiaa
==> Checking out commit...
==> Using Dockerfile: ./Dockerfile
==> Building Docker image
Step 1/10 : FROM python:3.11-slim
...
```

✅ **NO debe aparecer:** "Root directory Dockerfile does not exist"

---

## 📋 CONFIGURACIÓN CORRECTA RESUMIDA

```yaml
# Estructura del proyecto (en GitHub)
Proyecto/
├── Dockerfile          ← Archivo Docker
├── manage.py
├── requirements_production.txt
├── Dislexia/
├── api/
└── frontend/

# Configuración en Render
Root Directory: .      ← El directorio raíz del proyecto
Dockerfile Path: ./Dockerfile   ← Ruta al archivo Dockerfile
Docker Context: .      ← Contexto de construcción Docker
```

**Explicación:**
- **Root Directory (`.`)** = Usa la raíz del repositorio
- **Dockerfile Path (`./Dockerfile`)** = El Dockerfile está en la raíz
- **Docker Context (`.`)** = Construye desde la raíz

---

## 🚨 ERRORES COMUNES

### ❌ ERROR 1: Poner "Dockerfile" en Root Directory
```
Root Directory: Dockerfile  ← MAL
```
**Correcto:**
```
Root Directory: .           ← BIEN
```

### ❌ ERROR 2: Ruta incorrecta del Dockerfile
```
Dockerfile Path: Dockerfile/  ← MAL (tiene slash)
```
**Correcto:**
```
Dockerfile Path: ./Dockerfile  ← BIEN
```

### ❌ ERROR 3: Docker Context vacío
```
Docker Context:              ← MAL (vacío)
```
**Correcto:**
```
Docker Context: .            ← BIEN
```

---

## 📝 SI USAS render.yaml (Opcional)

Si prefieres usar `render.yaml` para la configuración, asegúrate de que tenga esto:

```yaml
services:
  - type: web
    name: dislexia-backend-docker
    env: docker
    repo: https://github.com/MYBTIC/dislexiaa.git
    rootDir: .                    # ← Importante: punto, no "Dockerfile"
    dockerfilePath: ./Dockerfile  # ← Ruta al archivo
    dockerContext: .              # ← Contexto de construcción
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "False"
      - key: ALLOWED_HOSTS
        value: ".onrender.com"
      - key: CORS_ALLOWED_ORIGINS
        value: "https://tu-frontend.vercel.app"
    healthCheckPath: /api/juego1/
    autoDeploy: true
```

**Luego:**
1. Guarda el archivo
2. Sube a GitHub:
   ```powershell
   git add render.yaml
   git commit -m "Fix: Corregir configuración de Root Directory"
   git push origin main
   ```
3. En Render, ve a **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🎯 PASOS FINALES

1. ✅ Configura Root Directory correctamente en Render
2. ✅ Verifica que Dockerfile Path sea `./Dockerfile`
3. ✅ Verifica que Docker Context sea `.`
4. ✅ Guarda los cambios
5. ✅ Redesplegar manualmente
6. ✅ Espera 5-10 minutos
7. ✅ Verifica que el estado sea "Live"

---

## 🔗 RECURSOS

- **Render Docker Docs:** https://render.com/docs/docker
- **Tu repositorio:** https://github.com/MYBTIC/dislexiaa
- **Dashboard de Render:** https://dashboard.render.com

---

## 💡 TIP IMPORTANTE

**La configuración en el Dashboard de Render tiene prioridad sobre render.yaml**

Si tienes ambos, lo que configures en el dashboard es lo que se usará. Por eso es más fácil configurar directamente en el dashboard.

---

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de redesplegar, verifica:

- [ ] Root Directory está en `.` (o vacío)
- [ ] Root Directory NO dice "Dockerfile"
- [ ] Dockerfile Path está en `./Dockerfile`
- [ ] Docker Context está en `.`
- [ ] Variables de entorno configuradas
- [ ] Branch es `main`
- [ ] Repositorio es `https://github.com/MYBTIC/dislexiaa.git`

---

**Si sigues estos pasos exactamente, el error desaparecerá y Render construirá tu aplicación correctamente.** ✅

¿Necesitas más ayuda? Revisa `GUIA_DESPLIEGUE.md` para más detalles.
