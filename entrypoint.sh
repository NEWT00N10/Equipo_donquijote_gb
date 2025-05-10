#!/usr/bin/env bash
# entrypoint.sh — ejecutado por Docker
set -e

# Esperar a que Postgres acepte conexiones
echo "⏳ Esperando a Postgres..."
until nc -z db 5432; do
  >&2 echo "Postgres no disponible — reintentando..."
  sleep 1
done
echo "✅ Postgres disponible"

# Aplicar migraciones
echo "⚙️ Aplicando migraciones..."
python manage.py migrate --noinput

# Crear superusuario provisionado por variables (opcional)
if [[ "$DJANGO_SUPERUSER_USERNAME" ]]; then
  echo "🛠 Creando superusuario (si no existe)..."
  python manage.py shell <<PY
import os, django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]
email    = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
PY
fi

# Recolectar estáticos
echo "📦 Collectstatic..."
python manage.py collectstatic --noinput

# Lanzar Gunicorn
echo "🚀 Iniciando Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
