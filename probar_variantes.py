# -*- coding: utf-8 -*-
"""Compara variantes de la publicación sobre el millón de perfiles. Gratis, sin API.
Los efectos de cada elemento están en variantes/supuestos.json: son supuestos, no datos medidos.
Uso: python probar_variantes.py  ->  resultados_1m/variantes.md
"""
import json, os
from calificar import puntaje

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(HERE, "datos_1m", "personas_1m.jsonl")
VARIANTES = os.path.join(HERE, "variantes", "variantes.json")
SUPUESTOS = os.path.join(HERE, "variantes", "supuestos.json")
SALIDA = os.path.join(HERE, "resultados_1m", "variantes.md")

def efecto(v, p, sup):
    d = 0.0
    if v["imagen_real"]:
        d += sup["imagen_real"]
    if v["cta_contacto"]:
        d += sup["cta_contacto"]
    if v["contexto_incluyente"] and p["estrato"] <= 3:
        d += sup["contexto_incluyente_estratos_1_3"]
    return d

def resumir(s_lista):
    n = len(s_lista)
    cal = [min(5, max(1, round(1 + s * 8))) for s in s_lista]
    llama = sum(1 for s in s_lista if s >= 0.42)
    no_llega = sum(1 for s in s_lista if s < 0.25)
    return sum(cal) / n, 100 * llama / n, 100 * no_llega / n

def main():
    with open(VARIANTES, encoding="utf-8") as f:
        variantes = json.load(f)
    with open(SUPUESTOS, encoding="utf-8") as f:
        sup = {k: v for k, v in json.load(f).items() if not k.startswith("_")}

    cols = {v["id"]: {"s": [], "estr": {}} for v in variantes}
    with open(ENTRADA, encoding="utf-8") as f:
        for linea in f:
            p = json.loads(linea)
            base = puntaje(p)
            for v in variantes:
                s = base + efecto(v, p, sup)
                cols[v["id"]]["s"].append(s)
                e = cols[v["id"]]["estr"].setdefault(p["estrato"], [0, 0])
                e[0] += 1
                e[1] += s >= 0.25

    L = ["# Variantes de la publicación (SIMULACIÓN, 1.000.000 perfiles)", "",
         "Los efectos de cada elemento son supuestos definidos en `variantes/supuestos.json`, no datos medidos.", "",
         "| Variante | Descripción | Prom. calificación | Le llama la atención | No le llega | Alcance estratos 1-3 | Alcance estratos 4-6 |",
         "|---|---|---|---|---|---|---|"]
    for v in variantes:
        s_lista = cols[v["id"]]["s"]
        prom, llama, no_llega = resumir(s_lista)
        est = cols[v["id"]]["estr"]
        bajo = 100 * sum(est[e][1] for e in (1, 2, 3)) / sum(est[e][0] for e in (1, 2, 3))
        alto = 100 * sum(est[e][1] for e in (4, 5, 6)) / sum(est[e][0] for e in (4, 5, 6))
        L.append(f"| {v['id']} | {v['descripcion']} | {prom:.2f} | {llama:.1f}% | {no_llega:.1f}% | {bajo:.1f}% | {alto:.1f}% |")
    L += ["", "Alcance = personas a las que no les es indiferente la publicación ni le llega (postura distinta de 'no le llega').", "",
          "Elementos sin supuesto (color y titular) quedan en 0: el modelo no puede compararlos todavía."]
    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    main()
