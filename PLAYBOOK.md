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
- **Oficina de agentes** (artifact `https://claude.ai/artifact/3yJt3qS1zdcoaj58Q4N9Ev`, base de datos con la herramienta
  ArtifactData; cargarla con ToolSearch si no está): poner al agente `aleix` en estado `ocupado` (leer el documento y
  `update` con su `version` como if_version) y leer el plan de hoy, `planes/<AAAA-MM-DD de hoy>`. Lo deja el turno de noche
  del equipo (Lucía, Bruno, Emma y Pau). Si la oficina no responde, seguir sin ella.

## 1b. Aprender de los días anteriores (mejora diaria)
- Pedir a Metricool (`getAnalyticsDataByMetrics`, brandId 7763971) los Shorts publicados en los **últimos 7 días** con:
  `YTVP02` fecha y hora, `YTVP17` título, `YTVP06` reproducciones, `YTVP08` duración media vista (s),
  `YTVP09` likes, `YTVP11` comentarios, `YTVP12` compartidos. (Los datos llegan con 1-2 días de retraso.)
- Calcular la **retención** = duración media vista / 21 s (o 28 s para los vídeos antiguos).
- Comparar por tema, por idioma, por hora y por **estilo de gancho** (campo `estilo_gancho` del JSON, ver paso 3):
  ¿qué tiene más reproducciones y más retención? ¿qué va peor?
- Escribir en `aprendizajes.md` (al principio, con la fecha) 3-5 conclusiones cortas y **qué se cambia hoy** por ellas.
  Si aún no hay datos suficientes (< 10 Shorts con reproducciones), decirlo y no sacar conclusiones.
- **Aplicarlo hoy**: repetir categorías y estilos de gancho que funcionan, abandonar los que fallan varias veces,
  y probar siempre al menos 1 idea nueva al día (tema, gancho o horario) para seguir aprendiendo.

## 1c. Tendencias del día
- Buscar con WebSearch qué es tendencia **hoy** en España y en EE. UU./mundo, sobre todo temas aptos para todas las edades:
  fechas especiales (Halloween, Navidad, Día de la Tierra, eclipses, lanzamientos espaciales, Mundial, Juegos Olímpicos…),
  noticias científicas o de animales, retos virales sin riesgo. Ejemplos de búsqueda: "trending today", "efemérides hoy",
  "YouTube Shorts trending hashtags", "tendencias hoy España".
- Si hay una tendencia apta, dedicarle **1 o 2 de los 6 temas** (con datos igual de verificados).
- Anotar en `aprendizajes.md` las tendencias usadas, para comparar luego si rindieron más.

## 2. Elegir 6 temas y sus datos
- **Si hay plan de la oficina para hoy, es el punto de partida**: sus 6 temas, horas, ganchos (`gancho`, `gancho_en`) y datos.
  Volver a comprobar cada dato con WebSearch igualmente; cambiar el que no se confirme, el que repita historial o el que
  choque con las conclusiones de hoy (paso 1b). Si el plan trae los campos de Marco (`titulo`, `titulo_en`, `descripcion`,
  `descripcion_en`, `tags`, `tags_en`), usarlos en el JSON (paso 3) y en Metricool, comprobando que cumplen las reglas del
  paso 3 (longitudes, 3-5 hashtags, tendencias solo si tienen relación real). Si un tema trae `prueba_titulo`, copiarlo
  tal cual en su JSON para que Pau pueda comparar las variantes. Sin plan, elegir como siempre:
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
- `hook`: [**PREGUNTA gancho en MAYÚSCULAS, ≤ 34 caracteres**, que cree curiosidad y se entienda en 1 segundo
  (p. ej. "¿TIENES MÁS HUESOS QUE TU MADRE?", "¿SABES QUÉ ANIMAL TIENE 3 CORAZONES?")], [subtítulo corto, p. ej.
  "la respuesta te sorprenderá"]; `hook_emoji`; `cat` (categoría de YouTube)
- **Sin emojis dentro de los textos en pantalla** (la fuente no los tiene); los emojis van solo en `hook_emoji` y en los facts.
- `facts`: 3 × [emoji, frase inicial ≤ 24 car., REMATE EN MAYÚSCULAS ≤ 18 car., cierre ≤ 40 car.]
- `outro`: ["¿Cuál no sabías?" o pregunta parecida, que invite a comentar], ["Míralo otra vez" / "Watch it again"]
  (el final se funde con el inicio para que el Short se repita en bucle). El script añade solo un botón rojo
  "SUSCRÍBETE · 1 dato cada hora" / "SUBSCRIBE · 1 fact every hour" bajo el outro: no hace falta escribirlo.
