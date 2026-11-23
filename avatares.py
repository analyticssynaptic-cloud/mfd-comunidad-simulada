# -*- coding: utf-8 -*-
"""Genera un avatar SVG (muñequito) por persona. Gratis, sin dependencias.
Uso: python avatares.py  ->  avatares/SIM-00001.svg ...
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
PERSONAS = os.path.join(HERE, "personas.jsonl")
SALIDA = os.path.join(HERE, "avatares")

PIEL = ["#f1c7a5", "#d9a57c", "#b47c52", "#8d5a3b", "#5e3b26"]
PELO = ["#1a1a1a", "#4a2c17", "#8b5a2b", "#c9a46a", "#7a1f1f", "#555555"]
CAMISA = {1: "#7c8b99", 2: "#5b8fa3", 3: "#3d7d5a", 4: "#b07d2b", 5: "#8a3b7d", 6: "#b02a2a"}

def svg(p):
    r = random.Random(p["id"])
    piel = r.choice(PIEL)
    pelo = r.choice(PELO)
    camisa = CAMISA[p["estrato"]]
    partes = []
    partes.append('<rect width="96" height="96" rx="20" fill="#18131a"/>')
    partes.append(f'<path d="M14 96 Q14 66 48 64 Q82 66 82 96 Z" fill="{camisa}"/>')
    if p["genero"] == "F":
        partes.append(f'<path d="M24 46 Q24 18 48 18 Q72 18 72 46 L72 66 Q48 74 24 66 Z" fill="{pelo}"/>')
    partes.append(f'<rect x="42" y="56" width="12" height="10" fill="{piel}"/>')
    partes.append(f'<ellipse cx="48" cy="44" rx="20" ry="22" fill="{piel}"/>')
    if p["genero"] == "M" or p["edad"] < 45:
        partes.append(f'<path d="M27 40 Q28 20 48 20 Q68 20 69 40 Q62 30 48 30 Q34 30 27 40 Z" fill="{pelo}"/>')
    if p["genero"] == "M" and p["edad"] > 35:
        partes.append(f'<path d="M36 54 Q48 62 60 54 Q58 60 48 61 Q38 60 36 54 Z" fill="{pelo}" opacity="0.8"/>')
    partes.append('<circle cx="41" cy="44" r="2.4" fill="#1a1a1a"/><circle cx="55" cy="44" r="2.4" fill="#1a1a1a"/>')
    partes.append('<path d="M42 53 Q48 57 54 53" stroke="#1a1a1a" stroke-width="2" fill="none" stroke-linecap="round"/>')
    if p["personalidad"] == "analítico":
        partes.append('<g fill="none" stroke="#1a1a1a" stroke-width="1.8"><rect x="34" y="40" width="12" height="9" rx="3"/><rect x="50" y="40" width="12" height="9" rx="3"/><line x1="46" y1="43" x2="50" y2="43"/></g>')
    if p["genero"] == "F" and p["personalidad"] == "emocional":
        partes.append('<circle cx="26" cy="54" r="2.5" fill="#f5c542"/><circle cx="70" cy="54" r="2.5" fill="#f5c542"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96">'
            + "".join(partes) + "</svg>")

if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    n = 0
    with open(PERSONAS, encoding="utf-8") as f:
        for linea in f:
            p = json.loads(linea)
            with open(os.path.join(SALIDA, f"{p['id']}.svg"), "w", encoding="utf-8") as out:
                out.write(svg(p))
            n += 1
    print(f"{n} avatares -> {SALIDA}")
