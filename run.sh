#!/bin/bash
# Script helper para configurar variables de entorno y ejecutar la aplicación

# Activar entorno virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install "PureCloudPlatformClientV2>=240.0.0" "requests>=2.31.0" --quiet
fi

# Configurar variables de entorno (puedes modificar estos valores o exportarlos antes de ejecutar)
export GENESYS_CLIENT_ID="${GENESYS_CLIENT_ID:-5b964554-9ce3-4ed9-94d5-2f9cf483d878}"
export GENESYS_CLIENT_SECRET="${GENESYS_CLIENT_SECRET:-O79ocr64myamQfe0BxQFJCh3yxHRS1HgCpUFmemL1iE}"
export GENESYS_REGION="${GENESYS_REGION:-sae1.pure.cloud}"
export GENESYS_ENVIRONMENT="${GENESYS_ENVIRONMENT:-mypurecloud.com}"

# Ejecutar el script solicitado (por defecto test_connection.py)
SCRIPT="${1:-scripts/test_connection.py}"
echo "🚀 Running: $SCRIPT"
echo ""

python "$SCRIPT"
