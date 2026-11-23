# -*- coding: utf-8 -*-
"""Simula un debate de la comunidad sobre una publicación y lo muestra como chat en HTML (gratis, sin API).
Uso: python chat_publicacion.py [--participantes 25] [--rondas 3]
  -> publicacion/debate_post.html   (abrir con doble clic en el navegador)
  -> personas.html                  (listado buscable de los 10.000 perfiles)
"""
import argparse, html, json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "publicacion")
PERSONAS = os.path.join(HERE, "personas.jsonl")
OPINIONES = os.path.join(HERE, "opiniones.jsonl")

PREGUNTA = "¿Qué le parece esta publicación de MFD en Instagram? ¿Le llama la atención, le es indiferente o no le llega?"

REACCION = {
    "analítico": "Los números (15 años, 50+ clientes) suenan bien, pero no dicen cuánta gente vio la publicación ni cuántas personas se interesaron.",
    "emocional": "La frase 'de corazón' me suena bonita, pero quiero ver gente real en las fotos, no solo texto.",
    "escéptico": "'Hacemos marcas de corazón' lo dice cualquiera. Hay que demostrarlo.",
    "optimista": "Me gusta que hablen de Cali y de toda Colombia. Si lo hacen bien, puede llegar a mucha gente.",
    "práctico": "Bien, pero ¿cómo les escribo? Debería verse el WhatsApp o un botón para pedir cotización.",
    "crítico social": "¿Las activaciones llegan a barrios o solo a centros comerciales? La publicación no lo aclara.",
    "curioso": "¿Qué es eso de la metodología EPECAR? Me daría curiosidad entrar a la página a ver cómo trabajan.",
    "conservador": "Me gustaría ver un número de contacto o una dirección en la publicación. Eso genera confianza.",
}

ESTRATO_TXT = {
    "bajo": "Como no tengo presupuesto para eventos grandes, esto me llega poco.",
    "medio": "Lo veo en el celular, pero no sé si esto es para alguien de mi nivel.",
    "alto": "Me interesa si hay proyectos para empresas de mi ciudad.",
}

ACCESO_TXT = {
    "bajo": "Con datos limitados, casi no abro publicaciones de empresas.",
    "medio": "La veo si me aparece, pero no la busco.",
    "alto": "Me aparece seguido y la miro con calma.",
}

def cargar(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f]

def postura(p):
    s = {"bajo": 0.1, "medio": 0.25, "alto": 0.4}[p["acceso_redes"]] + (p["estrato"] - 1) * 0.04 \
        + (0.1 if p["ve_publicidad_de_marcas_btl"] else 0) - p["escepticismo"] * 0.25
    if s >= 0.42:
        return "le llama la atención", "good"
    if s >= 0.25:
        return "le es indiferente", "mid"
    return "no le llega", "bad"

def mensaje(p, previo, rnd):
    pos, _ = postura(p)
    gusto = rnd.choice(p["gustos"])
    base = f"{REACCION[p['personalidad']]} {ESTRATO_TXT['bajo' if p['estrato'] <= 2 else 'medio' if p['estrato'] == 3 else 'alto']} {ACCESO_TXT[p['acceso_redes']]}"
    if previo is None:
        return f"{base} Para mí, {pos}. (Me gusta {gusto}.)"
    otro, pos_otro = previo
    if pos_otro == pos:
        return f"Coincido con {otro}. {base}"
    return f"No estoy de acuerdo con {otro}: para mí {pos}. {base}"

def debate(personas, participantes, rondas, rnd):
    grupo = rnd.sample(personas, participantes)
    turnos, previo = [], None
    for r in range(1, rondas + 1):
        for p in grupo:
            _, clase = postura(p)
            texto = mensaje(p, previo, rnd)
            turnos.append({"ronda": r, "p": p, "texto": texto, "clase": clase})
            previo = (p["nombre"], postura(p)[0])
    return turnos

