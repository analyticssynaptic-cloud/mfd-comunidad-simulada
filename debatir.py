# -*- coding: utf-8 -*-
"""Opiniones y debates simulados con reglas (sin API ni modelos, gratis y reproducibles).
Uso:
  python debatir.py opiniones            -> opiniones.jsonl (10.000 perfiles)
  python debatir.py debates [--grupos 50] [--tam 20] [--rondas 3]  -> debates/debate_NNN.md
"""
import argparse, json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
PERSONAS = os.path.join(HERE, "personas.jsonl")
OPINIONES = os.path.join(HERE, "opiniones.jsonl")
DEBATES = os.path.join(HERE, "debates")
PREGUNTA = ("¿La publicidad de MFD Marketing & Eventos (activaciones BTL, sampling y eventos en Cali) "
            "llegará a todas las personas, incluidas las de menores ingresos, o solo a quienes ya tienen dinero y acceso a redes?")

SI, DEPENDE, NO = "llega a casi todos", "depende", "no llega a todos"

PERSONALIDAD = {
    "analítico": ("Según cómo se segmenta la pauta, lo que llega depende del presupuesto y del alcance.",
                  "Quiero ver cifras de alcance antes de creer que llega a alguien."),
    "emocional": ("Lo que me mueve es si la gente se siente vista.", "Un anuncio que no me toca no me dice nada."),
    "escéptico": ("Yo asumo que esto no es para mí.", "Desconfío de cualquier marca que dice que es para todos."),
    "optimista": ("Si la marca se acerca bien, cualquiera puede llegar a ser cliente.", "Creo que todo el mundo puede enterarse si se hace bien."),
    "práctico": ("A mí solo me importa si sirve esta semana.", "Si no me resuelve algo concreto, lo ignoro."),
    "crítico social": ("Esto deja por fuera a quien tiene menos dinero, y eso es un problema.", "La publicidad siempre le habla a quien ya puede comprar."),
    "curioso": ("Me interesa cómo llegan con sampling en la calle, porque eso sí toca a más gente.", "Quiero entender el mecanismo antes de juzgar."),
    "conservador": ("Confío más en la radio y en el boca a boca que en internet.", "Lo de siempre, la recomendación de alguien cercano, es lo que funciona."),
}

POR_ESTRATO = {
    "bajo": ["Con lo que gano, esa publicidad me queda muy lejos: lo que anuncian no me alcanza.",
             "Lo que veo son marcas para gente con plata, no para la cuadra."],
    "medio": ["Me llega algo por redes, pero los eventos de la ciudad casi nunca los veo.",
              "En mi barrio la publicidad llega más por el parlante del vendedor que por internet."],
    "alto": ["Me aparecen anuncios todo el día, pero siempre son los mismos públicos.",
             "La pauta se compra por segmento, y los segmentos populares casi nadie los compra."],
}

POR_ACCESO = {
    "bajo": "Con datos limitados ni abro esos anuncios.",
    "medio": "Veo anuncios en el celular, pero salto la mayoría.",
    "alto": "Estoy conectado todo el día, así que los anuncios sí me llegan.",
}

GUSTO_FRASE = "Por ejemplo, a mí que me gusta {g} sí me llegaría algo si lo acercan donde estoy."

def postura(p):
    e = p["estrato"]
    s = (e - 1) / 5 * 0.5 + {"bajo": 0.0, "medio": 0.15, "alto": 0.3}[p["acceso_redes"]] \
        + (0.2 if p["ve_publicidad_de_marcas_btl"] else 0.0) - p["escepticismo"] * 0.2
    if s >= 0.5:
        return SI
    if s < 0.3:
        return NO
    return DEPENDE

def razon(p, rnd):
    e = p["estrato"]
    estrato_txt = rnd.choice(POR_ESTRATO["bajo" if e <= 2 else "medio" if e == 3 else "alto"])
    partes = [PERSONALIDAD[p["personalidad"]][0], estrato_txt, POR_ACCESO[p["acceso_redes"]]]
    return " ".join(partes)

def opinion(p, rnd):
    pos = postura(p)
    cierre = PERSONALIDAD[p["personalidad"]][1]
    gusto = GUSTO_FRASE.format(g=rnd.choice(p["gustos"]))
    return f"{cierre} {razon(p, rnd)} {gusto}" if pos != SI else f"{razon(p, rnd)} {cierre} {gusto}", pos

def cargar_personas():
    with open(PERSONAS, encoding="utf-8") as f:
        return [json.loads(l) for l in f]

def generar_opiniones():
    rnd = random.Random(42)
    personas = cargar_personas()
    with open(OPINIONES, "w", encoding="utf-8") as f:
        for p in personas:
            texto, pos = opinion(p, rnd)
            f.write(json.dumps({"id": p["id"], "nombre": p["nombre"], "postura": pos, "opinion": texto}, ensure_ascii=False) + "\n")
    print(f"{len(personas)} opiniones -> {OPINIONES}")

def generar_debates(grupos, tam, rondas):
    personas = cargar_personas()
    rnd = random.Random(7)
    os.makedirs(DEBATES, exist_ok=True)
    for g in range(1, grupos + 1):
        grupo = rnd.sample(personas, tam)
        lineas = [f"# Debate {g:03d} (SIMULADO)", "", f"**Pregunta:** {PREGUNTA}", "",
                  "Participantes: " + "; ".join(f"{p['nombre']} ({p['id']}, {p['personalidad']}, estrato {p['estrato']})" for p in grupo),
                  ""]
        anterior = None
        for r in range(1, rondas + 1):
            lineas.append(f"## Ronda {r}")
            for p in grupo:
                pos = postura(p)
                if anterior is None:
                    texto = f"{razon(p, rnd)} Creo que {pos}."
                elif anterior[1] == pos:
                    texto = f"Coincido con {anterior[0]}. {razon(p, rnd)}"
                else:
                    texto = f"No estoy de acuerdo con {anterior[0]}: creo que {pos}. {razon(p, rnd)}"
                lineas.append(f"**{p['nombre']}** ({p['personalidad']}): {texto}")
                lineas.append("")
                anterior = (p["nombre"], pos)
        with open(os.path.join(DEBATES, f"debate_{g:03d}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
    print(f"{grupos} debates -> {DEBATES}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("modo", choices=["opiniones", "debates"])
    ap.add_argument("--grupos", type=int, default=50)
    ap.add_argument("--tam", type=int, default=20)
    ap.add_argument("--rondas", type=int, default=3)
    a = ap.parse_args()
    if a.modo == "opiniones":
        generar_opiniones()
    else:
        generar_debates(a.grupos, a.tam, a.rondas)
