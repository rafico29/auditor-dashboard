# 🏥 Radar de Alertas - Contratación en Salud (SECOP)

Dashboard interactivo de auditoría para la detección temprana de riesgos en contratos de salud pública.

## 📋 Descripción

Sistema de alertas tempranas diseñado para identificar y priorizar contratos de salud pública que presenten indicadores de riesgo, facilitando labores de auditoría y control.

## ✨ Características

### 📊 Dashboard General
- Vista panorámica con KPIs principales
- Mapa interactivo de riesgo por departamento
- Serie temporal de alertas con contexto
- Distribución por modalidad de contratación
- Top 20 contratos priorizados por riesgo

### 🔍 Análisis Detallado
- Exploración individual de contratos
- Score de riesgo con indicador gauge
- Señales de alerta automáticas
- Factores de riesgo desglosados
- Comparación con contratos similares

### 🏢 Análisis de Proveedores
- Top proveedores por score de riesgo
- Detección de patrones de concentración
- Distribución de contratos por entidad
- Análisis de simultaneidad

### 📈 Calidad de Datos
- Índice de calidad en 4 dimensiones:
  - Completitud (30%)
  - Consistencia (25%)
  - Oportunidad (25%)
  - Estandarización (20%)
- Ranking de entidades por calidad
- Estadísticas generales del sistema

### ℹ️ Ayuda
- Guía completa de uso
- Interpretación de scores
- Recomendaciones de análisis

## 🚀 Instalación Local

### Prerrequisitos
- Python 3.8 o superior
- pip

### Pasos

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd "Dashboard Auditor"
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

5. **Abrir en el navegador**
La aplicación estará disponible en `http://localhost:8501`

## 📦 Dependencias

- streamlit >= 1.30.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- plotly >= 5.18.0

## 🎯 Uso

### Filtros Disponibles
- **📅 Período**: Rango de años a analizar
- **📍 Departamento**: Filtrar por región específica
- **📋 Modalidad**: Tipo de contratación
- **⚠️ Nivel de Riesgo**: Alto, Medio, Bajo

### Navegación
Usa el menú lateral para cambiar entre las 5 secciones principales del dashboard.

### Interpretación del Score
- 🔴 **70-100% (Alto)**: Revisión prioritaria
- 🟠 **40-70% (Medio)**: Revisión recomendada
- 🟢 **0-40% (Bajo)**: Parámetros normales

## 🔒 Nota Importante

Este es un **prototipo con datos simulados** para fines de demostración y testeo. Los scores y alertas no representan situaciones reales de contratación.

## 👥 Autores

Universidad Javeriana 2025

## 📄 Licencia

Este proyecto es un prototipo académico.

## 🆕 Versión

**MVP v3.0** - Dashboard con navegación mejorada y secciones organizadas

---

Desarrollado con ❤️ para mejorar la transparencia en contratación pública
