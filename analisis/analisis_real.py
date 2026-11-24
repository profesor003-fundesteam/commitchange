# WattLens - Analisis del consumo electrico real
# Vivienda francesa - Mayo de 2007

import pandas as pd
import matplotlib.pyplot as plt
import json

# Leer el dataset real
datos = pd.read_csv(
    "wattwise_mayo_2007.csv",
    parse_dates=["timestamp"]
)


# Validacion inicial de las mediciones

columnas_requeridas = [
    "timestamp",
    "energy_kwh",
    "kitchen_kwh",
    "laundry_kwh",
    "water_ac_kwh",
    "other_kwh"
]

faltan = [
    columna for columna in columnas_requeridas
    if columna not in datos.columns
]

if faltan:
    raise ValueError(f"Columnas faltantes: {faltan}")

# Comprobar fechas y valores vacios
if datos.empty or datos[columnas_requeridas].isna().any().any():
    raise ValueError("El CSV esta vacio o contiene valores faltantes.")

# Comprobar que los consumos sean numericos y no negativos
columnas_energia = columnas_requeridas[1:]

for columna in columnas_energia:
    datos[columna] = pd.to_numeric(datos[columna], errors="coerce")

if datos[columnas_energia].isna().any().any():
    raise ValueError("Existen consumos no numericos.")

if datos[columnas_energia].lt(0).any().any():
    raise ValueError("Existen consumos negativos.")

# Ordenar y verificar continuidad temporal
datos = datos.sort_values("timestamp").reset_index(drop=True)

if datos["timestamp"].duplicated().any():
    raise ValueError("Existen fechas duplicadas.")

intervalos = datos["timestamp"].diff().dropna()

if not intervalos.eq(pd.Timedelta(minutes=1)).all():
    raise ValueError("Existen intervalos temporales irregulares.")

# Comprobar que cada hora tenga 60 mediciones
registros_por_hora = datos.groupby(
    datos["timestamp"].dt.floor("h")
).size()

if not registros_por_hora.eq(60).all():
    raise ValueError("Existen horas con mediciones incompletas.")

print("\nVALIDACION INICIAL SUPERADA")


# Calcular la energia total del mes
consumo_mensual = datos["energy_kwh"].sum()

# Mostrar los resultados
print("\nWATTLENS - ANALISIS REAL")

print("Cantidad de mediciones:", len(datos))

print(f"Consumo total de mayo: {consumo_mensual:.2f} kWh")

# Extraer la fecha y la hora de cada medicion

datos["fecha"] = datos["timestamp"].dt.date
datos["hora"] = datos["timestamp"].dt.hour

# Calcular la energia consumida por cada dia y hora

consumo_diario_horario = datos.groupby(
    ["fecha", "hora"]
)["energy_kwh"].sum()

# Calcular el promedio de cada hora entre los 31 dias

promedio_horario = consumo_diario_horario.groupby(
    "hora"
).mean()

# Mostrar los resultados

print("\nCONSUMO PROMEDIO POR HORA DEL DIA:")
print(promedio_horario.round(4))

# Identificar el horario de mayor consumo promedio

hora_pico = promedio_horario.idxmax()

energia_pico = promedio_horario.max()

print("\nHORARIO DE MAYOR CONSUMO:")

print(f"Hora pico: {hora_pico}:00")

print(f"Energia promedio: {energia_pico:.4f} kWh")

# Grafica de consumo horario - WattLens

plt.figure(figsize=(11, 6))

# Representar el consumo promedio de las 24 horas
plt.plot(
    promedio_horario.index,
    promedio_horario.values,
    marker="o",
    linewidth=2,
    label="Average hourly energy use"
)

# Destacar el horario de mayor consumo
plt.scatter(
    hora_pico,
    energia_pico,
    color="red",
    s=90,
    zorder=3
)


# Identificar el punto maximo
plt.annotate(
    f"Peak hour: {hora_pico}:00 - {energia_pico:.4f} kWh",
    xy=(hora_pico, energia_pico),
    xytext=(-165, -45),
    textcoords="offset points",
    fontsize=10,
    bbox=dict(
        boxstyle="round,pad=0.3",
        fc="white",
        ec="gray",
        alpha=0.9
    ),
    arrowprops=dict(arrowstyle="->")
)


# Titulo y ejes
plt.title("WattLens - Hourly Electricity Use, May 2007")
plt.xlabel("Time of day")
plt.ylabel("Average hourly energy use (kWh)")

# Mostrar las 24 horas
plt.xticks(range(0, 24))
plt.xlim(0, 23)
plt.ylim(bottom=0)

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# Guardar la grafica automaticamente
plt.savefig("grafica_consumo_horario_real.png", dpi=300)
plt.close()

print("\nGRAFICA REAL GENERADA CORRECTAMENTE")
# Analizar los circuitos durante la hora pico

datos_hora_pico = datos[datos["hora"] == hora_pico].copy()

promedio_circuitos_pico = datos_hora_pico[
    ["kitchen_kwh", "laundry_kwh", "water_ac_kwh", "other_kwh"]
].sum() / datos["fecha"].nunique()

print("\nPROMEDIO DE CONSUMO POR CIRCUITO EN LA HORA PICO:")
print(promedio_circuitos_pico.round(4))

# Segunda grafica real de WattLens
# Consumo promedio de los circuitos en la hora pico

nombres_circuitos = [
    "Kitchen",
    "Laundry",
    "Water heating & AC",
    "Other uses"
]

valores_circuitos = promedio_circuitos_pico.values

