# 🎮 Juego de Palabras - Sistema de Dislexia

Aplicación web educativa para ayudar a niños con dislexia mediante juegos interactivos de palabras.

## 📁 Estructura del Proyecto

```
Proyecto/
├── 📂 Backend (Django REST API)
│   ├── Dislexia/          # Configuración del proyecto Django
│   ├── api/               # Endpoints de la API REST
│   │   ├── models.py      # Modelos de base de datos
│   │   ├── views.py       # Lógica de endpoints
│   │   ├── serializers.py # Serialización de datos
│   │   └── urls.py        # Rutas de la API
│   ├── manage.py          # Comando de gestión Django
│   ├── db.sqlite3         # Base de datos SQLite
│   └── requirements.txt   # Dependencias Python
│
├── 📂 Frontend (React + Vite)
│   ├── src/
│   │   ├── components/    # Componentes React del juego
│   │   ├── config/        # Configuración (URL backend)
│   │   ├── data/          # Datos de respaldo
│   │   └── App.jsx        # Componente principal
│   ├── package.json       # Dependencias Node.js
│   └── vite.config.js     # Configuración Vite
│
├── 📂 Docker
│   ├── Dockerfile         # Imagen Docker del backend
│   ├── docker-compose.yml # Orquestación de servicios
│   └── docker-helper.ps1  # Script de ayuda (Windows)
│
├── 📂 Deployment
│   ├── build.sh           # Script de build para Render.com
│   ├── render.yaml        # Configuración de Render.com
│   └── runtime.txt        # Versión de Python
│
└── 📄 Documentación
    ├── README.md          # Este archivo (inicio rápido)
    ├── backend.md         # Documentación detallada del backend
    └── frontend.md        # Documentación detallada del frontend
```

## 🚀 Inicio Rápido

### Requisitos Previos
- **Python 3.11+** (recomendado: 3.13)
- **Node.js 22.12+** (o 20.19+)
- Git (para clonar el repositorio)

### 🔧 Opción 1: Desarrollo Local

#### 1️⃣ Backend (Django)

```bash
# Activar entorno virtual (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

**URL**: http://127.0.0.1:8000/

#### 2️⃣ Frontend (React)

```bash
# Entrar a la carpeta frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor
npm run dev
```

**URL**: http://localhost:5173/

### 🐳 Opción 2: Con Docker

```bash
# Iniciar todos los servicios (backend + frontend + base de datos)
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

**Windows**: Usa el script de ayuda `.\docker-helper.ps1 help`

## 🎯 Modos de Juego

### 1. 🔤 Modo Anagrama
Los niños reorganizan letras desordenadas para formar palabras. Pueden escribir con el teclado o hacer clic en las letras.

### 2. 📝 Modo Sílabas
Los niños completan palabras eligiendo la sílaba correcta entre varias opciones.

### 3. 🎤 Repetición de Oración (con IA)
Después de completar una palabra, se genera una oración usando Google Gemini AI. Los niños deben repetir la oración usando reconocimiento de voz.

## 🔧 API Endpoints

**Backend**: http://127.0.0.1:8000/

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| GET | `/api/juego1/` | Palabras para anagramas | `cantidad` (2-8, default: 3) |
| GET | `/api/juego2/` | Palabras para sílabas | `cantidad` (2-8, default: 3) |
| POST | `/api/oracion/` | Generar oración con IA | `{"palabra": "gato"}` |

**Ejemplo**:
```bash
# Obtener 5 palabras para anagrama
curl http://127.0.0.1:8000/api/juego1/?cantidad=5

# Generar oración
curl -X POST http://127.0.0.1:8000/api/oracion/ \
  -H "Content-Type: application/json" \
  -d '{"palabra": "casa"}'
```

## 🛠️ Tecnologías Utilizadas

**Backend**: Django 5+ • Django REST Framework • Google Gemini AI • SQLite  
**Frontend**: React 18 • Vite 6 • Axios • Web Speech API

## 🐛 Solución de Problemas Comunes

### ❌ Error: "AxiosError" o "Error al obtener datos"

**Causa:** El backend no está corriendo.

**Solución:**
```powershell
# Opción 1: Usa el script de inicio
.\iniciar.ps1

# Opción 2: Manual
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

**Ver guía completa:** `ERROR_BACKEND_NO_CORRIENDO.md`

### ❌ Error: "Module not found" (Backend)

```powershell
pip install -r requirements.txt
```

### ❌ Error: "Module not found" (Frontend)

```powershell
cd frontend
npm install
```

### ❌ Backend funciona pero frontend no conecta

Verifica que:
1. Backend esté en: `http://127.0.0.1:8000`
2. Frontend esté en: `http://localhost:5173`
3. Ambos servidores estén corriendo simultáneamente

## 📚 Documentación Detallada

- **[backend.md](./backend.md)** - Configuración completa del backend, endpoints, deployment, Docker, y más
- **[frontend.md](./frontend.md)** - Configuración del frontend, componentes, deployment en Vercel, y más

## 👨‍💻 Comandos Útiles

```bash
# Backend
python manage.py createsuperuser    # Crear admin
python manage.py migrate            # Aplicar migraciones
python manage.py showmigrations     # Ver migraciones

# Frontend
npm run build                       # Build para producción
npm run preview                     # Preview del build

# Docker
docker-compose up -d --build        # Iniciar servicios
docker-compose logs -f              # Ver logs
docker-compose down                 # Detener servicios
```

---

**Autor**: Maximiliano Madrid  
**Proyecto**: POLI - Usabilidad y Accesibilidad  
**Fecha**: Febrero 2026

