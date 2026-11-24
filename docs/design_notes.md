# Notas de diseño de las pantallas

- Formato 1920x1080 (16:9) para insertar en la plantilla de Samsung.
- Mismo encabezado en las 3 pantallas: nombre de la vivienda, periodo y unidades (kWh).
- Ámbar = solo lo que hay que mirar (franja pico, circuito principal). Turquesa = datos normales.
- Todo el texto está en español; los nombres de grupos y etiquetas de ejes se cambian en `src/wattwise/config.py`.
- Mientras los datos no sean reales, las pantallas llevan la etiqueta "Datos ilustrativos".
- Tipografía: Inter (poner los .otf/.ttf en ui/fonts/ si no la tienen instalada; si no, se usa Arial/DejaVu).
- Tamaño de cada gráfica: 1140 x 660 px.
