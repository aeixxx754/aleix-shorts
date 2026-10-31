# Playbook diario – Shorts de Aleix

Canal de YouTube de datos curiosos **para todas las edades**, en **español e inglés**.
Ritmo: **un Short por hora de 10:00 a 21:00, alternando idioma → 12 Shorts al día.**
**6 temas al día**; cada tema sale en **español a una hora par y en inglés a la hora siguiente**:
tema 1 → ES 10:00 / EN 11:00, tema 2 → ES 12:00 / EN 13:00, … tema 6 → ES 20:00 / EN 21:00.
(Motivo: límite diario de subidas de YouTube en un canal nuevo.) Una sola ejecución por la mañana lo crea y programa todo.

## 1. Preparar
- Repo: `aeixxx754/aleix-shorts`. Rama `main` = código, contenido e historial. Rama `media` = solo los vídeos del día.
- Clonar `main` con `git clone --depth 1`.
- Leer `historial.md` y los nombres de `content/` para no repetir temas ni datos.

## 2. Elegir 6 temas y sus datos
- Un tema distinto por hora. Temas posibles (y cualquier otro apto): animales, espacio, cuerpo humano, océano,
  dinosaurios, insectos, plantas, inventos, comida, geografía, clima, récords del mundo, aves, deportes (datos generales,
  sin ligas ni marcas), música e instrumentos, colores y luz, volcanes, el tiempo y los relojes, mascotas, reptiles,
  la Antigüedad (Egipto, Roma), transportes, matemáticas divertidas, idiomas.
  Se pueden repetir categorías amplias de otros días, pero **nunca los mismos datos** (comprobar historial y content/).
- 3 datos por tema, **comprobados** con WebSearch en fuentes fiables (enciclopedias, museos, universidades, agencias científicas).
  Ante cualquier duda, descartar el dato. Preferir datos muy conocidos y verificables a datos dudosos pero llamativos.
- Aptos para niños: nada violento, aterrador, sexual ni político. Sin marcas, personajes con derechos ni personas reales.
- Un emoji por dato que exista en Noto Color Emoji.

## 3. Escribir el contenido
Un archivo por tema: `content/AAAA-MM-DD_HH_tema.json` (HH = hora del Short en español: 10, 12, 14, 16, 18 o 20), con el formato de
`content/2026-10-31_13_cuerpo.json`:
- `hook`: [título en MAYÚSCULAS, ≤ 22 caracteres], [subtítulo corto]; `hook_emoji`; `cat` (categoría de YouTube)
- `facts`: 3 × [emoji, frase inicial ≤ 24 car., REMATE EN MAYÚSCULAS ≤ 18 car., cierre ≤ 40 car.]
- `outro`: [pregunta o frase final], ["Suscríbete para más datos" / "Subscribe for more facts"]
- `titulo` (≤ 60 car., con emoji), `descripcion` (1 frase + hashtags con #Shorts), `tags` (4-6).
- La versión EN es una traducción natural, no literal.

## 4. Crear los 12 vídeos
Para cada JSON y cada idioma (salida fuera del repo, p. ej. en una carpeta `media/` temporal):
```
python3 tools/make_short.py content/<archivo>.json es <carpeta_trabajo> <media>/<archivo>_es.mp4
python3 tools/make_short.py content/<archivo>.json en <carpeta_trabajo> <media>/<archivo>_en.mp4
```
Tarda ~25 s por vídeo. Revisión: hoja de contactos con fotogramas en 2, 6.5, 13.5, 20.5 y 26 s de todos los vídeos
(miniaturas de 180 px) y mirarla. Si un texto se corta o se solapa, acortarlo y volver a renderizar ese vídeo.

## 5. Subir a GitHub
- Vídeos: crear un repo nuevo vacío con solo los mp4 del día y hacer **force push a la rama `media`**
  (`git init -b media`, add, commit, `git push -f https://github.com/aeixxx754/aleix-shorts media:media`).
  Así la rama solo guarda los vídeos del día y el repositorio no crece. Metricool copia el vídeo a sus servidores
  al programarlo, así que no hace falta conservarlo.
- URL pública: `https://raw.githubusercontent.com/aeixxx754/aleix-shorts/media/<archivo>_<es|en>.mp4`
- Contenido: commit de los JSON de `content/` en `main` y push. **No** subir vídeos a `main`.

## 6. Programar en Metricool
- blogId `7763971`, zona horaria `Europe/Madrid`.
- Antes, `getScheduledPosts` del día (ignorar los borradores): si una hora ya tiene un Short de YouTube, no programar otro en esa hora
  (ese tema sale solo en el otro idioma).
- Cada tema: ES a la hora HH:00 de su archivo y EN a la hora HH+1:00.
- `providers: [{"network":"youtube"}]`, `autoPublish: true`, `draft: false`, `media: [URL raw]`,
  `text`: descripción, `youtubeData`: `{title, type:"short", privacy:"public", tags, category: cat, madeForKids:true, isAiGeneratedContent:false}`.
  Categoría: PETS_ANIMALS para animales; EDUCATION o SCIENCE_TECHNOLOGY para el resto.
- Programar primero uno y comprobar que Metricool acepta la URL; después el resto.

## 7. Cerrar
- Añadir a `historial.md` una línea por tema: fecha | hora | tema | los 3 datos. Commit y push a `main`.
- Avisar a Aleix con un resumen corto: los 6 temas con sus horas y cuántos Shorts se han programado.
- Si algo falla: no programar a medias los temas afectados; programar los que estén bien y explicar qué falló.
  Si Metricool rechaza por límite de publicaciones del plan, parar y avisar. Si en Metricool aparecen publicaciones de días
  anteriores fallidas por límite de subidas de YouTube, mencionarlo en el aviso.
