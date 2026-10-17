#!/usr/bin/env python3
"""Sustituye fotos de la web por las versiones mejoradas con ChatGPT (fuentes/chatgpt/<nombre>-gpt.png).

Solo las aprobadas tras compararlas con el original (ver README). No se les aplica más
corrección de color: ChatGPT ya las entrega limpias. Exporta WebP 800 y 1600 px y
actualiza dimensiones.txt.
Uso: python3 -I herramientas/fotos_gpt.py
"""
import os
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GPT = os.path.join(RAIZ, "fuentes", "chatgpt")
SALIDA = os.path.join(RAIZ, "public", "img", "fotos")

# foto de la web: foto mejorada de origen
APROBADAS = {
    "polar-lobby": "polar-lobby", "polar-h2so4": "polar-h2so4", "polar-revestimiento": "polar-revestimiento",
    "polar-piso": "polar-piso", "polar-tanques": "polar-tanques", "polar-escalera": "polar-escalera",
    "polar-bomba": "polar-bomba", "polar-entrada": "polar-entrada",
    "tijerazo-foso": "tijerazo-foso", "tijerazo-estructura": "tijerazo-estructura",
    "tijerazo-entrepiso": "tijerazo-entrepiso", "tijerazo-losa": "tijerazo-losa",
    "digitel-crucero": "digitel-crucero", "digitel-torre": "digitel-torre", "digitel-andamio": "digitel-andamio",
    "digitel-izado": "digitel-izado", "digitel-antenas": "digitel-antenas", "digitel-azotea": "digitel-azotea",
    # servicios que reutilizan fotos de obra
    "srv-construccion": "tijerazo-foso", "srv-mantenimiento": "polar-revestimiento", "srv-telecom": "digitel-torre",
}
# Descartadas: srv-ingenieria (cara inventada), srv-levantamientos (marca inventada en el equipo)

ruta_dim = os.path.join(SALIDA, "dimensiones.txt")
dims = dict(l.split(None, 1) for l in open(ruta_dim).read().splitlines() if l.strip())
for nombre, origen in APROBADAS.items():
    im = Image.open(os.path.join(GPT, origen + "-gpt.jpg")).convert("RGB")
    for ancho in (800, 1600):
        f = ancho / im.width
        out = im if f >= 1 else im.resize((ancho, round(im.height * f)), Image.LANCZOS)
        out.save(os.path.join(SALIDA, f"{nombre}-{ancho}.webp"), "WEBP", quality=82, method=6)
    w16 = min(1600, im.width)
    dims[nombre] = f"{w16} {round(im.height * w16 / im.width)}"
    print(nombre, im.size)
open(ruta_dim, "w").write("\n".join(f"{k} {v}" for k, v in dims.items()) + "\n")
