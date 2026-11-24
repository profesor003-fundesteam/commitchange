# Documentación técnica

1. **Fuente y periodo:** UCI Individual Household Electric Power Consumption (Sceaux, Francia). Mayo de 2007: 31 días completos, 44 640 mediciones por minuto, sin faltantes, duplicados ni intervalos irregulares.
2. **Unidades:** energía por minuto en kWh (`energy_kwh`) y por circuito (`kitchen_kwh`, `laundry_kwh`, `water_ac_kwh`, `other_kwh`). `other_kwh` es el resto no medido por los tres submedidores.
3. **Lecturas faltantes:** ninguna en el periodo elegido. El script valida columnas, valores vacíos y negativos, fechas duplicadas, continuidad minuto a minuto y 60 registros por hora.
4. **Coherencia energética:** 2 registros difieren de la suma de circuitos en hasta 0.00036667 kWh; se conservaron las mediciones originales.
5. **Gráfica 1 (Resumen del hogar):** energía sumada por día y hora, luego promedio de cada hora entre los 31 días. Pico: 21:00, 2.2547 kWh.
6. **Gráfica 2 (Dentro del pico):** promedio por circuito durante 21:00-22:00 (suma de la hora 21 dividida entre 31 días).
7. **Frecuencia del patrón:** el máximo diario cayó en la hora 21 en 12 de 31 días (38.71 %). Es la hora más frecuente, pero no ocurre todos los días.
8. **Recorrido completo:** pico a las 21:00 -> circuito medido principal: calentador de agua y aire acondicionado (0.55 kWh, 24.6 %) -> resumen a Gemini (`analisis/resumen_real.json`) -> recomendación revisada en la pantalla 3.
9. **Limitaciones:** el circuito 3 agrupa calentador de agua y aire acondicionado, y "Otros usos" es lo que no se mide; atribuir el pico a un equipo exige otra medición. Una sola vivienda y un solo mes.
