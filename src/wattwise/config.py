"""Constantes compartidas por el análisis, las gráficas y las pantallas.

Si cambian un nombre, un color o un tamaño, háganlo AQUÍ para que las
tres pantallas y las dos gráficas sigan viéndose iguales.
"""

# --- Paleta -----------------------------------------------------------------
COLORS = {
    "ink": "#10262E",      # texto principal
    "slate": "#5B707A",    # texto secundario
    "paper": "#EDF2F4",    # fondo de la pantalla
    "panel": "#FFFFFF",    # tarjetas y paneles
    "teal": "#1B7F8C",     # datos normales
    "teal_soft": "#CFE5E8",
    "amber": "#F2A02B",    # SOLO para lo que hay que mirar (pico, circuito principal)
    "amber_soft": "#FCE9C9",
    "line": "#D5DEE2",
}

# --- Nombres de los grupos (etiquetas en español para la interfaz) -----------
# Sub_metering_1 = cocina (lavavajillas, horno, microondas)
# Sub_metering_2 = lavandería (lavadora, secadora, refrigerador, una luz)
# Sub_metering_3 = calentador de agua eléctrico y aire acondicionado
# "other"        = energía activa global - (sub1 + sub2 + sub3), en kWh
GROUP_ORDER = ["sub_metering_1", "sub_metering_2", "sub_metering_3", "other"]
GROUP_LABELS = {
    "sub_metering_1": "Cocina",
    "sub_metering_2": "Lavandería",
    "sub_metering_3": "Calentador de agua y aire acondicionado",
    "other": "Otros usos del hogar",
}

# --- Etiquetas de ejes ---------------------------------------------
LABEL_X_HOURLY = "Hora del día"
LABEL_Y_HOURLY = "Consumo promedio por hora (kWh)"
LABEL_PEAK = "Hora pico"
LABEL_X_BREAKDOWN = "Energía promedio durante la franja pico (kWh)"

# --- Gráficas: tamaño fijo para que encajen en el hueco de la pantalla ------
FIG_SIZE_INCHES = (11.4, 6.6)
DPI = 100                      # 1140 x 660 px
FIG_HOURLY = "fig1_hourly_profile.png"
FIG_PEAK = "fig2_peak_breakdown.png"

# --- Identidad del caso -----------------------------------------------------
HOUSEHOLD_NAME = "Vivienda en Sceaux, Francia"
