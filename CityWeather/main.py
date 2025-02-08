import requests
import csv
import pandas as pd
from datetime import datetime

# Coordenadas de Berlín
BERLIN_LAT = 52.520008
BERLIN_LONGITUDE = 13.404954
API_KEY = "02b0db70fac81ab6e71999aa102b3b93"
FILE_NAME = "clima-berlin-hoy.csv"


def get_weather(lat, lon, api):
    """Obtiene los datos del clima de la API de OpenWeather."""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Devuelve el JSON con los datos
    else:
        return {"cod": 404}  # Si hay un error, devuelve código 4

def write2csv(json_response, csv_filename):
    """Guarda los datos del clima en un archivo CSV sin sobrescribir los datos anteriores."""
    
    # Verificar si el archivo ya existe para escribir los encabezados solo una vez
    file_exists = False
    try:
        with open(csv_filename, "r", encoding="utf-8") as file:
            file_exists = True
    except FileNotFoundError:
        pass  # Si el archivo no existe, lo creará después
    
    # Abrir en modo 'a' (append) para agregar nuevas filas sin sobrescribir
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Si el archivo no existía, escribir encabezados
        if not file_exists:
            writer.writerow([
                "dt", "coord_lon", "coord_lat", 
                "weather_0_id", "weather_0_main", "weather_0_description", "weather_0_icon", 
                "base", "main_temp", "main_feels_like", "main_temp_min", "main_temp_max", 
                "main_pressure", "main_humidity", "main_sea_level", "main_grnd_level", 
                "visibility", "wind_speed", "wind_deg", "wind_gust", "clouds_all", 
                "sys_type", "sys_id", "sys_country", "sys_sunset", "timezone", 
                "id", "name", "cod"
            ])
        
        # Extraer los datos de la respuesta JSON con .get() para evitar errores si faltan valores
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Marca de tiempo (Unix)
            json_response.get("coord", {}).get("lon", ""),  # Longitud
            json_response.get("coord", {}).get("lat", ""),  # Latitud
            
            json_response.get("weather", [{}])[0].get("id", ""),  # ID de la condición meteorológica
            json_response.get("weather", [{}])[0].get("main", ""),  # Estado del clima principal (ej: Clouds)
            json_response.get("weather", [{}])[0].get("description", ""),  # Descripción del clima
            json_response.get("weather", [{}])[0].get("icon", ""),  # Icono del clima
            
            json_response.get("base", ""),  # Base de los datos meteorológicos
            
            json_response.get("main", {}).get("temp", ""),  # Temperatura actual
            json_response.get("main", {}).get("feels_like", ""),  # Sensación térmica
            json_response.get("main", {}).get("temp_min", ""),  # Temperatura mínima
            json_response.get("main", {}).get("temp_max", ""),  # Temperatura máxima
            json_response.get("main", {}).get("pressure", ""),  # Presión atmosférica
            json_response.get("main", {}).get("humidity", ""),  # Humedad en porcentaje
            json_response.get("main", {}).get("sea_level", ""),  # Presión a nivel del mar (si disponible)
            json_response.get("main", {}).get("grnd_level", ""),  # Presión a nivel del suelo (si disponible)
            
            json_response.get("visibility", ""),  # Visibilidad en metros
            
            json_response.get("wind", {}).get("speed", ""),  # Velocidad del viento
            json_response.get("wind", {}).get("deg", ""),  # Dirección del viento
            json_response.get("wind", {}).get("gust", ""),  # Ráfagas de viento (si disponible)
            
            json_response.get("clouds", {}).get("all", ""),  # Porcentaje de nubosidad
            
            json_response.get("sys", {}).get("type", ""),  # Tipo de sistema meteorológico
            json_response.get("sys", {}).get("id", ""),  # ID del sistema meteorológico
            json_response.get("sys", {}).get("country", ""),  # Código del país
            json_response.get("sys", {}).get("sunset", ""),  # Hora de la puesta del sol
            
            json_response.get("timezone", ""),  # Zona horaria en segundos
            json_response.get("id", ""),  # ID de la ciudad
            json_response.get("name", ""),  # Nombre de la ciudad
            json_response.get("cod", "")  # Código de estado de la API
        ])
    
    print(f"Datos agregados en {csv_filename}")

from datetime import datetime

def process(json):
    """Procesa los datos del clima para obtener solo la información importante."""
    
    # Extraer datos de manera segura con `.get()`
    temperatura = json.get("main", {}).get("temp", "N/A")
    humedad = json.get("main", {}).get("humidity", "N/A")
    presion = json.get("main", {}).get("pressure", "N/A")
    clima = json.get("weather", [{}])[0].get("description", "N/A")
    
    # Datos adicionales
    sensacion_termica = json.get("main", {}).get("feels_like", "N/A")
    temp_min = json.get("main", {}).get("temp_min", "N/A")
    temp_max = json.get("main", {}).get("temp_max", "N/A")

    # Viento
    viento_velocidad = json.get("wind", {}).get("speed", "N/A")
    viento_direccion = json.get("wind", {}).get("deg", "N/A")
    viento_rafagas = json.get("wind", {}).get("gust", "N/A")

    # Visibilidad
    visibilidad = json.get("visibility", "N/A")

    # Nubosidad
    nubosidad = json.get("clouds", {}).get("all", "N/A")

    # Coordenadas
    latitud = json.get("coord", {}).get("lat", "N/A")
    longitud = json.get("coord", {}).get("lon", "N/A")

    # Zona horaria y fecha
    timestamp = json.get("dt", None)  # Timestamp UNIX
    fecha = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

    # Hora de atardecer
    sunset_timestamp = json.get("sys", {}).get("sunset", None)
    hora_atardecer = datetime.utcfromtimestamp(sunset_timestamp).strftime('%H:%M:%S') if sunset_timestamp else "N/A"

    # País y ciudad
    pais = json.get("sys", {}).get("country", "N/A")
    ciudad = json.get("name", "N/A")

    # Diccionario normalizado con los datos extraídos
    normalized_dict = {
        "Fecha": fecha,
        "Ciudad": ciudad,
        "País": pais,
        "Latitud": latitud,
        "Longitud": longitud,
        "Temperatura (°C)": temperatura,
        "Sensación térmica (°C)": sensacion_termica,
        "Temp. Mín (°C)": temp_min,
        "Temp. Máx (°C)": temp_max,
        "Presión (hPa)": presion,
        "Humedad (%)": humedad,
        "Clima": clima,
        "Nubosidad (%)": nubosidad,
        "Visibilidad (m)": visibilidad,
        "Viento Velocidad (m/s)": viento_velocidad,
        "Viento Dirección (°)": viento_direccion,
        "Viento Ráfagas (m/s)": viento_rafagas,
        "Hora Atardecer": hora_atardecer
    }

    return normalized_dict


def main():
    """Función principal que obtiene, procesa y guarda los datos del clima."""
    print("===== Bienvenido a Clima-Berlín =====")
    berlin_weather = get_weather(lat=BERLIN_LAT, lon=BERLIN_LONGITUDE, api=API_KEY)

    if berlin_weather['cod'] != 404:
        data = process(berlin_weather)  # Procesar datos
        write2csv(berlin_weather, FILE_NAME)  # Guardar en CSV
        print("Datos obtenidos:", data)
    else:
        print("Ciudad no disponible o API KEY no válida")


if __name__ == '__main__':
    main()
