FROM python:3.10-slim

# Instala las dependencias necesarias para psycopg2, OpenCV y las bibliotecas de sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc libgl1 libglib2.0-0 --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala Gunicorn
RUN pip install gunicorn

COPY src/ /app/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

# Cambia el comando de ejecución para usar Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "src.__main__:app"]

