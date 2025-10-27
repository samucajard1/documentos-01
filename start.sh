#!/bin/bash
export PORT=${PORT:-8080}
echo "🚀 Iniciando Airbus Careers na porta $PORT"
exec gunicorn main:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --preload

