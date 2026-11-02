# Playbook diario – Shorts de Aleix

Canal de YouTube de datos curiosos **para todas las edades**, en **español e inglés**.
Ritmo: **4 Shorts al día, pocos y muy cuidados.** 2 temas, cada uno en español y en inglés:
- **Tema A · serie «¿Verdadero o falso?»** (`formato: "vof"`): ES **13:00** · EN **18:00** (mediodía en Nueva York).
- **Tema B · «3 datos curiosos»** (`formato: "datos"`): ES **20:00** · EN **23:00** (tarde en EE. UU.).
Motivo: YouTube penaliza el contenido «no auténtico» (plantillas casi idénticas subidas en volumen). Menos vídeos, más
variados y con una serie propia que da una razón para suscribirse. Una sola ejecución por la mañana lo crea y programa todo.

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
- Calcular la **retención** = duración media vista / duración del vídeo (21,5 s «datos», 22,4 s «vof»; los anteriores al 3/11: 21 s y 21,5 s; 28 s los más antiguos).
- Comparar por **formato** (vof frente a datos), tema, idioma, hora y **estilo de gancho** (campo `estilo_gancho` del JSON, ver paso 3):
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
- Si hay una tendencia apta, dedicarle **uno de los 2 temas** (con datos igual de verificados).
- Anotar en `aprendizajes.md` las tendencias usadas, para comparar luego si rindieron más.

## 2. Elegir los 2 temas y sus datos
- **Si hay plan de la oficina para hoy, es el punto de partida**: sus 2 temas, horas, ganchos (`gancho`, `gancho_en`) y datos.
  Volver a comprobar cada dato con WebSearch igualmente; cambiar el que no se confirme, el que repita historial o el que
  choque con las conclusiones de hoy (paso 1b). Si el plan trae los campos de Marco (`titulo`, `titulo_en`, `descripcion`,
  `descripcion_en`, `tags`, `tags_en`), usarlos en el JSON (paso 3) y en Metricool, comprobando que cumplen las reglas del
  paso 3 (longitudes, 3-5 hashtags, tendencias solo si tienen relación real). Si un tema trae `prueba_titulo`, copiarlo
  tal cual en su JSON para que Pau pueda comparar las variantes. El plan viene revisado por Irene (campo `revision`):
  si un tema trae `revisar`, cambiar ese dato o afirmación por otro verificado antes de escribir el JSON.
  Sin plan, elegir como siempre:
- Tema A (vof) y tema B (datos) de categorías distintas. Temas posibles (y cualquier otro apto): animales, espacio, cuerpo humano, océano,
  dinosaurios, insectos, plantas, inventos, comida, geografía, clima, récords del mundo, aves, deportes (datos generales,
  sin ligas ni marcas), música e instrumentos, colores y luz, volcanes, el tiempo y los relojes, mascotas, reptiles,
  la Antigüedad (Egipto, Roma), transportes, matemáticas divertidas, idiomas.
  Se pueden repetir categorías amplias de otros días, pero **nunca los mismos datos** (comprobar historial y content/).
- **Serie «¿Verdadero o falso?»**: 3 afirmaciones sobre un mismo tema, con **al menos una verdadera y una falsa**.
  Las falsas tienen que ser **mitos muy extendidos** que fuentes fiables desmienten («los murciélagos son ciegos», «la
  Gran Muralla se ve desde el espacio»); las verdaderas, datos que parecen mentira («la miel puede durar miles de años»).
  La gracia es que la gente falle: elegir afirmaciones en las que la mayoría se equivocaría.
- 3 datos o afirmaciones por tema, **comprobados** con WebSearch en fuentes fiables (enciclopedias, museos, universidades, agencias científicas).
  Ante cualquier duda, descartar el dato. Preferir datos muy conocidos y verificables a datos dudosos pero llamativos.
- Aptos para niños: nada violento, aterrador, sexual ni político. Sin marcas, personajes con derechos ni personas reales.
- Un emoji por dato que exista en Noto Color Emoji.

