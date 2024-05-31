import json
import requests
import subprocess
from datetime import datetime
import time

# Método para cargar los argumentos desde un archivo JSON
def cargar_argumentos_desde_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

# Método para enviar un mensaje al grupo de Telegram
def enviar_mensaje_telegram(mensaje, bot_token, group_id):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': group_id,
        'text': mensaje
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
    config = cargar_argumentos_desde_json('config.json')

    # Extraer los tokens para Telegram del archivo de configuración
    bot_token = config.pop('bot_token')
    group_id = config.pop('group_id')
    bucleCalls = config.pop('bucleCalls')

    # Construir la ruta al script Python que deseas ejecutar
    script_path = './callAPI.py'

    # Filtrar los argumentos para excluir 'bot_token' y 'group_id'
    argumentos_script = []
    for key, value in config.items():
        argumentos_script.append(f'--{key}')
        argumentos_script.append(str(value))

    # Ejecutar el script y obtener el resultado
    resultado_script = ejecutar_script(script_path, argumentos_script)

    # Verificar si el script devolvió un resultado
    if resultado_script.strip():
        print("[", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "] Inicio datos actualizados.")
        enviar_mensaje_telegram(resultado_script, bot_token, group_id)
        print("[", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "] Fin datos actualizados.")
    else:
        print("[", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "] No se encontraron nuevas horas disponibles.")

    # Esperar una hora antes de ejecutar el script nuevamente
    time.sleep(int(bucleCalls))
