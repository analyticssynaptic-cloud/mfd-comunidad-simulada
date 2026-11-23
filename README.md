# Comunidad simulada MFD (SIMULACIÓN)

Todo el contenido de este repositorio es **sintético**. Los perfiles no son personas reales. Las opiniones y los debates se generan con plantillas y reglas (personalidad, estrato, acceso a redes y gustos), no con un modelo de lenguaje, así que el texto es repetitivo y no representa opiniones de consumidores reales.

## Contenido

- `generar_personas.py`: genera 10.000 perfiles con edad, ciudad, estrato, ingreso aproximado, ocupación, gustos, personalidad y escepticismo. Semilla fija, así que es reproducible.
- `personas.jsonl`: los 10.000 perfiles.
- `avatares.py` y `avatares/`: un muñequito SVG por persona.
- `debatir.py`: opinión de cada perfil (`opiniones.jsonl`) y debates en grupo (`debates/`).
- `calificar.py` y `resultados/`: calificación de la publicación (1 a 5) por cada persona, y el índice de éxito.
- `publicacion/`: publicación de Instagram (`post_instagram.png`, `caption.txt`), debate de la publicación en `debate_publicacion.md` (con avatares) y en HTML tipo chat (`debate_post.html`).
- `chat_publicacion.py`: genera el debate de la publicación y `personas.html` (listado buscable).
- `mapa_3d.py` y `mapa/`: mapa 3D con las 10.000 personas como muñequitos. Abrir `mapa/mapa_3d.html` en el navegador (necesita internet para cargar Three.js; `datos.js` debe quedar al lado). Clic en una figura para ver su perfil, opinión y el debate.

## Sistema de calificación

Cada perfil tiene un puntaje según acceso a redes, estrato, si ya ve publicidad de marcas BTL y su nivel de escepticismo. De ese puntaje salen:

- **Calificación** (1 a 5) y **postura**: le llama la atención, le es indiferente o no le llega.
- **Índice de éxito** (0 a 100) = 40% calificación promedio + 40% % que le llama la atención + 20% equidad de alcance (penaliza si los estratos 5-6 alcanzan mucho más que 1-2).
- Veredicto: 70 o más exitosa, 50 a 69 mejorable, menos de 50 débil.

Los pesos y los umbrales son decisiones de diseño, no datos reales. Las diferencias por estrato salen directamente de las reglas que se escribieron, así que sirven para comparar versiones de la publicación, no para medir el mercado.

## Reproducir

```
python generar_personas.py
python debatir.py opiniones
python debatir.py debates
python avatares.py
python calificar.py
python chat_publicacion.py
python publicacion/generar_post.py
python mapa_3d.py
```

## Pregunta de la simulación

¿La publicidad de MFD Marketing & Eventos llegará a todas las personas, incluidas las de menores ingresos, o solo a quienes ya tienen dinero y acceso a redes?

## Cómo leerlo

Sirve para explorar hipótesis y ver qué argumentos aparecen según perfil. No sirve como medición de mercado: para eso hay que usar encuestas o datos reales.