## 3. Escribir el contenido
Un archivo por tema: `content/AAAA-MM-DD_HH_tema.json` (HH = hora del Short en español: 13 o 20).
- Tema B (`"formato": "datos"`) con el formato de `content/2026-10-31_13_cuerpo.json`.
- Tema A (`"formato": "vof"`) con el formato de `tools/ejemplo_vof.json`: `"episodio"`: nº de episodio (el número de JSON
  con `"formato": "vof"` que ya hay en `content/` + 1); `hook`: [título ≤ 34 car. en MAYÚSCULAS, p. ej. "3 MITOS DEL
  ESPACIO", subtítulo "¿cuántos aciertas?"]; `facts`: 3 × [emoji, afirmación ≤ 60 car., true/false, explicación ≤ 50 car.];
  `outro`: ["¿Cuántas acertaste?", "Míralo otra vez"]. El vídeo pone solo el nombre de la serie, el nº de episodio,
  los botones VERDADERO/FALSO, la cuenta atrás 3-2-1 y la revelación.
Campos comunes:
- `hook`: [**PREGUNTA gancho en MAYÚSCULAS, ≤ 34 caracteres**, que cree curiosidad y se entienda en 1 segundo
  (p. ej. "¿TIENES MÁS HUESOS QUE TU MADRE?", "¿SABES QUÉ ANIMAL TIENE 3 CORAZONES?")], [subtítulo corto, p. ej.
  "la respuesta te sorprenderá"]; `hook_emoji`; `cat` (categoría de YouTube)
- **Sin emojis dentro de los textos en pantalla** (la fuente no los tiene); los emojis van solo en `hook_emoji` y en los facts.
- `facts`: 3 × [emoji, frase inicial ≤ 24 car., REMATE EN MAYÚSCULAS ≤ 18 car., cierre ≤ 40 car.]
- `outro`: ["¿Cuál no sabías?" o pregunta parecida, que invite a comentar], ["Míralo otra vez" / "Watch it again"]
  (el final se funde con el inicio para que el Short se repita en bucle). El script añade solo un botón rojo de
  suscripción bajo el outro («datos nuevos cada día» o «para el próximo episodio»): no hace falta escribirlo.
- `voz` (dentro de `es`) y la misma clave dentro de `en`: la **locución** que dice la voz de ElevenLabs. La escribe Nora en el plan.
  Cada frase tiene que caber en su tramo (el script avisa si no): cuenta las palabras.
  - «datos»: [gancho ≤ 6 palabras, dato 1 ≤ 13, dato 2 ≤ 13, dato 3 ≤ 13, final ≤ 6].
  - «vof»: [gancho ≤ 6, [afirmación ≤ 8, revelación], [afirmación, revelación], [afirmación, revelación], final ≤ 6], donde la
    revelación es "¡Falso!" / "¡Verdadero!" ("False!" / "True!") + como mucho 4 palabras ("¡Falso! Sí que ven.").
  Tono cercano y con energía; frases cortas; el REMATE o la cifra se dicen tal cual salen en pantalla. Si falta `voz`,
  se lee la pantalla (en la serie, solo el veredicto en la revelación).
- `primer_comentario` y `primer_comentario_en`: comentario que se publica con el vídeo, ≤ 150 caracteres. Una pregunta
  concreta sobre el tema que se pueda contestar en una palabra o un número (p. ej. "¿Cuántos huesos crees que tiene una
  jirafa en el cuello? 👇"), y nada de pedir likes. Así hay conversación desde el primer minuto.
- `estilo_gancho`: etiqueta del tipo de gancho usado, para medir qué funciona: `pregunta-tu` ("¿Sabías que TÚ…?"),
  `reto` ("Seguro que no sabías…"), `comparacion` ("Más grande que…"), `numero` ("100.000 veces al día"),
  `misterio` ("Nadie sabe por qué…"). Usar estilos distintos en los temas de días seguidos.
- `titulo` (≤ 60 car., con emoji; en la serie empieza por "¿Verdadero o falso? #N" / "True or False? #N"),
  `descripcion` (1 frase + "Suscríbete para datos nuevos cada día" / "Subscribe for new facts every day", o en la serie
  "Suscríbete para no perderte el próximo episodio" / "Subscribe so you don't miss the next episode" + hashtags), `tags` (4-6).
- **Hashtags** (en la descripción, en el idioma del vídeo), **entre 3 y 5 en total**:
  `#Shorts` + 1-2 del tema (p. ej. #dinosaurios / #dinosaurs) + 1-2 **en tendencia** solo si tienen relación real con el vídeo
  (p. ej. #Halloween en un vídeo de murciélagos el 31 de octubre). **Nunca** hashtags de tendencia sin relación con el contenido:
  YouTube los considera engañosos y puede quitar el vídeo. Nunca más de 15 hashtags (YouTube los ignora todos).
- La versión EN es una traducción natural, no literal.

## 4. Crear los 4 vídeos
Primero comprobar la voz: `python3 tools/voz.py --check`. Debe decir `voz: OK · ElevenLabs · …`. La clave **no** se escribe en
ningún sitio: está guardada como secreto de red del entorno (host `api.elevenlabs.io`, cabecera `xi-api-key`) y se añade sola.
Si dice `voz: NO (motivo)`, **no parar**: los vídeos salen solo con música y se avisa del motivo en el mensaje final.

Para cada JSON y cada idioma (salida fuera del repo, p. ej. en una carpeta `media/` temporal):
```
python3 tools/make_short.py content/<archivo>.json es <carpeta_trabajo> <media>/<archivo>_es.mp4
python3 tools/make_short.py content/<archivo>.json en <carpeta_trabajo> <media>/<archivo>_en.mp4
```
El script escribe `voz: sí · …` o `voz: NO (motivo)`, y `voz: AVISO frase N…` si una frase no cabe: en ese caso acortar esa
frase de `voz` y volver a renderizar ese vídeo (las frases que no cambian salen de la caché y no gastan créditos).
Los vídeos duran 21,5 s («datos») o 22,4 s («vof»). Tarda ~20 s por vídeo. Revisión: hoja de contactos con fotogramas en
1.4, 5.5, 11, 16.5 y 20.3 s («datos») o en 1.3, 4.6, 6.4, 12.2 y 21.6 s («vof»: portada, cuenta atrás, revelación, outro) de todos los vídeos
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
- Tema A (vof): ES 13:00 y EN 18:00. Tema B (datos): ES 20:00 y EN 23:00.
- **Solo YouTube** (no publicar en TikTok): `providers: [{"network":"youtube"}]`, `autoPublish: true`,
  `draft: false`, `media: [URL raw]`, `text`: descripción, `firstCommentText`: `primer_comentario` (o `_en`),
  `youtubeData`: `{title, type:"short", privacy:"public", tags, category: cat, madeForKids:false, isAiGeneratedContent:false}`.
  `madeForKids:false`: el canal es para todas las edades (público general), no está dirigido principalmente a niños.
  Categoría: PETS_ANIMALS para animales; EDUCATION o SCIENCE_TECHNOLOGY para el resto.
- Programar primero uno y comprobar que Metricool acepta la URL; después el resto.
  Si Metricool rechaza `firstCommentText` en YouTube, programar sin él y decirlo en el aviso final.

## 7. Cerrar
- Añadir a `historial.md` una línea por tema: fecha | hora | tema | los 3 datos. Commit y push a `main`.
- Avisar a Aleix con un resumen corto: los 2 temas con sus horas (y el nº de episodio de la serie) y cuántos Shorts se han programado, y si llevan voz (y si no, por qué).
- Dejarlo también en la oficina: una entrada en `tablon` (doc_id `AAAAMMDD-HHMM-aleix`) con
  `{fecha: ms epoch, agenteId: "aleix", nombre: "Aleix", tipo: "publicado" (o "alerta" si algo falló), turno: "manana",
  titulo: "Shorts del <día>", texto: el mismo resumen}`; marcar el plan de hoy con `estado: "usado"` si se usó;
  y volver a poner al agente `aleix` en `disponible`.
- Si algo falla: no programar a medias los temas afectados; programar los que estén bien y explicar qué falló.
  Si Metricool rechaza por límite de publicaciones del plan, parar y avisar. Si en Metricool aparecen publicaciones de días
  anteriores fallidas por límite de subidas de YouTube, mencionarlo en el aviso.
