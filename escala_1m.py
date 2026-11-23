# -*- coding: utf-8 -*-
"""Genera 1.000.000 de perfiles sintéticos en local y los resume por grupo. Gratis, sin API.
Uso: python escala_1m.py  ->  datos_1m/personas_1m.jsonl (no se sube a GitHub)
                              resultados_1m/resumen_1m.md y resultados_1m/grupos_1m.csv (sí se suben)
Los primeros 10.000 perfiles son los mismos de personas.jsonl (misma semilla y mismo orden).
"""
import csv, json, os
from collections import Counter, defaultdict
from generar_personas import persona
from calificar import puntaje, calificacion, postura

HERE = os.path.dirname(os.path.abspath(__file__))
N = 1_000_000
DATOS = os.path.join(HERE, "datos_1m")
RES = os.path.join(HERE, "resultados_1m")

def main():
    os.makedirs(DATOS, exist_ok=True)
    os.makedirs(RES, exist_ok=True)
    grupos = Counter()
    por_postura = Counter()
    por_cal = Counter()
    suma_cal = 0
    alcanza = defaultdict(lambda: [0, 0])
    with open(os.path.join(DATOS, "personas_1m.jsonl"), "w", encoding="utf-8") as f:
        for i in range(1, N + 1):
            p = persona(i)
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
            cal = calificacion(p)
            pos = postura(p)
            grupos[(p["estrato"], p["ciudad"], p["acceso_redes"], cal, pos)] += 1
            por_postura[pos] += 1
            por_cal[cal] += 1
            suma_cal += cal
            alcanza[p["estrato"]][0] += 1
            alcanza[p["estrato"]][1] += pos != "no le llega"

    with open(os.path.join(RES, "grupos_1m.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["estrato", "ciudad", "acceso_redes", "calificacion", "postura", "personas"])
        for (e, c, a, cal, pos), n in sorted(grupos.items()):
            w.writerow([e, c, a, cal, pos, n])

    n = N
    prom = suma_cal / n
    llama = 100 * por_postura["le llama la atención"] / n
    popular = 100 * (alcanza[1][1] + alcanza[2][1]) / (alcanza[1][0] + alcanza[2][0])
    alto = 100 * (alcanza[5][1] + alcanza[6][1]) / (alcanza[5][0] + alcanza[6][0])
    brecha = alto - popular
    indice = 100 * (0.4 * (prom - 1) / 4 + 0.4 * llama / 100 + 0.2 * max(0.0, 1 - max(0.0, brecha) / 100))
    veredicto = "Exitosa" if indice >= 70 else "Mejorable" if indice >= 50 else "Débil"

    L = ["# Resumen a 1.000.000 de perfiles (SIMULACIÓN)", "",
         "Generado con reglas, no con IA. Los perfiles completos quedan en el PC (no se suben).", "",
         f"**Índice de éxito: {indice:.1f} / 100 · {veredicto}**", "",
         "| Métrica | Valor |", "|---|---|",
         f"| Perfiles | {n:,} |",
         f"| Calificación promedio | {prom:.2f} / 5 |",
         f"| Le llama la atención | {llama:.1f}% |",
         f"| Le es indiferente | {100 * por_postura['le es indiferente'] / n:.1f}% |",
         f"| No le llega | {100 * por_postura['no le llega'] / n:.1f}% |",
         f"| Alcance estratos 1-2 | {popular:.1f}% |",
         f"| Alcance estratos 5-6 | {alto:.1f}% |", "",
         "## Calificaciones", "", "| Calificación | Personas | % |", "|---|---|---|"]
    for c in sorted(por_cal):
        L.append(f"| {c} | {por_cal[c]:,} | {100 * por_cal[c] / n:.1f}% |")
    L += ["", "Detalle por grupo (estrato, ciudad, acceso, calificación): `grupos_1m.csv`."]
    with open(os.path.join(RES, "resumen_1m.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"indice={indice:.1f} {veredicto} prom={prom:.2f} llama={llama:.1f}% brecha={brecha:+.1f}")

if __name__ == "__main__":
    main()
