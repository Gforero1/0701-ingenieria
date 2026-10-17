#!/usr/bin/env python3
"""Vectoriza el logo del brochure (PNG de 408 px) con potrace limpio.

Uso: python3 -I herramientas/logo_vector.py <logo.png> <carpeta_salida>
Sube la imagen x10 con interpolación suave, umbraliza al 50 % y traza con
potrace (alphamax alto y optimización de curvas) para que las rectas salgan
rectas y las curvas lisas. Genera logo.svg (marca + INGENIERIA C.A.) y
marca.svg (solo el 0701), pintados con currentColor.
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
import potrace

ESC = 10
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
a = np.asarray(im).astype(float)
azul = np.array([0x1d, 0x45, 0x69], float)
blanco = np.array([255, 255, 255.0])
t = np.clip(((blanco - a) @ (blanco - azul)) / ((blanco - azul) @ (blanco - azul)), 0, 1)
tinta = Image.fromarray((t * 255).astype(np.uint8), "L")


def trazar(filas, nombre):
    y0, y1 = filas
    parte = tinta.crop((0, y0, tinta.width, y1))
    caja = parte.point(lambda v: 255 if v > 13 else 0).getbbox()
    parte = parte.crop(caja)
    w, h = parte.size
    grande = parte.resize((w * ESC, h * ESC), Image.LANCZOS).filter(ImageFilter.GaussianBlur(ESC * 0.9))
    bits = np.asarray(grande) <= 127  # potracer rellena los False
    trazo = potrace.Bitmap(bits).trace(turdsize=40, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
                                       alphamax=1.2, opticurve=True, opttolerance=1.0)
    d = []
    f = lambda p: f"{p.x / ESC:.2f},{p.y / ESC:.2f}"
    for curva in trazo:
        d.append("M" + f(curva.start_point))
        for s in curva.segments:
            if s.is_corner:
                d.append("L" + f(s.c) + "L" + f(s.end_point))
            else:
                d.append("C" + f(s.c1) + " " + f(s.c2) + " " + f(s.end_point))
        d.append("Z")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
           f'<path fill="currentColor" fill-rule="evenodd" d="{"".join(d)}"/></svg>')
    open(f"{out}/{nombre}.svg", "w").write(svg)
    print(nombre, w, h, len(svg), "bytes")


# Filas del PNG: 0-193 el 0701, 211-240 INGENIERIA C.A., 262-280 el RIF (fuera)
trazar((0, 245), "logo")
trazar((0, 196), "marca")
