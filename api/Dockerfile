# Usamos Python 3.11 slim para mantenerlo ligero
FROM python:3.11-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos requirements.txt y lo instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY app ./app

# Exponemos el puerto 80
EXPOSE 80

# Comando para correr la API con waitress en el puerto 80
CMD ["python", "-m", "app.main"]


 
