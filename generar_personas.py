# -*- coding: utf-8 -*-
"""Genera N perfiles sintéticos (Colombia) con rasgos de personalidad y situación económica.
Uso: python generar_personas.py [N]  ->  personas.jsonl
"""
import json, random, sys, os

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
HERE = os.path.dirname(os.path.abspath(__file__))
rnd = random.Random(20261123)

NOMBRES_F = ["Laura", "Valentina", "Camila", "Yoana", "Sofía", "Daniela", "Mariana", "Paula", "Andrea", "Lina",
             "Carolina", "Juliana", "Natalia", "Gloria", "Marcela", "Ana", "Diana", "Luz", "Érika", "Patricia"]
NOMBRES_M = ["Santiago", "Andrés", "Esneyder", "Juan", "Carlos", "Mateo", "Jhon", "Luis", "Felipe", "Miguel",
             "Edwin", "Óscar", "Julián", "Ricardo", "Harold", "Wilson", "Diego", "Hernán", "Javier", "Yeison"]
APELLIDOS = ["Gómez", "Restrepo", "Vélez", "Ramírez", "Osorio", "Mosquera", "Valencia", "Perea", "Caicedo",
             "Hurtado", "Quintero", "Rentería", "Murillo", "Arboleda", "Londoño", "Cuesta", "Ospina", "Banguero"]

CIUDADES = [("Cali", 0.34), ("Bogotá", 0.22), ("Medellín", 0.14), ("Barranquilla", 0.10),
            ("Bucaramanga", 0.05), ("Pereira", 0.04), ("Otra ciudad", 0.11)]

# (estrato, ingreso mensual aprox. COP, peso, acceso a internet/redes)
ESTRATOS = [(1, 900_000, 0.12, "bajo"), (2, 1_300_000, 0.24, "medio"), (3, 2_000_000, 0.28, "medio"),
            (4, 3_500_000, 0.18, "alto"), (5, 6_000_000, 0.10, "alto"), (6, 12_000_000, 0.08, "alto")]

OCUPACIONES = {
    1: ["vendedor informal", "empleada doméstica", "mototaxista", "vendedor ambulante", "celador", "desempleado/a buscando trabajo"],
    2: ["auxiliar de bodega", "tendero", "estilista independiente", "cocinero/a", "conductor de app", "operario de fábrica"],
    3: ["técnico en mantenimiento", "vendedor de tienda", "enfermero/a auxiliar", "administrativo/a", "profesor de colegio público"],
    4: ["ingeniero/a junior", "community manager", "coordinador/a de compras", "contador/a", "agente de ventas corporativas"],
    5: ["gerente de marca", "abogado/a corporativo", "médico/a especialista", "director/a comercial", "emprendedor/a exitoso/a"],
    6: ["empresario/a", "gerente general", "inversionista", "director/a de agencia", "dueño/a de cadena de restaurantes"],
}
GUSTOS = ["fútbol", "reguetón", "salsa", "vallenato", "cine", "series", "videojuegos", "cocina", "gimnasio",
           "iglesia", "ferias y fiestas", "viajes", "motos", "lectura", "marcas de lujo", "ahorro", "política",
           "redes sociales", "mascotas", "religión", "tecnología", "bares", "familia", "emprendimiento"]

PERSONALIDADES = {
    "analítico": "pregunta por datos y cifras, desconfía de lo que no se puede medir",
    "emocional": "decide por lo que siente y por la gente que conoce",
    "escéptico": "asume que la publicidad es para otros y que las marcas no le hablan",
    "optimista": "cree que cualquier persona puede ser cliente si la marca se acerca bien",
    "práctico": "solo le importa si el anuncio le sirve para algo concreto esta semana",
    "crítico social": "piensa que la publicidad excluye a quien tiene menos dinero",
    "curioso": "le llama la atención lo nuevo y busca entender antes de juzgar",
    "conservador": "prefiere lo tradicional, confía en el boca a boca y en la radio",
}

def elegir(pares):
    items, pesos = zip(*pares)
    return rnd.choices(items, weights=pesos, k=1)[0]

def persona(i):
    genero = rnd.choice(["F", "M"])
    nombre = f"{rnd.choice(NOMBRES_F if genero == 'F' else NOMBRES_M)} {rnd.choice(APELLIDOS)}"
    eleccion = rnd.choices(ESTRATOS, weights=[x[2] for x in ESTRATOS], k=1)[0]
    estrato, ingreso, _, acceso = eleccion
    ocupacion = rnd.choice(OCUPACIONES[estrato])
    personalidad = rnd.choice(list(PERSONALIDADES))
    return {
        "id": f"SIM-{i:05d}",
        "nombre": nombre,
        "genero": genero,
        "edad": rnd.randint(18, 70),
        "ciudad": elegir(CIUDADES),
        "estrato": estrato,
        "ingreso_mensual_aprox_cop": ingreso + rnd.randint(-150_000, 150_000),
        "ocupacion": ocupacion,
        "acceso_redes": acceso,
        "gustos": rnd.sample(GUSTOS, k=rnd.randint(2, 4)),
        "personalidad": personalidad,
        "personalidad_descripcion": PERSONALIDADES[personalidad],
        "escepticismo": round(rnd.random(), 2),
        "ve_publicidad_de_marcas_btl": estrato >= 3 and rnd.random() < 0.6 or estrato < 3 and rnd.random() < 0.25,
    }

if __name__ == "__main__":
    out = os.path.join(HERE, "personas.jsonl")
    with open(out, "w", encoding="utf-8") as f:
        for i in range(1, N + 1):
            f.write(json.dumps(persona(i), ensure_ascii=False) + "\n")
    print(f"{N} personas -> {out}")
