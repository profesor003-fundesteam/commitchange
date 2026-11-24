#!/usr/bin/env python
"""Genera las 3 pantallas de WattWise como PNG de 1920x1080 (16:9).

    python ui/make_screens.py          # pantallas con HUECOS (o con las gráficas reales si ya existen)
    python ui/make_screens.py --demo   # pantallas con datos de muestra (Datos ilustrativos)

Textos: ui/screen_content.json
Gráficas reales (las busca solas): outputs/figures/fig1_hourly_profile.png
                                   outputs/figures/fig2_peak_breakdown.png
Salida:  outputs/screens/ (o outputs/screens_demo/ con --demo)
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from wattwise import config as C  # noqa: E402
from wattwise.plots import plot_hourly_profile, plot_peak_breakdown  # noqa: E402

W, H = 1920, 1080
COL = C.COLORS
CHART_W, CHART_H = int(C.FIG_SIZE_INCHES[0] * C.DPI), int(C.FIG_SIZE_INCHES[1] * C.DPI)

NAV = ["Resumen del hogar", "Dentro del pico", "Tu consejo de energía"]
FILES = ["pantalla1_resumen_hogar.png", "pantalla2_dentro_del_pico.png", "pantalla3_consejo_de_energia.png"]

FONT_FILES = {
    "regular": ["Inter-Regular.otf", "Inter-Regular.ttf", "Arial.ttf", "arial.ttf", "DejaVuSans.ttf"],
    "semibold": ["Inter-SemiBold.otf", "Inter-SemiBold.ttf", "Arial Bold.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"],
    "bold": ["Inter-Bold.otf", "Inter-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"],
}
FONT_DIRS = [ROOT / "ui" / "fonts", Path("/usr/share/fonts/opentype/inter")]


def font(weight, size):
    for name in FONT_FILES[weight]:
        for d in FONT_DIRS:
            if (d / name).exists():
                return ImageFont.truetype(str(d / name), size)
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def paragraph(draw, xy, text, fnt, fill, max_w, spacing=1.35):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * spacing)
    return y


def rounded(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def dashed_box(draw, box, color, r=18, dash=14, gap=10, width=3):
    x0, y0, x1, y1 = box
    for x in range(x0 + r, x1 - r, dash + gap):
        draw.line([(x, y0), (min(x + dash, x1 - r), y0)], fill=color, width=width)
        draw.line([(x, y1), (min(x + dash, x1 - r), y1)], fill=color, width=width)
    for y in range(y0 + r, y1 - r, dash + gap):
        draw.line([(x0, y), (x0, min(y + dash, y1 - r))], fill=color, width=width)
        draw.line([(x1, y), (x1, min(y + dash, y1 - r))], fill=color, width=width)


def badge(draw, right, top, text):
    f = font("semibold", 22)
    tw = draw.textlength(text, font=f)
    box = (right - tw - 36, top, right, top + 44)
    rounded(draw, box, 22, fill=COL["amber_soft"])
    draw.text((box[0] + 18, top + 8), text, font=f, fill=COL["ink"])


def chart_slot(img, draw, box, fig_path, hint, size_hint):
    """Pega la gráfica real si existe; si no, dibuja el hueco con instrucciones."""
    x0, y0, x1, y1 = box
    if fig_path and fig_path.exists():
        fig = Image.open(fig_path).convert("RGB")
        fig.thumbnail((x1 - x0, y1 - y0), Image.LANCZOS)
        img.paste(fig, (x0 + (x1 - x0 - fig.width) // 2, y0 + (y1 - y0 - fig.height) // 2))
        return
    rounded(draw, box, 18, fill="#F7FAFB")
    dashed_box(draw, box, "#9DB4BC")
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    f1, f2, f3 = font("semibold", 34), font("regular", 24), font("regular", 22)
    for text, f, dy, fill in [
        (hint, f1, -50, COL["ink"]),
        (f"Insertar: outputs/figures/{fig_path.name}", f2, 8, COL["slate"]),
        (size_hint, f3, 48, COL["slate"]),
    ]:
        draw.text((cx - draw.textlength(text, font=f) / 2, cy + dy), text, font=f, fill=fill)


def chrome(content, active, illustrative):
    """Cabecera, pestañas, pregunta y pie: iguales en las tres pantallas."""
    img = Image.new("RGB", (W, H), COL["paper"])
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 112), fill=COL["panel"])
    d.line((0, 112, W, 112), fill=COL["line"], width=2)
    # marca
    d.ellipse((80, 30, 128, 78), outline=COL["teal"], width=7)
    d.ellipse((96, 46, 112, 62), fill=COL["amber"])
    d.text((146, 28), "WattWise", font=font("bold", 46), fill=COL["ink"])
    # vivienda y periodo
    f_h, f_s = font("semibold", 27), font("regular", 24)
    for text, f, y, fill in [
        (content["household_name"], f_h, 24, COL["ink"]),
        (f"Periodo: {content['period']}", f_s, 58, COL["slate"]),
    ]:
        d.text((W - 80 - d.textlength(text, font=f), y), text, font=f, fill=fill)
    # pestañas
    x, f_t = 80, font("semibold", 26)
    for i, name in enumerate(NAV):
        tw = d.textlength(name, font=f_t)
        box = (x, 140, x + tw + 56, 192)
        if i == active:
            rounded(d, box, 26, fill=COL["ink"])
            d.text((x + 28, 150), name, font=f_t, fill="white")
        else:
            rounded(d, box, 26, outline=COL["line"], width=3)
            d.text((x + 28, 150), name, font=f_t, fill=COL["slate"])
        x = box[2] + 16
    # pie
    d.text((80, 1030), "WattWise  |  Commint4Change  |  Samsung Innovation Campus Panamá",
           font=font("regular", 20), fill=COL["slate"])
    if illustrative:
        badge(d, W - 80, 1022, "Datos ilustrativos")
    return img, d


def peak_chip(d, x, y, w, content):
    """Franja destacada: se repite en las pantallas 1 y 2 para que el horario siga visible."""
    rounded(d, (x, y, x + w, y + 170), 22, fill=COL["amber_soft"])
    d.text((x + 32, y + 22), "Hora pico", font=font("semibold", 26), fill=COL["slate"])
    d.text((x + 32, y + 62), content["peak"]["window"], font=font("bold", 64), fill=COL["ink"])


def screen1(c, figs):
    img, d = chrome(c, 0, c["illustrative"])
    d.text((80, 222), c["screen1"]["question"], font=font("semibold", 42), fill=COL["ink"])
    rounded(d, (80, 300, 1260, 1000), 26, fill=COL["panel"])
    chart_slot(img, d, (100, 320, 1240, 980), figs["hourly"], "Gráfica 1: consumo promedio por hora", f"{CHART_W} x {CHART_H} px")
    peak_chip(d, 1300, 300, 540, c)
    rounded(d, (1300, 490, 1840, 1000), 26, fill=COL["panel"])
    d.text((1336, 520), "Qué significa", font=font("semibold", 26), fill=COL["teal"])
    y = paragraph(d, (1336, 566), c["screen1"]["result"], font("regular", 32), COL["ink"], 468)
    p = c["peak"]
    paragraph(d, (1336, y + 24), f"Fue el máximo del día en {p['days_observed']} de {p['days_total']} días",
              font("semibold", 28), COL["ink"], 468, 1.3)
    return img


def screen2(c, figs):
    img, d = chrome(c, 1, c["illustrative"])
    d.text((80, 222), c["screen2"]["question"], font=font("semibold", 42), fill=COL["ink"])
    rounded(d, (80, 300, 1260, 1000), 26, fill=COL["panel"])
    chart_slot(img, d, (100, 320, 1240, 980), figs["peak"], "Gráfica 2: energía por grupo durante el pico", f"{CHART_W} x {CHART_H} px")
    peak_chip(d, 1300, 300, 540, c)
    rounded(d, (1300, 490, 1840, 1000), 26, fill=COL["panel"])
    d.text((1336, 520), "Mayor aporte medido", font=font("semibold", 26), fill=COL["teal"])
    s2 = c["screen2"]
    y = paragraph(d, (1336, 566), s2["top_group"], font("bold", 32), COL["ink"], 468, 1.25)
    d.text((1336, y + 6), s2["top_kwh"], font=font("bold", 46), fill=COL["amber"])
    paragraph(d, (1336, y + 84), s2["result"], font("regular", 28), COL["ink"], 468)
    paragraph(d, (1336, 880), s2["note"], font("regular", 21), COL["slate"], 468, 1.3)
    return img


def screen3(c, figs):
    img, d = chrome(c, 2, c["illustrative"])
    d.text((80, 222), c["screen3"]["question"], font=font("semibold", 42), fill=COL["ink"])
    # gráfica que respalda la recomendación (mismo hueco, formato más pequeño)
    rounded(d, (80, 300, 980, 1000), 26, fill=COL["panel"])
    d.text((112, 326), "Los datos detrás del consejo", font=font("semibold", 26), fill=COL["teal"])
    chart_slot(img, d, (100, 370, 960, 985), figs["peak"], "Gráfica de respaldo", "Reutilizar la Gráfica 2")
    cards = [("Qué encontramos", "found", COL["teal"]), ("Qué puedes probar", "try", COL["amber"]),
             ("Cómo comprobarlo", "check", COL["ink"])]
    for i, (title, key, color) in enumerate(cards):
        top = 300 + i * 240
        rounded(d, (1020, top, 1840, top + 220), 26, fill=COL["panel"])
        d.rounded_rectangle((1020, top, 1038, top + 220), 9, fill=color)
        d.text((1068, top + 24), title, font=font("semibold", 28), fill=COL["teal"])
        paragraph(d, (1068, top + 70), c["screen3"][key], font("regular", 30), COL["ink"], 740, 1.3)
    return img


DEMO = {
    "illustrative": True,
    "period": "Mes ilustrativo",
    "peak": {"window": "18:00-19:00", "days_observed": "21", "days_total": "28"},
    "screen1": {"question": None,
                "result": "Tu hogar usó más electricidad alrededor de las 18:00."},
    "screen2": {"top_group": "Lavandería", "top_kwh": "0.90 kWh",
                "result": "Lavandería aportó más energía durante la franja pico."},
}


def merge(base, extra):
    for k, v in extra.items():
        if isinstance(v, dict):
            merge(base[k], v)
        elif v is not None:
            base[k] = v
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="usa datos de muestra")
    a = ap.parse_args()
    c = json.loads((ROOT / "ui" / "screen_content.json").read_text(encoding="utf-8"))
    figdir = ROOT / "outputs" / "figures"
    outdir = ROOT / "outputs" / ("screens_demo" if a.demo else "screens")
    outdir.mkdir(parents=True, exist_ok=True)

    if a.demo:
        c = merge(c, DEMO)
        figdir = ROOT / "outputs" / "figures_demo"
        sample = [0.35, 0.28, 0.24, 0.22, 0.21, 0.26, 0.45, 0.70, 0.62, 0.48, 0.42, 0.46, 0.55,
                  0.50, 0.44, 0.42, 0.50, 0.72, 0.98, 0.90, 0.74, 0.62, 0.50, 0.41]
        plot_hourly_profile(sample, 18, figdir / C.FIG_HOURLY, illustrative=True)
        plot_peak_breakdown({"sub_metering_1": 0.12, "sub_metering_2": 0.90,
                             "sub_metering_3": 0.34, "other": 0.54}, "18:00-19:00",
                            figdir / C.FIG_PEAK, illustrative=True)

    figs = {"hourly": figdir / C.FIG_HOURLY, "peak": figdir / C.FIG_PEAK}
    for fn, build in zip(FILES, (screen1, screen2, screen3)):
        build(c, figs).save(outdir / fn)
        print("OK", outdir / fn)


if __name__ == "__main__":
    main()