- `primer_comentario` y `primer_comentario_en`: comentario que se publica con el vídeo, ≤ 150 caracteres. Una pregunta
  concreta sobre el tema que se pueda contestar en una palabra o un número (p. ej. "¿Cuántos huesos crees que tiene una
  jirafa en el cuello? 👇"), y nada de pedir likes. Así hay conversación desde el primer minuto.
- `estilo_gancho`: etiqueta del tipo de gancho usado, para medir qué funciona: `pregunta-tu` ("¿Sabías que TÚ…?"),
  `reto` ("Seguro que no sabías…"), `comparacion` ("Más grande que…"), `numero` ("100.000 veces al día"),
  `misterio` ("Nadie sabe por qué…"). Repartir estilos distintos entre los 6 temas del día.
- `titulo` (≤ 60 car., con emoji), `descripcion` (1 frase + "Suscríbete para un dato nuevo cada hora" / "Subscribe for a new fact every hour" + hashtags), `tags` (4-6).
- **Hashtags** (en la descripción, en el idioma del vídeo), **entre 3 y 5 en total**:
  `#Shorts` + 1-2 del tema (p. ej. #dinosaurios / #dinosaurs) + 1-2 **en tendencia** solo si tienen relación real con el vídeo
  (p. ej. #Halloween en un vídeo de murciélagos el 31 de octubre). **Nunca** hashtags de tendencia sin relación con el contenido:
  YouTube los considera engañosos y puede quitar el vídeo. Nunca más de 15 hashtags (YouTube los ignora todos).
- La versión EN es una traducción natural, no literal.

## 4. Crear los 12 vídeos
Para cada JSON y cada idioma (salida fuera del repo, p. ej. en una carpeta `media/` temporal):
```
python3 tools/make_short.py content/<archivo>.json es <carpeta_trabajo> <media>/<archivo>_es.mp4
python3 tools/make_short.py content/<archivo>.json en <carpeta_trabajo> <media>/<archivo>_en.mp4
```
Los vídeos duran 21 s. Tarda ~20 s por vídeo. Revisión: hoja de contactos con fotogramas en 1.2, 5, 10.5, 16 y 19.8 s de todos los vídeos
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
- **Solo YouTube** (no publicar en TikTok): `providers: [{"network":"youtube"}]`, `autoPublish: true`,
  `draft: false`, `media: [URL raw]`, `text`: descripción, `firstCommentText`: `primer_comentario` (o `_en`),
  `youtubeData`: `{title, type:"short", privacy:"public", tags, category: cat, madeForKids:false, isAiGeneratedContent:false}`.
  `madeForKids:false`: el canal es para todas las edades (público general), no está dirigido principalmente a niños.
  Categoría: PETS_ANIMALS para animales; EDUCATION o SCIENCE_TECHNOLOGY para el resto.
- Programar primero uno y comprobar que Metricool acepta la URL; después el resto.
  Si Metricool rechaza `firstCommentText` en YouTube, programar sin él y decirlo en el aviso final.

## 7. Cerrar
- Añadir a `historial.md` una línea por tema: fecha | hora | tema | los 3 datos. Commit y push a `main`.
- Avisar a Aleix con un resumen corto: los 6 temas con sus horas y cuántos Shorts se han programado.
- Dejarlo también en la oficina: una entrada en `tablon` (doc_id `AAAAMMDD-HHMM-aleix`) con
  `{fecha: ms epoch, agenteId: "aleix", nombre: "Aleix", tipo: "publicado" (o "alerta" si algo falló), turno: "manana",
  titulo: "Shorts del <día>", texto: el mismo resumen}`; marcar el plan de hoy con `estado: "usado"` si se usó;
  y volver a poner al agente `aleix` en `disponible`.
- Si algo falla: no programar a medias los temas afectados; programar los que estén bien y explicar qué falló.
  Si Metricool rechaza por límite de publicaciones del plan, parar y avisar. Si en Metricool aparecen publicaciones de días
  anteriores fallidas por límite de subidas de YouTube, mencionarlo en el aviso.
