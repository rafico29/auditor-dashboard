# Dockerfile para Google Cloud Run o cualquier servicio que soporte Docker

FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app.py .

# Exponer puerto
EXPOSE 8080

# Variable de entorno para Streamlit
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
