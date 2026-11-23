# -*- coding: utf-8 -*-
"""Genera una publicación de Instagram (1080x1080) de MFD con Pillow. Gratis, sin API."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(HERE, "post_instagram.png")
FONDO = (14, 10, 12)
ROJO = (220, 38, 38)
BLANCO = (245, 240, 238)
GRIS = (170, 160, 160)
F = "C:/Windows/Fonts/"

def fuente(nombre, tam):
    return ImageFont.truetype(F + nombre, tam)

def centrado(d, texto, y, font, color):
    ancho = d.textlength(texto, font=font)
    d.text(((1080 - ancho) / 2, y), texto, font=font, fill=color)

img = Image.new("RGB", (1080, 1080), FONDO)
d = ImageDraw.Draw(img)

for i in range(0, 1080, 4):
    t = i / 1080
    d.line([(0, i), (1080, i)], fill=(int(14 + 30 * (1 - t) * 0.3), 10, int(12 + 10 * (1 - t))))

d.rectangle([60, 60, 1020, 1020], outline=(70, 22, 26), width=2)

centrado(d, "MFD", 110, fuente("impact.ttf", 64), ROJO)
centrado(d, "MARKETING & EVENTOS", 190, fuente("arialbd.ttf", 26), GRIS)

d.line([(440, 265), (640, 265)], fill=ROJO, width=3)

centrado(d, "HACEMOS MARCAS", 320, fuente("arialbd.ttf", 90), BLANCO)
centrado(d, "de corazón.", 440, fuente("georgiab.ttf", 96), ROJO)

linea = fuente("arial.ttf", 38)
centrado(d, "Experiencias reales que conectan marcas", 600, linea, BLANCO)
centrado(d, "con personas en Cali y en toda Colombia.", 650, linea, BLANCO)

stats = [("15", "años"), ("50+", "clientes"), ("7", "líneas de trabajo")]
ancho_col = 300
inicio = (1080 - ancho_col * len(stats)) / 2
for n, (num, etiqueta) in enumerate(stats):
    x = inicio + n * ancho_col + ancho_col / 2
    numf = fuente("impact.ttf", 80)
    w = d.textlength(num, font=numf)
    d.text((x - w / 2, 760), num, font=numf, fill=ROJO)
    lw = d.textlength(etiqueta, font=fuente("arial.ttf", 28))
    d.text((x - lw / 2, 860), etiqueta, font=fuente("arial.ttf", 28), fill=GRIS)

centrado(d, "Cobertura nacional · Eventos · Activaciones · Producción", 935, fuente("arial.ttf", 26), GRIS)
centrado(d, "mfdmarketingeventos.com", 985, fuente("arialbd.ttf", 30), BLANCO)

img.save(SALIDA)
print(SALIDA)
