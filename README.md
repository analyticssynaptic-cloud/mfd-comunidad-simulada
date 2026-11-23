# Comunidad simulada MFD (SIMULACIÓN)

Todo el contenido de este repositorio es **sintético**. Los perfiles no son personas reales. Las opiniones y los debates se generan con plantillas y reglas (personalidad, estrato, acceso a redes y gustos), no con un modelo de lenguaje, así que el texto es repetitivo y no representa opiniones de consumidores reales.

## Contenido

- `generar_personas.py`: genera 10.000 perfiles con edad, ciudad, estrato, ingreso aproximado, ocupación, gustos, personalidad y escepticismo. Semilla fija, así que es reproducible.
- `personas.jsonl`: los 10.000 perfiles.
- `debatir.py`: opinión de cada perfil (`opiniones`) y debates en grupo (`debates`). Sin costo y sin API.
- `opiniones.jsonl`: postura y opinión de los 10.000 perfiles.
- `debates/`: 50 transcripciones de debates en grupos de 20 personas, 3 rondas cada una.

## Reproducir

```
python generar_personas.py
python debatir.py opiniones
python debatir.py debates
```

## Pregunta de la simulación

¿La publicidad de MFD Marketing & Eventos llegará a todas las personas, incluidas las de menores ingresos, o solo a quienes ya tienen dinero y acceso a redes?

## Cómo leerlo

Sirve para explorar hipótesis y ver qué argumentos aparecen según perfil. No sirve como medición de mercado: para eso hay que usar encuestas o datos reales.
