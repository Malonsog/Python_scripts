# Importar las bibliotecas necesarias
import requests
from dateutil.parser import parse
import pandas as pd


# **Definición de variables**

# URL de la API
url = 'https://mindicador.cl/api/'

# Datos recibidos desde la API en formato JSON
data = requests.get(url).json()

# Diccionario sólo con la data de los indicadores
# (sin datos de versión, autor ni fecha de consulta)
indicadores = {}


# **Recorrer los datos de la API**
for dato in data:
    # Si el dato es tipo dict, se agrega al diccionario "indicadores"
    if type(data[dato]) == dict:
        indicadores.update({dato: data[dato]})

# Definición de símbolos para las unidades de medición
unidades = {"Pesos": "$", "Dólar": "US$", "Porcentaje": "%"}


# Función para convertir en fecha el string que entrega la API
def format_date(fecha_str):
    try:
        # Verifica si el string tiene formato de fecha
        fecha = parse(fecha_str)
        return fecha.strftime("%d-%m-%Y")
    except Exception as e:
        # Si el formato es incorrecto, devuelve el string
        return fecha_str


# **Crear una lista de diccionarios con los datos de los indicadores**

# Esta sección crea una lista de diccionarios con los datos de los indicadores recibidos desde la API.
data_indicadores = [
    {
        "Indicador": value_dict["nombre"],
        "Valor": value_dict["valor"],
        "Unidad": unidades.get(value_dict["unidad_medida"], ""),
        "Fecha": format_date(value_dict["fecha"]),
    }
    # Se agrega un diccionario a la lista para cada indicador.
    for value_dict in indicadores.values()
]


# Definición de las columnas para el DataFrame
columns = ["Indicador", "Valor", "Unidad", "Fecha"]

# Creación del DataFrame con la data y con las columnas
df = pd.DataFrame(data_indicadores, columns=columns)


# Mostrar en la consola la info obtenida
print(f'Fecha de consulta: {format_date(data["fecha"])}')
print(df.to_string(index=False))

# Se puede usar el df para plotear los datos o hacer análisis..