#!/usr/bin/env python
"""Puente entre el análisis real y la interfaz.

Lee analisis/resumen_real.json y analisis/wattwise_mayo_2007.csv, genera las dos gráficas en español
(outputs/figures/) y actualiza los números de ui/screen_content.json. Después ejecutar:
    python ui/make_screens.py
No modifica analisis_real.py: solo reutiliza sus resultados.
"""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from wattwise import config as C  # noqa: E402
from wattwise.plots import plot_hourly_profile, plot_peak_breakdown  # noqa: E402

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]

resumen = json.loads((ROOT / "analisis" / "resumen_real.json").read_text(encoding="utf-8"))
datos = pd.read_csv(ROOT / "analisis" / "wattwise_mayo_2007.csv", parse_dates=["timestamp"])

# Mismo cálculo que analisis_real.py: energía por día y hora, promedio de cada hora del día
por_hora = (datos.groupby([datos["timestamp"].dt.date, datos["timestamp"].dt.hour])["energy_kwh"]
            .sum().groupby(level=1).mean())
avg_by_hour = [float(v) for v in por_hora.sort_index().values]
peak_hour = int(resumen["hora_pico"])
assert peak_hour == int(por_hora.idxmax()), "El pico recalculado no coincide con resumen_real.json"
assert abs(avg_by_hour[peak_hour] - resumen["energia_promedio_pico_kwh"]) < 1e-3

circ = resumen["consumo_circuitos_pico_kwh"]
pct = resumen["porcentajes_circuitos"]
kwh_by_group = {"sub_metering_1": circ["Cocina"], "sub_metering_2": circ["Lavanderia"],
                "sub_metering_3": circ["Climatizacion y agua caliente"], "other": circ["Otros consumos"]}

ventana = f"{peak_hour:02d}:00-{peak_hour + 1:02d}:00"
figs = ROOT / "outputs" / "figures"
plot_hourly_profile(avg_by_hour, peak_hour, figs / C.FIG_HOURLY)
plot_peak_breakdown(kwh_by_group, ventana, figs / C.FIG_PEAK)

# Circuito medido con mayor aporte (se excluye "Otros usos del hogar": es el resto no medido)
top = max(("sub_metering_1", "sub_metering_2", "sub_metering_3"), key=lambda k: kwh_by_group[k])
top_pct = pct[{"sub_metering_1": "Cocina", "sub_metering_2": "Lavanderia",
               "sub_metering_3": "Climatizacion y agua caliente"}[top]]
otros, otros_pct = kwh_by_group["other"], pct["Otros consumos"]

jpath = ROOT / "ui" / "screen_content.json"
c = json.loads(jpath.read_text(encoding="utf-8"))
ini, fin = resumen["periodo"].split(" a ")
c["illustrative"] = False
c["period"] = f"{MESES[int(ini[5:7]) - 1].capitalize()} {ini[:4]}"
c["peak"] = {"window": ventana, "days_observed": str(resumen["dias_con_hora_pico"]),
             "days_total": str(resumen["dias_analizados"])}
c["screen1"]["result"] = (f"Tu hogar usó más electricidad entre las {peak_hour:02d}:00 y las {peak_hour + 1:02d}:00, "
                          f"con {resumen['energia_promedio_pico_kwh']:.2f} kWh en promedio.")
c["screen2"]["top_group"] = C.GROUP_LABELS[top]
c["screen2"]["top_kwh"] = f"{kwh_by_group[top]:.2f} kWh ({top_pct + 1e-9:.1f}%)"
c["screen2"]["result"] = "Es el circuito medido que más aportó durante la franja pico."
c["screen2"]["note"] = (f"Otros usos del hogar ({otros:.2f} kWh, {otros_pct + 1e-9:.1f}%) reúne lo que los tres "
                        "submedidores no miden; no se puede atribuir a un equipo.")
jpath.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
print("OK: gráficas y ui/screen_content.json actualizados.", ventana, "| circuito medido principal:", C.GROUP_LABELS[top])
