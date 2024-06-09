import json
import requests
import subprocess
from datetime import datetime
import time
import os
import sys


def cargar_argumentos_desde_json(json_path):
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data
    else:
        # Ejecutar el script entrypoint.sh si el archivo no existe
        print("File not found, executing entrypoint.sh to create config.json")
        try:
            subprocess.check_call(['./entrypoint.sh'])
        except subprocess.CalledProcessError as e:
            print(f"Error executing entrypoint.sh: {e}")
        # Detener el script principal después de ejecutar entrypoint.sh
        sys.exit(0)

# Método para enviar un mensaje al grupo de Telegram
def enviar_mensaje_telegram(mensaje, bot_token, group_id):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': group_id,
        'text': mensaje,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Mensaje enviado correctamente a Telegram.")
    else:
        print("Error al enviar el mensaje a Telegram.")

# Método para ejecutar un script Python y devolver su salida como texto
def ejecutar_script(script_path, argumentos):
    try:
        # Ejecutar el script y capturar la salida
        resultado = subprocess.check_output(['python', script_path] + argumentos, stderr=subprocess.STDOUT, text=True)
        return resultado
    except subprocess.CalledProcessError as e:
        # Capturar errores de ejecución
        return f"Error al ejecutar el script: {e.output}"

# Bucle infinito para ejecutar el script cada hora
while True:
    # Cargar los argumentos desde el archivo JSON
    config = cargar_argumentos_desde_json('./Config/config.json')

    # Extraer los tokens para Telegram del archivo de configuración
    bot_token = config.pop('bot_token')
    group_id = config.pop('group_id')
    bucleCalls = config.pop('bucleCalls')
    url = config.pop('url')
    total_days = int(config.pop('total_days'))
    sleeper = int(config.pop('sleeper'))

    # Construir la ruta al script Python que deseas ejecutar
    script_path = './callAPI.py'

    # Iterar sobre los restaurantes en el archivo de configuración
    for key, value in config.items():
        # Filtrar los argumentos para incluir el restaurante actual
        argumentos_script = ['--url', url, '--restaurant', f'{value}', '--total_days', str(total_days), '--sleeper', str(sleeper)]

        # Ejecutar el script y obtener el resultado
        resultado_script = ejecutar_script(script_path, argumentos_script)
        print(resultado_script)
        # Verificar si el script devolvió un resultado
        if resultado_script.strip():
            print("[", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"] Inicio datos actualizados para {key}.")
            enviar_mensaje_telegram(resultado_script, bot_token, group_id)
            print("[", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"] Fin datos actualizados para {key}.")
        else:
            print("[", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"] No se encontraron nuevas horas disponibles para {key}.")

        # Esperar antes de procesar el siguiente restaurante
        time.sleep(sleeper)

    # Esperar una hora antes de ejecutar el script nuevamente
    time.sleep(int(bucleCalls))
