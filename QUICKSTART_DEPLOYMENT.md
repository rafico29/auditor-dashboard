# 🚀 Despliegue Rápido (5 minutos)

## Opción Más Fácil: Streamlit Community Cloud

### Paso 1: Subir a GitHub (2 minutos)

```bash
# 1. Ve a tu terminal
cd "/Users/rafito29/Downloads/Dashboard Auditor"

# 2. Configura Git (solo la primera vez)
git config user.name "Tu Nombre"
git config user.email "tuemail@gmail.com"

# 3. Crea un nuevo repositorio en GitHub
# Ve a: https://github.com/new
# Nombre sugerido: dashboard-auditor-salud
# Dejalo PÚBLICO
# NO marques "Initialize with README"

# 4. Agrega los archivos
git add .
git commit -m "Dashboard Auditor v3.0 - Ready for deployment"

# 5. Conecta con GitHub (cambia TU_USUARIO por tu usuario real)
git remote add origin https://github.com/TU_USUARIO/dashboard-auditor-salud.git
git branch -M main
git push -u origin main
```

### Paso 2: Desplegar en Streamlit Cloud (3 minutos)

1. **Abre**: https://share.streamlit.io/

2. **Haz clic en** "Sign in" → "Continue with GitHub"

3. **Autoriza** Streamlit para acceder a tus repos

4. **Haz clic en** "New app"

5. **Completa el formulario**:
   ```
   Repository: TU_USUARIO/dashboard-auditor-salud
   Branch: main
   Main file path: app.py
   App URL (opcional): dashboard-salud (o el nombre que quieras)
   ```

6. **Haz clic en** "Deploy!"

7. **Espera 2-3 minutos** mientras se despliega...

8. **¡LISTO!** 🎉 Tu app estará en:
   ```
   https://TU_USUARIO-dashboard-auditor-salud.streamlit.app
   ```

---

## 🎯 URLs de Ejemplo

Después del despliegue, tu app podría estar en URLs como:

- `https://rafito29-dashboard-auditor-salud.streamlit.app`
- `https://dashboard-salud.streamlit.app` (si personalizaste el nombre)

---

## ✅ Verificación Post-Despliegue

Una vez desplegado, verifica que:

- [ ] La página carga correctamente
- [ ] El menú de navegación funciona
- [ ] Los filtros aplican cambios
- [ ] Los gráficos se visualizan
- [ ] Las tablas muestran datos

---

## 🔄 Actualizar la App

Cuando hagas cambios en tu código:

```bash
# 1. Guarda tus cambios
git add .
git commit -m "Descripción de los cambios"
git push

# 2. Streamlit Cloud detecta el push automáticamente
# 3. La app se redespliega sola en 1-2 minutos ✨
```

---

## 🆘 ¿Problemas?

### Error: "Repository not found"
- Verifica que el repo sea público
- Revisa que escribiste bien el nombre del usuario y repo

### Error: "Module not found"
- Verifica que todas las dependencias estén en `requirements.txt`
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### La app se ve rara o no carga
- Revisa los logs en el dashboard de Streamlit Cloud
- Haz clic en "Manage app" → "Logs"

### ¿Necesitas hacer el repo privado?
- Streamlit Cloud soporta repos privados
- Solo necesitas dar acceso a la app de Streamlit

---

## 💡 Tips Pro

### 1. Custom URL
En Streamlit Cloud puedes personalizar tu URL:
- Dashboard → Settings → Custom subdomain
- Ejemplo: `dashboard-salud-colombia.streamlit.app`

### 2. Configurar secretos (si usas APIs)
- Dashboard → Settings → Secrets
- Añade variables de entorno en formato TOML

### 3. Configurar auto-sleep
- Por defecto, la app se duerme después de 7 días sin uso
- Se despierta automáticamente cuando alguien la visita

### 4. Analytics
- Dashboard → Analytics
- Ve estadísticas de uso, visitantes, etc.

---

## 🌐 Compartir tu Dashboard

Una vez desplegado, puedes compartir la URL:

### Para presentaciones:
```
🏥 Dashboard Auditor de Salud
🔗 https://tu-app.streamlit.app
📊 Sistema de alertas tempranas para contratación pública
```

### QR Code:
Genera un QR en: https://www.qr-code-generator.com/
Coloca tu URL de Streamlit Cloud

---

## 📊 Estadísticas de Despliegue

- **Tiempo total**: ~5 minutos
- **Costo**: $0 (completamente gratis)
- **Límites**: 1GB RAM, uso razonable
- **SSL**: Incluido (HTTPS automático)
- **Uptime**: 99.9%

---

## 🎉 ¡Eso es todo!

Tu dashboard ya está en la nube y accesible desde cualquier lugar del mundo.

**¿Siguientes pasos?**
1. Comparte la URL con tu equipo
2. Configura un custom domain si quieres (opcional)
3. Añade más funcionalidades
4. ¡Disfruta! 🚀
