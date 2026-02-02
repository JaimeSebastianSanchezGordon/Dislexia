# Frontend - React + Vite

## 🚀 Instalación y configuración

### 1. Instalar Node.js
Asegúrate de tener Node.js instalado:
- **Versión recomendada**: Node.js 22.12+ o 20.19+
- Descarga desde: https://nodejs.org/

### 2. Instalar dependencias y ejecutar

```bash
# 1. Entrar a la carpeta del frontend
cd frontend

# 2. Instalar todas las librerías de React (solo la primera vez)
npm install

# 3. Iniciar el servidor de desarrollo
npm run dev
```

El frontend estará disponible en: **http://localhost:5173/**

## 📋 Componentes principales

### Estructura del proyecto
```
frontend/
├── src/
│   ├── components/          # Componentes React
│   │   ├── Inicio.jsx      # Pantalla de inicio
│   │   ├── Configuracion.jsx
│   │   ├── ModoAnagrama.jsx
│   │   ├── ModoSilabaCorrecta.jsx
│   │   ├── InstruccionesAnagrama.jsx
│   │   ├── InstruccionesSilabaCorrecta.jsx
│   │   ├── Modal.jsx       # ⭐ Componente de ventana flotante
│   │   ├── EjemplosModal.jsx # Ejemplos de uso del Modal
│   │   └── ...
│   ├── config/
│   │   └── api.js          # Configuración de la URL del backend
│   ├── data/
│   │   └── datosSilabas.js # Datos de respaldo (fallback)
│   ├── App.jsx             # Componente principal
│   ├── gameLogic.js        # Lógica del juego
│   └── main.jsx            # Punto de entrada
├── public/                  # Archivos estáticos
├── index.html              # HTML principal
├── package.json            # Dependencias
├── vite.config.js          # Configuración de Vite
└── MODAL_GUIDE.md          # Guía completa del componente Modal
```

### 🪟 Componente Modal (Nuevo)

Se ha creado un **componente Modal reutilizable** para mostrar mensajes, errores, confirmaciones y más:

**Características:**
- ✅ 4 tipos de modal: Error, Éxito, Advertencia, Información
- ✅ Animaciones suaves (fade in + slide down)
- ✅ Backdrop con efecto blur
- ✅ Completamente responsive
- ✅ Cierre con clic fuera o botón
- ✅ Íconos automáticos según tipo
- ✅ Contenido personalizable

**Uso básico:**
```jsx
import Modal from './components/Modal';
import { useState } from 'react';

const MiComponente = () => {
    const [mostrarError, setMostrarError] = useState(false);

    return (
        <>
            <button onClick={() => setMostrarError(true)}>
                Mostrar Error
            </button>

            <Modal
                mostrar={mostrarError}
                onCerrar={() => setMostrarError(false)}
                titulo="Error"
                mensaje="Error al cargar el juego. Intenta de nuevo."
                tipo="error"
                textoBoton="OK"
            />
        </>
    );
};
```

**Ver guía completa:** `MODAL_GUIDE.md` con ejemplos detallados y casos de uso.

## 🎮 Modos de Juego

### 1. Modo Anagrama
- Los niños reorganizan letras desordenadas para formar palabras
- Pueden escribir con el teclado o hacer clic en las letras
- Se muestran imágenes de referencia para ayudar
- **Endpoint**: `GET /api/juego1/?cantidad=3`

### 2. Modo Sílabas
- Los niños completan palabras eligiendo la sílaba correcta
- Ejercicio de reconocimiento silábico
- **Endpoint**: `GET /api/juego2/?cantidad=3`

### 3. Repetición de Oración (con IA)
- Después de completar una palabra, se genera una oración
- Los niños deben repetir la oración usando reconocimiento de voz
- Usa Google Gemini AI para generar oraciones apropiadas
- **Endpoint**: `POST /api/oracion/`

## 🔧 Configuración del Backend

Edita `src/config/api.js` para configurar la URL del backend:

```javascript
// Desarrollo local
const API_URL = 'http://127.0.0.1:8000';

// Producción (ejemplo)
// const API_URL = 'https://tu-backend.onrender.com';

export default API_URL;
```

## 🛠️ Tecnologías utilizadas

- **React 18**: Librería de UI
- **Vite**: Build tool y dev server (ultra rápido)
- **Axios**: Cliente HTTP para llamadas al backend
- **Web Speech API**: Reconocimiento de voz del navegador
- **CSS Modules**: Estilos component-scoped

## 📦 Scripts disponibles

```bash
# Desarrollo
npm run dev          # Inicia servidor de desarrollo en http://localhost:5173

# Producción
npm run build        # Construye la aplicación para producción
npm run preview      # Previsualiza el build de producción

# Linting
npm run lint         # Ejecuta ESLint para verificar código
```

## 🎨 Características de accesibilidad

- ✅ **Fuente OpenDyslexic**: Fuente diseñada para personas con dislexia
- ✅ **Alto contraste**: Colores con buen contraste para mejor legibilidad
- ✅ **Tamaños de texto grandes**: Fácil de leer
- ✅ **Reconocimiento de voz**: Permite interacción sin teclado
- ✅ **Imágenes de apoyo**: Refuerzo visual para cada palabra
- ✅ **Feedback visual**: Indicadores claros de correcto/incorrecto

## 🌐 Despliegue en Vercel

El frontend está configurado para desplegarse en Vercel:

1. Conecta tu repositorio de GitHub a Vercel
2. Vercel detectará automáticamente Vite
3. Configuración en `vercel.json`:
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

**Nota**: No olvides configurar la URL del backend en producción editando `src/config/api.js`

## ⚠️ Solución de problemas

### Pantalla en blanco
- Verifica que el servidor esté corriendo: `npm run dev`
- Revisa la consola del navegador (F12) para ver errores
- Asegúrate de que todos los componentes existan

### Error: "Module not found"
- Ejecuta: `rm -rf node_modules package-lock.json && npm install`
- Verifica que todas las importaciones usen rutas correctas

### Error de conexión con el backend
- Verifica que el backend esté corriendo en `http://127.0.0.1:8000`
- Revisa la configuración en `src/config/api.js`
- Verifica CORS en el backend (debe permitir `http://localhost:5173`)

### Reconocimiento de voz no funciona
- Usa **Google Chrome** (mejor compatibilidad con Web Speech API)
- Asegúrate de dar permisos de micrófono al navegador
- Verifica que el sitio esté en HTTPS (en producción)

## 🔄 Datos de respaldo

El archivo `src/data/datosSilabas.js` contiene datos de prueba para el modo sílabas. Se usa como fallback si el backend no está disponible.

**Nota**: En producción, siempre se usa el backend para obtener datos frescos.

---

**Stack**: React 18 + Vite 6 + Axios  
**Fecha**: Febrero 2026
