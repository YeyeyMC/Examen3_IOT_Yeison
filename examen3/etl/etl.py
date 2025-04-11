import requests
import pymongo

# Rangos oficiales del EPA para PM2.5
pm25_breakpoints = [
    (0.0, 12.0, 0, 50, "Bueno"),
    (12.1, 35.4, 51, 100, "Moderado"),
    (35.5, 55.4, 101, 150, "Insalubre para grupos sensibles"),
    (55.5, 150.4, 151, 200, "Insalubre"),
    (150.5, 250.4, 201, 300, "Muy insalubre"),
    (250.5, 500.4, 301, 500, "Peligroso")
]

# Calcular AQI para un valor PM2.5
def calcular_aqi_pm25(valor_pm25):
    for c_low, c_high, i_low, i_high, categoria in pm25_breakpoints:
        if c_low <= valor_pm25 <= c_high:
            aqi = round(((i_high - i_low) / (c_high - c_low)) * (valor_pm25 - c_low) + i_low)
            return aqi, categoria
    return None, "Fuera de rango"

# URL de la API del SIATA
url = "https://siata.gov.co/EntregaData1/Datos_SIATA_Aire_AQ_pm25_Last.json"

# Conexión a MongoDB
mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")
db = mongo_client["siata"]
collection = db["calidad_aire"]

# Obtener y limpiar datos
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    mediciones_limpias = []
    for m in data.get("measurements", []):
        valor = m.get("value")
        if valor is not None and valor >= 0:
            aqi_valor, aqi_cat = calcular_aqi_pm25(valor)
            m["aqi_value"] = aqi_valor
            m["aqi_category"] = aqi_cat
            mediciones_limpias.append(m)

    if mediciones_limpias:
        result = collection.insert_many(mediciones_limpias)
        print(f"{len(result.inserted_ids)} documentos insertados.")
    else:
        print("No se encontraron datos válidos para insertar.")

except requests.RequestException as e:
    print("Error al consultar la API:", e)
except Exception as e:
    print("Error general:", e)
