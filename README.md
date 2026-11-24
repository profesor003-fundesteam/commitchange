# WattWise

> WattWise ayuda a las familias a ver en qué momento usan más electricidad y a elegir un cambio práctico para probar en casa.

Proyecto del equipo **Commint4Change** (Samsung Innovation Campus Panamá). Usa las lecturas de una vivienda
(UCI *Individual Household Electric Power Consumption*) para encontrar la hora de mayor consumo, ver qué
circuito aporta más en esa franja y proponer, con ayuda de Gemini, una acción que la familia pueda probar.
ODS 7: eficiencia energética.

## Estructura

```
wattwise/
├── analisis/            # análisis real de mayo de 2007 (analisis_real.py, CSV, resumen_real.json)
├── data/raw/            # archivo completo de UCI (NO se sube a GitHub; ver data/README.md)
├── data/processed/      # tablas intermedias
├── notebooks/           # esqueleto opcional del cuaderno
├── src/wattwise/
│   ├── config.py        # nombres de grupos, colores, tamaños (un solo lugar)
│   └── plots.py         # las 2 gráficas con el estilo del producto
├── gemini/              # plantilla del resumen enviado a Gemini + respuesta revisada
├── ui/
│   ├── build_from_analysis.py # gráficas en español + números de las pantallas desde analisis/
│   ├── screen_content.json    # textos de las 3 pantallas
│   └── make_screens.py        # genera los PNG de las pantallas
├── outputs/
│   ├── figures/         # fig1_hourly_profile.png, fig2_peak_breakdown.png (finales)
│   └── screens/         # 3 pantallas finales
└── docs/                # documentación del análisis y notas de diseño
```

## Cómo reproducir

```bash
python -m venv .venv && source .venv/bin/activate      # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
# 1. Análisis real (genera gráficas originales y resumen_real.json)
cd analisis && python analisis_real.py && cd ..
# 2. Gráficas en español con el estilo de la interfaz + números de las pantallas
python ui/build_from_analysis.py
# 3. Pantallas finales (1920x1080)
python ui/make_screens.py
```

## Resultados (mayo de 2007, 44 640 mediciones)

- Hora pico: 21:00 a 22:00, con 2.25 kWh en promedio. Fue la hora de mayor consumo del día en 12 de 31 días (38.7 %).
- Durante esa hora: Otros usos del hogar 1.16 kWh (51.7 %), Calentador de agua y aire acondicionado 0.55 kWh (24.6 %), Cocina 0.38 kWh (16.8 %), Lavandería 0.16 kWh (6.9 %).
- Los resultados describen patrones históricos; no permiten atribuir el consumo a un aparato ni prometer un porcentaje de ahorro.

## Datos y licencia

Hébrail, G. y Berard, A. (2006). *Individual Household Electric Power Consumption* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C58K54. Licencia CC BY 4.0: se puede compartir y adaptar con la atribución correspondiente. `analisis/wattwise_mayo_2007.csv` es un subconjunto preparado de ese conjunto, así que debe conservar esta atribución.

## Equipo
Commint4Change, Panamá. Datos: Hébrail y Berard, UCI Machine Learning Repository (vivienda en Sceaux, Francia).
