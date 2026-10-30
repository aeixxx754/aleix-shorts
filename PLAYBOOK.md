# Playbook diario – Shorts de Aleix

Canal de YouTube de datos curiosos **para todas las edades**, en **español e inglés**.
Cada día: 1 tema nuevo → 2 Shorts (ES y EN) → programados en Metricool.

## 1. Preparar
- Repo: `aeixxx754/aleix-shorts` (rama `main`). Clonar con `git clone --depth 1`.
- Leer `historial.md` para no repetir temas ni datos.

## 2. Elegir tema y datos
- Temas rotativos (no repetir el de los últimos 7 días): animales, espacio, cuerpo humano, océano,
  dinosaurios, insectos, plantas, inventos, comida, geografía, clima, récords del mundo, aves, deportes (datos generales, sin ligas ni marcas).
- 3 datos **comprobados**: verificar cada uno con WebSearch en una fuente fiable (enciclopedia, museo, universidad, agencia científica).
  Si hay dudas sobre un dato, descartarlo y elegir otro.
- Aptos para niños: nada violento, aterrador, sexual ni político. Sin marcas, personajes con derechos ni personas reales.
- Un emoji por dato que exista en Noto Color Emoji y represente bien el dato.

## 3. Escribir el contenido
Crear `content/AAAA-MM-DD_tema.json` siguiendo el formato de `content/2026-10-30_animales.json`:
- `hook`: [título en MAYÚSCULAS, ≤ 22 caracteres], [subtítulo corto]
- `facts`: 3 × [emoji, frase inicial ≤ 24 car., REMATE EN MAYÚSCULAS ≤ 18 car., cierre ≤ 40 car.]
- `outro`: [pregunta o frase final], ["Suscríbete para más datos" / "Subscribe for more facts"]
- `titulo` (≤ 60 car., con emoji), `descripcion` (1 frase + hashtags con #Shorts), `tags` (4-6).
- La versión EN es una traducción natural, no literal.

## 4. Crear los vídeos
```
python3 tools/make_short.py content/AAAA-MM-DD_tema.json es <carpeta_temporal> videos/AAAA-MM-DD_tema_es.mp4
python3 tools/make_short.py content/AAAA-MM-DD_tema.json en <carpeta_temporal> videos/AAAA-MM-DD_tema_en.mp4
```
Revisar fotogramas en 2 s, 6.5 s, 13.5 s, 20.5 s y 26 s de cada vídeo (ffmpeg -ss … -frames:v 1).
Comprobar que ningún texto se corta ni se solapa; si pasa, acortar el texto y volver a renderizar.

## 5. Subir a GitHub
`git add`, commit y `git push origin main`. URL pública del vídeo:
`https://raw.githubusercontent.com/aeixxx754/aleix-shorts/main/videos/<archivo>.mp4`

## 6. Programar en Metricool
- blogId `7763971`, zona horaria `Europe/Madrid`.
- Antes, `getScheduledPosts` del día: si ya hay un Short de YouTube programado ese día en ese idioma, no duplicarlo.
- ES a las **16:00**, EN a las **18:00** del mismo día.
- `providers: [{"network":"youtube"}]`, `autoPublish: true`, `draft: false`, `media: [URL raw]`,
  `text`: descripción, `youtubeData`: `{title, type:"short", privacy:"public", tags, category, madeForKids:true, isAiGeneratedContent:false}`.
  Categoría: PETS_ANIMALS para animales; EDUCATION o SCIENCE_TECHNOLOGY para el resto.

## 7. Cerrar
- Añadir una línea a `historial.md`: fecha | tema | los 3 datos | enlaces de Metricool. Commit y push.
- Avisar a Aleix con un resumen corto: tema, títulos y horas de publicación.
- Si algo falla (render, push o Metricool), no publicar nada a medias: avisar del error.
