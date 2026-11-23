# -*- coding: utf-8 -*-
"""Califica la publicación con los 10.000 perfiles y calcula el índice de éxito. Gratis, sin API.
Uso: python calificar.py  ->  resultados/calificaciones.csv y resultados/resumen.md
"""
import csv, json, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PERSONAS = os.path.join(HERE, "personas.jsonl")
RESULTADOS = os.path.join(HERE, "resultados")

def puntaje(p):
    return ({"bajo": 0.1, "medio": 0.25, "alto": 0.4}[p["acceso_redes"]] + (p["estrato"] - 1) * 0.04
            + (0.1 if p["ve_publicidad_de_marcas_btl"] else 0) - p["escepticismo"] * 0.25)

def postura(p):
    s = puntaje(p)
    if s >= 0.42:
        return "le llama la atención"
    if s >= 0.25:
        return "le es indiferente"
    return "no le llega"

def calificacion(p):
    return min(5, max(1, round(1 + puntaje(p) * 8)))

def pct(n, d):
    return 100 * n / d if d else 0.0

def main():
    with open(PERSONAS, encoding="utf-8") as f:
        personas = [json.loads(l) for l in f]
    os.makedirs(RESULTADOS, exist_ok=True)
    filas = [{"id": p["id"], "estrato": p["estrato"], "ciudad": p["ciudad"], "personalidad": p["personalidad"],
              "acceso_redes": p["acceso_redes"], "calificacion": calificacion(p), "postura": postura(p)} for p in personas]
    with open(os.path.join(RESULTADOS, "calificaciones.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    n = len(filas)
    prom = sum(x["calificacion"] for x in filas) / n
    por_postura = defaultdict(int)
    for x in filas:
        por_postura[x["postura"]] += 1
    llama = pct(por_postura["le llama la atención"], n)
    indiferente = pct(por_postura["le es indiferente"], n)
    no_llega = pct(por_postura["no le llega"], n)

    por_estrato = defaultdict(lambda: [0, 0])
    for x in filas:
        por_estrato[x["estrato"]][0] += 1
        por_estrato[x["estrato"]][1] += x["postura"] != "no le llega"
    alcance = {e: pct(v[1], v[0]) for e, v in sorted(por_estrato.items())}
    popular = (por_estrato[1][1] + por_estrato[2][1]) / (por_estrato[1][0] + por_estrato[2][0]) * 100
    alto = (por_estrato[5][1] + por_estrato[6][1]) / (por_estrato[5][0] + por_estrato[6][0]) * 100
    brecha = alto - popular

    por_pers = defaultdict(list)
    for x in filas:
        por_pers[x["personalidad"]].append(x["calificacion"])

    indice = 100 * (0.4 * (prom - 1) / 4 + 0.4 * llama / 100 + 0.2 * max(0.0, 1 - max(0.0, brecha) / 100))
    if indice >= 70:
        veredicto = "Exitosa"
    elif indice >= 50:
        veredicto = "Mejorable"
    else:
        veredicto = "Débil"

    L = ["# Calificación de la publicación de Instagram (SIMULACIÓN)", "",
         f"Base: {n:,} perfiles sintéticos. Generado con reglas, no con IA.", "",
         "## Índice de éxito", "",
         f"**{indice:.0f} / 100 · {veredicto}**", "",
         "Fórmula: 40% calificación promedio (escala 1 a 5, normalizada) + 40% % que le llama la atención "
         "+ 20% equidad de alcance (penaliza si estratos 5-6 alcanzan mucho más que 1-2).", "",
         "| Métrica | Valor |", "|---|---|",
         f"| Calificación promedio | {prom:.2f} / 5 |",
         f"| Le llama la atención | {llama:.1f}% |",
         f"| Le es indiferente | {indiferente:.1f}% |",
         f"| No le llega | {no_llega:.1f}% |",
         f"| Alcance estratos 1-2 | {popular:.1f}% |",
         f"| Alcance estratos 5-6 | {alto:.1f}% |",
         f"| Brecha de alcance (5-6 menos 1-2) | {brecha:+.1f} puntos |", "",
         "## Alcance por estrato", "",
         "| Estrato | Personas | Alcanza (%) | Calificación promedio |", "|---|---|---|---|"]
    for e in sorted(por_estrato):
        cals = [x["calificacion"] for x in filas if x["estrato"] == e]
        L.append(f"| {e} | {por_estrato[e][0]:,} | {alcance[e]:.1f}% | {sum(cals) / len(cals):.2f} |")
    L += ["", "## Por personalidad", "", "| Personalidad | Calificación promedio |", "|---|---|"]
    for k in sorted(por_pers, key=lambda k: -sum(por_pers[k]) / len(por_pers[k])):
        L.append(f"| {k} | {sum(por_pers[k]) / len(por_pers[k]):.2f} |")
    L += ["", "Detalle por persona: `calificaciones.csv`. Las calificaciones son estimaciones simuladas, no mediciones reales."]
    with open(os.path.join(RESULTADOS, "resumen.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"indice={indice:.1f} {veredicto} prom={prom:.2f} llama={llama:.1f}% brecha={brecha:+.1f}")

if __name__ == "__main__":
    main()