def render_chat(turnos, participantes, rondas):
    burbujas = []
    ronda_actual = None
    for t in turnos:
        if t["ronda"] != ronda_actual:
            ronda_actual = t["ronda"]
            burbujas.append(f'<div class="ronda">Ronda {ronda_actual}</div>')
        p = t["p"]
        lado = "der" if p["genero"] == "F" else "izq"
        iniciales = "".join(w[0] for w in p["nombre"].split()[:2])
        burbujas.append(
            f'<div class="fila {lado}"><div class="av">{html.escape(iniciales)}</div><div class="burb {t["clase"]}">'
            f'<div class="meta"><b>{html.escape(p["nombre"])}</b> · {p["edad"]} años · {html.escape(p["ciudad"])} · estrato {p["estrato"]} · '
            f'{html.escape(p["personalidad"])} · acceso {p["acceso_redes"]}</div>'
            f'<div>{html.escape(t["texto"])}</div></div></div>')
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Debate simulado - publicación MFD</title>
<style>
body{{font-family:Arial,sans-serif;background:#0e0a0c;color:#f5f0ee;margin:0;padding:24px}}
.wrap{{max-width:760px;margin:0 auto}}
h1{{font-size:20px;color:#dc2626;margin:0 0 6px}}
.sub{{color:#aaa;font-size:13px;margin-bottom:16px}}
.post{{display:flex;gap:16px;align-items:center;background:#1a1316;border:1px solid #3a1d20;border-radius:12px;padding:12px;margin-bottom:18px}}
.post img{{width:160px;height:160px;border-radius:8px}}
.post p{{margin:0;font-size:14px;color:#ddd;white-space:pre-line}}
.ronda{{text-align:center;color:#888;font-size:12px;margin:18px 0 8px;letter-spacing:1px}}
.fila{{display:flex;gap:8px;margin:8px 0;align-items:flex-end}}
.fila.der{{flex-direction:row-reverse}}
.av{{width:34px;height:34px;border-radius:50%;background:#dc2626;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:12px;flex-shrink:0}}
.burb{{max-width:78%;padding:10px 12px;border-radius:14px;font-size:14px;line-height:1.4}}
.izq .burb{{background:#241b1e;border-bottom-left-radius:4px}}
.der .burb{{background:#3b1316;border-bottom-right-radius:4px}}
.meta{{font-size:11px;color:#aaa;margin-bottom:4px}}
.burb.good{{box-shadow:inset 3px 0 0 #22c55e}}
.burb.mid{{box-shadow:inset 3px 0 0 #eab308}}
.burb.bad{{box-shadow:inset 3px 0 0 #ef4444}}
.nota{{font-size:12px;color:#888;margin-top:20px;border-top:1px solid #333;padding-top:10px}}
</style></head><body><div class="wrap">
<h1>Debate simulado: publicación de MFD en Instagram</h1>
<div class="sub">SIMULACIÓN · {participantes} personas · {rondas} rondas · generado con reglas (sin IA de pago)</div>
<div class="post"><img src="post_instagram.png" alt="Publicación MFD">
<p>{html.escape(open(os.path.join(PUB, "caption.txt"), encoding="utf-8").read().strip())}</p></div>
<p class="sub">Pregunta: {html.escape(PREGUNTA)}</p>
{''.join(burbujas)}
<div class="nota">Verde: le llama la atención · Amarillo: le es indiferente · Rojo: no le llega. Las personas son perfiles sintéticos; el texto sale de plantillas.</div>
</div></body></html>"""

def render_personas(personas, opiniones):
    op = {o["id"]: o for o in opiniones}
    filas = []
    for p in personas:
        o = op.get(p["id"], {})
        filas.append(
            "<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in [
                p["id"], p["nombre"], p["genero"], p["edad"], p["ciudad"], p["estrato"],
                f'{p["ingreso_mensual_aprox_cop"]:,}', p["ocupacion"], p["acceso_redes"],
                ", ".join(p["gustos"]), p["personalidad"], p["escepticismo"], o.get("postura", "")]) + "</tr>")
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Personas simuladas MFD</title>
<style>
body{{font-family:Arial,sans-serif;background:#0e0a0c;color:#f5f0ee;margin:0;padding:20px}}
input{{width:360px;padding:8px;margin-bottom:12px;background:#1a1316;color:#fff;border:1px solid #3a1d20;border-radius:6px}}
table{{border-collapse:collapse;width:100%;font-size:12px}}
th,td{{border-bottom:1px solid #2a1d20;padding:5px 7px;text-align:left;white-space:nowrap}}
th{{position:sticky;top:0;background:#1a1316;color:#dc2626}}
</style></head><body>
<h2 style="color:#dc2626;margin:0 0 8px">Personas simuladas (SIMULACIÓN)</h2>
<input id="q" placeholder="Buscar por nombre, ciudad, personalidad, ocupación..." oninput="filtrar()">
<div style="max-height:85vh;overflow:auto"><table id="t"><thead><tr>
<th>ID</th><th>Nombre</th><th>G</th><th>Edad</th><th>Ciudad</th><th>Estrato</th><th>Ingreso COP</th><th>Ocupación</th>
<th>Acceso</th><th>Gustos</th><th>Personalidad</th><th>Escepticismo</th><th>Postura</th></tr></thead>
<tbody>{''.join(filas)}</tbody></table></div>
<script>
function filtrar(){{const q=document.getElementById('q').value.toLowerCase();
for(const r of document.querySelectorAll('#t tbody tr')){{r.style.display=r.textContent.toLowerCase().includes(q)?'':'none';}}}}
</script></body></html>"""

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--participantes", type=int, default=25)
    ap.add_argument("--rondas", type=int, default=3)
    a = ap.parse_args()
    personas = cargar(PERSONAS)
    rnd = random.Random(2026)
    turnos = debate(personas, a.participantes, a.rondas, rnd)
    with open(os.path.join(PUB, "debate_post.html"), "w", encoding="utf-8") as f:
        f.write(render_chat(turnos, a.participantes, a.rondas))
    with open(os.path.join(HERE, "personas.html"), "w", encoding="utf-8") as f:
        f.write(render_personas(personas, cargar(OPINIONES)))
    print("ok: publicacion/debate_post.html y personas.html")
