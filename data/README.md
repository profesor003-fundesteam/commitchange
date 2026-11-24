# Datos

**Fuente:** UCI Machine Learning Repository, *Individual Household Electric Power Consumption*
(buscar el nombre en archive.ics.uci.edu). Archivo esperado: `data/raw/household_power_consumption.txt`
(separador `;`, valores faltantes como `?`).

- Vivienda en Sceaux (a 7 km de París, Francia), de diciembre de 2006 a noviembre de 2010, con 2 075 259 mediciones por minuto.
- Se descartó el conjunto de casas alemanas (Open Power System Data) en esta primera versión: por el tiempo disponible, su cantidad y variedad no permiten un buen análisis.

| Columna | Unidad | Uso en WattWise |
|---|---|---|
| Date (dd/mm/yyyy), Time (hh:mm:ss) | | unir en un solo datetime |
| Global_active_power | kW (promedio por minuto) | energía = kW x 1/60 h = kWh |
| Sub_metering_1 | Wh | Cocina (lavavajillas, horno, microondas) |
| Sub_metering_2 | Wh | Lavandería (lavadora, secadora, refrigerador, una luz) |
| Sub_metering_3 | Wh | Calentador de agua y aire acondicionado |
| Global_reactive_power, Voltage, Global_intensity | | no se usan |

**Otros usos del hogar** = `Global_active_power/60 - (sub1 + sub2 + sub3)/1000` (kWh, por minuto).
