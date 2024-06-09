#!/bin/sh

if [ ! -f ./Config/config.json ]; then
    echo "config.json no encontrado, iniciando formulario web..."
    python3 ./WEB/form_web.py
fi    

echo "config.json encontrado, iniciando main.py..."
python3 main.py
