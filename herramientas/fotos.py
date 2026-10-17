#!/usr/bin/env python3
"""Prepara las fotos de la web: toma la versión mejorada con Real-ESRGAN si existe
(scratchpad/sr/out), si no la original; corrige contraste y color con suavidad y
exporta WebP a 800 y 1600 px en public/img/fotos.
Uso: python3 herramientas/fotos.py <carpeta_entrada> <carpeta_sr>"""
import os, sys
import numpy as np, cv2
from PIL import Image, ImageEnhance, ImageFilter

ENTRADA, SR = sys.argv[1], sys.argv[2]
SALIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "img", "fotos")
os.makedirs(SALIDA, exist_ok=True)

# nombre final: (archivo de origen, recorte relativo (izq, arriba, der, abajo) o None)
MAPA = {
    "deposito-columnas": ("f_bf3abbaf", None),
    "deposito-cercha": ("f_d017b5d5", None),
    "deposito-montaje": ("f_c99523cd", None),
    "deposito-acarreo": ("f_e7d1f833", (0, 0, 1, .86)),
    "gabriel-forero": ("f_df685ed4", None),
    "plaza-mayor-rio": ("f_ba640bc1", None),
    "srv-procura": ("f_87782e15", None),
    "tijerazo-foso": ("p13_234", None),
    "tijerazo-estructura": ("p13_237", None),
    "tijerazo-entrepiso": ("p09_187", None),
    "tijerazo-losa": ("p07_142", None),
    "digitel-crucero": ("p14_245", None),
    "digitel-torre": ("p09_176", None),
    "digitel-andamio": ("p09_173", None),
    "digitel-izado": ("p14_248", None),
    "digitel-antenas": ("p14_251", None),
    "digitel-azotea": ("p14_254", None),
    "polar-lobby": ("p10_195", None),
    "polar-h2so4": ("p12_219", None),
    "polar-revestimiento": ("p12_217", None),
    "polar-piso": ("p11_206", None),
    "polar-tanques": ("p11_208", None),
    "polar-escalera": ("p10_193", None),
    "polar-bomba": ("p05_101", None),
    "polar-entrada": ("p10_191", None),
    "srv-ingenieria": ("p07_139", None),
    "srv-construccion": ("p13_234", None),
    "srv-mantenimiento": ("p12_217", None),
    "srv-telecom": ("p09_176", None),
    "srv-levantamientos": ("p03_67", None),
}


def cargar(base):
    sr = os.path.join(SR, base + ".png")
    if os.path.exists(sr):
        return Image.open(sr).convert("RGB"), True
    im = Image.open(os.path.join(ENTRADA, base + ".png")).convert("RGB")
    f = 1600 / max(im.size)
    if f > 1:
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    return im, False


def corregir(im, mejorada):
    a = np.asarray(im)
    lab = cv2.cvtColor(a, cv2.COLOR_RGB2LAB)
    l, aa, bb = cv2.split(lab)
    # contraste local suave en luminancia (sin tocar el color)
    l = cv2.createCLAHE(clipLimit=1.4, tileGridSize=(8, 8)).apply(l)
    # estirar niveles 0,4 % a 99,6 %
    lo, hi = np.percentile(l, (0.4, 99.6))
    l = np.clip((l.astype(np.float32) - lo) * 255.0 / max(hi - lo, 1), 0, 255).astype(np.uint8)
    a = cv2.cvtColor(cv2.merge((l, aa, bb)), cv2.COLOR_LAB2RGB)
    im = Image.fromarray(a)
    im = ImageEnhance.Color(im).enhance(1.08)
    if not mejorada:
        im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    return im


dims = []
for nombre, (base, rec) in MAPA.items():
    im, mejorada = cargar(base)
    if rec:
        w, h = im.size
        im = im.crop((int(rec[0] * w), int(rec[1] * h), int(rec[2] * w), int(rec[3] * h)))
    im = corregir(im, mejorada)
    for ancho in (800, 1600):
        f = ancho / im.width
        out = im if f >= 1 else im.resize((ancho, round(im.height * f)), Image.LANCZOS)
        out.save(os.path.join(SALIDA, f"{nombre}-{ancho}.webp"), "WEBP", quality=80, method=6)
    w16 = min(1600, im.width)
    dims.append(f"{nombre} {w16} {round(im.height * w16 / im.width)}")
    print(nombre, "SR" if mejorada else "lanczos", im.size)
open(os.path.join(SALIDA, "dimensiones.txt"), "w").write("\n".join(dims) + "\n")
