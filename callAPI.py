import argparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os
import time  # Importa el módulo time


# Función para parsear los argumentos de línea de comandos
def parse_arguments():
    parser = argparse.ArgumentParser(description='Script para obtener las horas disponibles de reservación.')
    parser.add_argument('--url', type=str, help='URL de la solicitud POST')
    parser.add_argument('--restaurant', type=str, help='ID del restaurante')
    parser.add_argument('--total_days', type=int, default=5, help='Número de días a futuro a buscar')
    parser.add_argument('--sleeper', type=int, default=2, help='Valor del sleeper en segundos')
    return parser.parse_args()

# Parsear los argumentos de línea de comandos
args = parse_arguments()
url = args.url
restaurantid = args.restaurant
total_days = args.total_days
sleeper = args.sleeper

# Fecha de inicio (hoy) y fin (tres días adelante)
start_date = datetime.now()
end_date = start_date + timedelta(days=total_days)

# Crear el directorio Logs si no existe
logs_dir = 'Logs'
os.makedirs(logs_dir, exist_ok=True)

# Nombre del archivo JSON
json_filename = os.path.join(logs_dir, f'reservas_{restaurantid}.json')

# Cargar el archivo JSON existente, si existe
if os.path.exists(json_filename):
    with open(json_filename, 'r') as f:
        reservas_disponibles = json.load(f)
else:
    reservas_disponibles = {}

# Bandera para indicar si hubo cambios
hubo_cambios = False
restaurante_mensaje_mostrado = False

# Iterar sobre cada día en el rango de fechas
current_date = start_date
while current_date <= end_date:
    # Formatear la fecha en el formato DD-MM-YYYY
    fecha_dia = current_date.strftime('%d-%m-%Y')
    
    # Datos del formulario para el body
    data = {
        'restaurant': restaurantid,
        'dia': fecha_dia
    }   

    # Realizar la solicitud POST
    response = requests.post(url, data=data)
    
    # Verificar la respuesta
    if response.status_code == 200:
        # Analizar el contenido JSON de la respuesta
        response_json = response.json()
        
        # Obtener el contenido de hour_box
        hour_box_html = response_json.get('hour_box', '')

        # Usar BeautifulSoup para analizar el HTML de hour_box
        soup = BeautifulSoup(hour_box_html, 'html.parser')

        # Verificar si hay un select en el hour_box
        select_element = soup.find('select')
        if select_element:
            # Extraer las opciones de la lista desplegable
            options = select_element.find_all('option')

            # Obtener solo las horas disponibles
            horas_disponibles = []
            for option in options:
                value = option.get('value')
                text = option.text
                if value not in ['-1', ''] and 'Select' not in text and 'seleccionar' not in text.lower():
                    horas_disponibles.append(text)
            
            if horas_disponibles:
                # Actualizar el JSON solo si hay nuevas horas disponibles
                if fecha_dia not in reservas_disponibles or set(reservas_disponibles[fecha_dia]) != set(horas_disponibles):
                    reservas_disponibles[fecha_dia] = horas_disponibles
                    hubo_cambios = True
                    if not restaurante_mensaje_mostrado:
                        print(f"*{restaurantid}*")
                        restaurante_mensaje_mostrado = True 
                    print(f"{fecha_dia}:")
                    print(f"{', '.join(horas_disponibles)}")
            else:
                # No hay horas disponibles, eliminar del JSON si existe
                if fecha_dia in reservas_disponibles:
                    del reservas_disponibles[fecha_dia]
                    hubo_cambios = True
                #print(f"No hay horas disponibles para {fecha_dia}")
        else:
            # No hay select element, eliminar del JSON si existe
            if fecha_dia in reservas_disponibles:
                del reservas_disponibles[fecha_dia]
                hubo_cambios = True
            #print(f"No hay horas disponibles para {fecha_dia}")
    
    else:
        print(f"Restaurante: {restaurantid}")
        print(f"Error en la solicitud: {response.status_code}")
        print(response.text)
    
    # Descansar durante 3 segundos antes de la siguiente solicitud
    time.sleep(sleeper)
    
    # Avanzar al siguiente día
    current_date += timedelta(days=1)

# Ordenar el diccionario por fechas
reservas_disponibles_ordenado = dict(sorted(reservas_disponibles.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y')))

# Guardar los datos actualizados en el archivo JSON solo si hubo cambios
if hubo_cambios:
    with open(json_filename, 'w') as f:
        json.dump(reservas_disponibles_ordenado, f, indent=4)
#else:
#    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#    print(f"No se encontraron nuevas horas disponibles. [{current_time}]")
