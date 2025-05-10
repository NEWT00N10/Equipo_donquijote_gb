# Imagen base ligera con Python 3.11 y build tools
FROM python:3.11-slim as base

# Evitar prompts
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar dependencias de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libpq-dev curl netcat-openbsd gcc \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no root para seguridad
RUN useradd -ms /bin/bash django

WORKDIR /app

# Copiar archivos de requisitos primero para aprovechar la cache
COPY requirements.txt /app/

# Instalar pip deps en venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . /app

# Ajustar permisos para el usuario
#RUN chown -R django:django /app
#USER django

# Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
