
# WattLens - Energy Consumption Analysis

## Samsung Innovation Campus (SIC)

WattLens es un proyecto de analisis del consumo electrico
domestico mediante Python y herramientas de inteligencia
artificial.

El objetivo es identificar patrones de consumo, horarios
de mayor demanda y posibles oportunidades de ahorro
energetico a partir de mediciones historicas.

## 1. Dataset utilizado

El caso principal corresponde a una vivienda francesa
durante mayo de 2007.

- Registros: 44,640 mediciones.
- Periodo: 1 al 31 de mayo de 2007.
- Frecuencia: una medicion por minuto.
- Unidad de energia: kWh.

Archivo principal:

wattwise_mayo_2007.csv

## 2. Herramientas utilizadas

- Python
- Pandas
- Matplotlib
- JSON

## 3. Archivos principales

- analisis_real.py: analisis estadistico principal.
- wattwise_mayo_2007.csv: dataset preparado.
- resumen_real.json: resultados para Gemini.
- grafica_consumo_horario_real.png: consumo por horario.
- grafica_circuitos_pico_real.png: consumo por circuito.
- requirements.txt: librerias necesarias.

## 4. Instalacion

Abrir una terminal dentro de la carpeta del proyecto.

Instalar las dependencias:

python -m pip install -r requirements.txt

## 5. Ejecucion

Ejecutar el programa principal:

python analisis_real.py

El programa genera automaticamente las dos graficas
y el resumen estadistico en formato JSON.

## 6. Resultados principales

Para mayo de 2007:

- Consumo mensual: 733.48 kWh.
- Horario pico promedio: 21:00 a 22:00.
- Energia promedio en esa hora: 2.2547 kWh.
- Frecuencia del pico diario a las 21:00: 38.71 %.
- Circuito con mayor contribucion: Other uses.

## 7. Validacion de datos

El programa verifica:

- Columnas requeridas.
- Valores faltantes.
- Mediciones negativas.
- Fechas duplicadas.
- Continuidad temporal.
- Coherencia entre el consumo total y sus circuitos.

Se identificaron dos registros con pequenas diferencias
de coherencia energetica. Estos registros se conservaron
y las diferencias quedaron documentadas.

## 8. Integracion con Gemini

El archivo resumen_real.json contiene los resultados
estadisticos necesarios para que el modulo de inteligencia
artificial genere recomendaciones.

Las recomendaciones deben basarse en los datos disponibles
y no deben inventar cifras de ahorro ni atribuir consumos
a dispositivos especificos sin evidencia.

## 9. Limitaciones

Los resultados corresponden a mediciones historicas de
una vivienda y no representan monitoreo en tiempo real.

El analisis describe patrones de consumo, pero no demuestra
por si solo las causas de cada incremento de demanda.