# Crear la figura
plt.figure(figsize=(10, 6))

# Dibujar las barras
barras = plt.bar(
    nombres_circuitos,
    valores_circuitos
)

# Mostrar el valor encima de cada barra
plt.bar_label(
    barras,
    fmt="%.3f",
    padding=4
)

# Agregar titulo y etiquetas
plt.title(
    f"WattLens - Inside the Peak ({hora_pico}:00-{hora_pico + 1}:00)"
)

plt.xlabel("Household circuits")
plt.ylabel("Average hourly energy use (kWh)")


# Ajustar la escala vertical
plt.ylim(0, max(valores_circuitos) * 1.2)

# Agregar cuadricula
plt.grid(axis="y", alpha=0.3)

# Guardar la grafica
plt.tight_layout()

plt.savefig(
    "grafica_circuitos_pico_real.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nSEGUNDA GRAFICA REAL GENERADA CORRECTAMENTE")

# Identificar la hora de mayor consumo de cada dia

tabla_diaria = consumo_diario_horario.reset_index()

indices_maximos = tabla_diaria.groupby("fecha")[
    "energy_kwh"
].idxmax()

picos_diarios = tabla_diaria.loc[indices_maximos]

# Contar los dias en que coincide con la hora pico mensual
dias_coinciden = (picos_diarios["hora"] == hora_pico).sum()

dias_analizados = len(picos_diarios)

frecuencia = (dias_coinciden / dias_analizados) * 100

print("\nFRECUENCIA DEL HORARIO PICO:")

print(f"Dias analizados: {dias_analizados}")
print(f"Dias con pico a las {hora_pico}:00: {dias_coinciden}")
print(f"Frecuencia: {frecuencia:.2f}%")

# Preparar los resultados reales para Gemini

nombres = {
    "kitchen_kwh": "Cocina",
    "laundry_kwh": "Lavanderia",
    "water_ac_kwh": "Climatizacion y agua caliente",
    "other_kwh": "Otros consumos"
}

# Organizar el consumo por circuito
circuitos = {
    nombres[clave]: round(float(valor), 4)
    for clave, valor in promedio_circuitos_pico.items()
}

# Calcular la participacion de cada circuito
total_circuitos = promedio_circuitos_pico.sum()

porcentajes = {
    nombres[clave]: round(float(valor / total_circuitos * 100), 2)
    for clave, valor in promedio_circuitos_pico.items()
}

# Crear el resumen estadistico
resumen_real = {
    "proyecto": "WattLens",
    "tipo_datos": "Mediciones historicas reales",
    "vivienda": "Vivienda francesa",
"periodo": f"{datos['timestamp'].min():%Y-%m-%d} a {datos['timestamp'].max():%Y-%m-%d}",
    "mediciones": int(len(datos)),
    "energia_mensual_kwh": round(float(consumo_mensual), 2),
    "hora_pico": int(hora_pico),
    "energia_promedio_pico_kwh": round(float(energia_pico), 4),
    "dias_analizados": int(dias_analizados),
    "dias_con_hora_pico": int(dias_coinciden),
    "frecuencia_pico_porcentaje": round(float(frecuencia), 2),
    "consumo_circuitos_pico_kwh": circuitos,
    "porcentajes_circuitos": porcentajes,
    "observacion": (
        "Los resultados describen patrones historicos. "
        "No permiten atribuir el consumo a un aparato "
        "especifico ni asegurar un porcentaje de ahorro."
    )
}

# Evaluacion de calidad del dataset real

columnas_energia = [
    "energy_kwh",
    "kitchen_kwh",
    "laundry_kwh",
    "water_ac_kwh",
    "other_kwh"
]

# Comprobar registros duplicados y valores faltantes
duplicados = datos["timestamp"].duplicated().sum()
faltantes = datos.isna().sum().sum()

# Comprobar consumos negativos
negativos = (datos[columnas_energia] < 0).sum().sum()

# Comprobar continuidad temporal
fechas_ordenadas = datos["timestamp"].sort_values()

saltos = (
    fechas_ordenadas.diff().dropna()
    != pd.Timedelta(minutes=1)
).sum()

# Comprobar coherencia energetica
suma_circuitos = datos[
    ["kitchen_kwh", "laundry_kwh",
     "water_ac_kwh", "other_kwh"]
].sum(axis=1)

diferencias = (
    datos["energy_kwh"] - suma_circuitos
).abs()

inconsistencias = (diferencias > 0.000001).sum()

# Agregar los resultados al resumen real
resumen_real["calidad_datos"] = {
    "registros_duplicados": int(duplicados),
    "valores_faltantes": int(faltantes),
    "valores_negativos": int(negativos),
    "intervalos_irregulares": int(saltos),
    "diferencias_energia": int(inconsistencias),
    "diferencia_maxima_kwh": round(float(diferencias.max()), 8),
    
"observacion": (
    f"Se detectaron {int(inconsistencias)} registros con "
    "diferencias de coherencia energetica superiores "
    "a la tolerancia de 0.000001 kWh. "
    "Se conservaron las mediciones originales."
    if inconsistencias > 0
    else "No se detectaron diferencias de coherencia "
         "energetica superiores a la tolerancia establecida."
)
}

print("\nCALIDAD DEL DATASET INCORPORADA AL RESUMEN")

# Guardar el archivo JSON
with open("resumen_real.json", "w", encoding="utf-8") as archivo:
    json.dump(resumen_real, archivo, indent=4, ensure_ascii=False)

print("\nRESUMEN REAL PARA GEMINI GENERADO CORRECTAMENTE")
