# 🚀 Guía de Despliegue en la Nube

Este documento explica cómo desplegar tu Dashboard Auditor en diferentes plataformas cloud.

---

## 🌟 Opción 1: Streamlit Community Cloud (RECOMENDADO)

### ✅ Ventajas:
- ✨ **100% GRATIS**
- 🚀 Despliegue en 2 minutos
- 🔄 Auto-actualización desde GitHub
- 💪 Sin límites de tráfico razonables
- 🎯 Optimizado para Streamlit

### 📋 Requisitos:
- Cuenta de GitHub (gratuita)
- Cuenta de Streamlit Cloud (gratuita)

### 🔧 Pasos:

#### 1️⃣ Subir tu proyecto a GitHub

```bash
# Ya inicializamos Git, ahora configuremos
cd "/Users/rafito29/Downloads/Dashboard Auditor"

# Configura tu identidad (si no lo has hecho)
git config user.name "Tu Nombre"
git config user.email "tu.email@ejemplo.com"

# Agregar archivos
git add app.py requirements.txt README.md .gitignore

# Hacer commit
git commit -m "Initial commit: Dashboard Auditor v3.0"

# Crear repositorio en GitHub
# Ve a https://github.com/new y crea un nuevo repositorio
# Llamalo: dashboard-auditor-salud

# Conectar con GitHub (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/dashboard-auditor-salud.git
git branch -M main
git push -u origin main
```

#### 2️⃣ Desplegar en Streamlit Cloud

1. **Ve a**: https://streamlit.io/cloud
2. **Click en** "Sign up" o "Sign in"
3. **Conecta tu GitHub**
4. **Click en** "New app"
5. **Selecciona**:
   - Repository: `dashboard-auditor-salud`
   - Branch: `main`
   - Main file path: `app.py`
6. **Click en** "Deploy!"

⏱️ **Tiempo de despliegue**: 2-3 minutos

🎉 **URL de tu app**: `https://tu-usuario-dashboard-auditor-salud.streamlit.app`

#### 3️⃣ Configuración Adicional (Opcional)

En Streamlit Cloud puedes:
- **Custom domain**: Conectar tu propio dominio
- **Secrets**: Añadir variables de entorno
- **Analytics**: Ver estadísticas de uso
- **Sleep settings**: Controlar cuándo la app se duerme

---

## 🐳 Opción 2: Render.com (También Gratuito)

### ✅ Ventajas:
- 🆓 Plan gratuito generoso
- 🔧 Más control que Streamlit Cloud
- 🌐 Custom domains incluido
- 📦 Soporta Docker

### 📋 Pasos:

#### 1️⃣ Subir a GitHub (igual que Opción 1)

#### 2️⃣ Desplegar en Render

1. **Ve a**: https://render.com
2. **Sign up** con GitHub
3. **New** → **Web Service**
4. **Conecta tu repositorio** `dashboard-auditor-salud`
5. **Configura**:
   - Name: `dashboard-auditor`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. **Click** "Create Web Service"

⏱️ **Tiempo de despliegue**: 5-7 minutos

🎉 **URL**: `https://dashboard-auditor.onrender.com`

⚠️ **Nota**: Plan gratuito se duerme después de 15 min de inactividad (tarda ~30s en despertar)

---

## ☁️ Opción 3: Google Cloud Run

### ✅ Ventajas:
- 🚀 Súper rápido
- 💰 Pay-as-you-go (muy barato)
- 🔒 Nivel empresarial
- 🌍 Global

### 📋 Requisitos:
- Cuenta de Google Cloud (incluye $300 créditos gratis)
- Docker instalado

### 🔧 Pasos:

#### 1️⃣ Crear Dockerfile

Ya creé el archivo `Dockerfile` en tu proyecto.

#### 2️⃣ Desplegar

```bash
# Instalar gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Configurar proyecto
gcloud config set project TU_PROJECT_ID

# Build y deploy
gcloud run deploy dashboard-auditor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

💰 **Costo estimado**: ~$2-5/mes con tráfico moderado

---

## 🔵 Opción 4: Heroku

### ⚠️ Nota: Heroku eliminó su plan gratuito. Costo mínimo $5/mes.

### 📋 Pasos:

#### 1️⃣ Crear archivos necesarios

Ya están creados:
- `Procfile`
- `setup.sh`

#### 2️⃣ Desplegar

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Crear app
heroku create dashboard-auditor-salud

# Deploy
git push heroku main

# Abrir
heroku open
```

💰 **Costo**: Desde $5/mes (Eco Dynos)

---

## 🆚 Comparación Rápida

| Plataforma | Precio | Velocidad | Facilidad | Uptime |
|------------|--------|-----------|-----------|--------|
| **Streamlit Cloud** | ✅ Gratis | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 99.9% |
| **Render** | ✅ Gratis | ⭐⭐⭐ | ⭐⭐⭐⭐ | 99.5% |
| **Google Cloud Run** | 💰 ~$3/mes | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 99.95% |
| **Heroku** | 💰 $5/mes | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 99.9% |

---

## 🎯 Recomendación

### Para tu caso (Dashboard Auditor):

**🏆 #1 Streamlit Community Cloud**
- Perfecto para este proyecto
- Gratis y sin límites importantes
- Mantenido por los creadores de Streamlit
- Despliegue super simple

### ¿Cuándo usar otras opciones?

- **Render**: Si necesitas más control o múltiples servicios
- **Google Cloud Run**: Para aplicaciones empresariales o con mucho tráfico
- **Heroku**: Si ya tienes infraestructura allí

---

## 📝 Checklist de Despliegue

- [ ] Subir código a GitHub
- [ ] Verificar que `requirements.txt` está actualizado
- [ ] Crear README.md descriptivo
- [ ] Configurar .gitignore correctamente
- [ ] Crear cuenta en plataforma elegida
- [ ] Conectar repositorio
- [ ] Configurar build settings
- [ ] Desplegar!
- [ ] Verificar que funciona correctamente
- [ ] Compartir URL 🎉

---

## 🆘 Problemas Comunes

### 1. Error de dependencias
```bash
# Regenera requirements.txt
pip freeze > requirements.txt
```

### 2. App no carga
- Verifica que `app.py` es el archivo principal
- Revisa logs de la plataforma
- Confirma que todas las dependencias están en requirements.txt

### 3. Timeout en deployment
- Algunas plataformas tienen límite de tiempo
- Optimiza instalación de dependencias
- Usa caché cuando sea posible

---

## 📚 Recursos Adicionales

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Render Deployment Guide](https://render.com/docs/deploy-streamlit)
- [Google Cloud Run Tutorial](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)

---

## 💡 Tips Pro

1. **Custom Domain**: Compra un dominio en Namecheap (~$10/año) y conéctalo
2. **Analytics**: Añade Google Analytics para trackear uso
3. **Monitoring**: Usa UptimeRobot para monitorear disponibilidad
4. **SSL**: Todas estas plataformas incluyen HTTPS automático ✅
5. **Auto-deploy**: Configura deploy automático en cada push a main

---

¿Necesitas ayuda con algún paso? ¡Pregúntame! 🚀
