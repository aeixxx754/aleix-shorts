# Playbook diario – Shorts de Aleix

Canal de YouTube de datos curiosos **para todas las edades**, **solo en español** (desde el 5/11/2026 no se hace inglés:
mezclar idiomas en un canal confunde a YouTube y a quien se suscribe; el ES tenía ~105 visitas de media y el EN ~13).
Ritmo: **3 Shorts al día, en español, pocos y muy cuidados**, cada uno de un tema distinto:
- **11:00 · serie «Animales increíbles»** (`formato: "datos"` + `"serie": "Animales increíbles"` + `episodio`): un animal
  por episodio y sus 3 datos más sorprendentes (los animales y dinosaurios son lo que más se ve).
- **14:00 · serie «¿Verdadero o falso?»** (`formato: "vof"`): 3 mitos o verdades de un tema.
- **19:00 · «3 datos curiosos»** (`formato: "datos"`): ciencia cotidiana, cuerpo, espacio, inventos, preguntas con sorpresa
  («¿por qué una hora tiene 60 minutos?»).
Las dos series dan a la gente un motivo para suscribirse (ver el siguiente episodio).
Motivo del ritmo: YouTube penaliza el contenido «no auténtico» (plantillas casi idénticas subidas en volumen). Menos vídeos,
más variados y muy cuidados. Una sola ejecución por la mañana lo crea y programa todo.

**Claves para ganar suscriptores** (de los datos del canal: la gente se iba a los 5 s de 21 s):
- **Cortos**: 15,2 s («datos») y 16,4 s («vof»), para que se vean enteros y se repitan en bucle.
- **Gancho en el primer segundo**: el primer fotograma ya muestra el gancho completo; tiene que picar al instante
  (un número increíble, un reto o una pregunta sobre TI). Nada de introducciones.
- **Pedir algo facilísimo al final**: «Comenta SÍ si lo sabías», «¿Cuántas acertaste?», nunca preguntas largas.

## 1. Preparar
- Repo: `aeixxx754/aleix-shorts`. Rama `main` = código, contenido e historial. Rama `media` = solo los vídeos del día.
- Clonar `main` con `git clone --depth 1`.
- Leer `historial.md` y los nombres de `content/` para no repetir temas ni datos.
- **Oficina de agentes** (artifact `https://claude.ai/artifact/3yJt3qS1zdcoaj58Q4N9Ev`, base de datos con la herramienta
  ArtifactData; cargarla con ToolSearch si no está): poner al agente `aleix` en estado `ocupado` (leer el documento y
  `update` con su `version` como if_version) y leer el plan de hoy, `planes/<AAAA-MM-DD de hoy>`. Lo deja el turno de noche
  del equipo (Lucía, Bruno, Emma, Marco, Nora e Irene). Si la oficina no responde, seguir sin ella. Si el plan trae campos en
  inglés (`_en`), ignorarlos.

## 1b. Aprender de los días anteriores (mejora diaria)
- Pedir a Metricool (`getAnalyticsDataByMetrics`, brandId 7763971) los Shorts publicados en los **últimos 7 días** con:
  `YTVP02` fecha y hora, `YTVP17` título, `YTVP06` reproducciones, `YTVP08` duración media vista (s),
  `YTVP09` likes, `YTVP11` comentarios, `YTVP12` compartidos. (Los datos llegan con 1-2 días de retraso.)
- Calcular la **retención** = duración media vista / duración del vídeo (desde el 5/11: 15,2 s «datos» y «Animales
  increíbles», 16,4 s «vof»; del 3/11 al 4/11: 21,5 s y 22,4 s; antes: 21 s, 21,5 s y 28 s). Los Shorts en inglés antiguos
  se ignoran.
- Comparar por **formato** (Animales increíbles, vof, datos), tema, hora y **estilo de gancho** (campo `estilo_gancho` del JSON, ver paso 3):
  ¿qué tiene más reproducciones y más retención? ¿qué va peor?
- Escribir en `aprendizajes.md` (al principio, con la fecha) 3-5 conclusiones cortas y **qué se cambia hoy** por ellas.
  Si aún no hay datos suficientes (< 10 Shorts con reproducciones), decirlo y no sacar conclusiones.
- **Aplicarlo hoy**: repetir categorías y estilos de gancho que funcionan, abandonar los que fallan varias veces,
  y probar siempre al menos 1 idea nueva al día (tema, gancho o horario) para seguir aprendiendo.

## 1c. Tendencias del día
- Buscar con WebSearch qué es tendencia **hoy** en España y Latinoamérica, sobre todo temas aptos para todas las edades:
  fechas especiales (Halloween, Navidad, Día de la Tierra, eclipses, lanzamientos espaciales, Mundial, Juegos Olímpicos…),
  noticias científicas o de animales, retos virales sin riesgo. Ejemplos de búsqueda: "trending today", "efemérides hoy",
  "YouTube Shorts trending hashtags", "tendencias hoy España".
- Si hay una tendencia apta, dedicarle **uno de los 3 temas** (con datos igual de verificados).
- Anotar en `aprendizajes.md` las tendencias usadas, para comparar luego si rindieron más.

## 2. Elegir los 3 temas y sus datos
- **Si hay plan de la oficina para hoy, es el punto de partida**: sus 3 temas, horas, ganchos (`gancho`) y datos.
  (Si el plan aún trae solo 2 temas, añadir tú el de «Animales increíbles».)
  Volver a comprobar cada dato con WebSearch igualmente; cambiar el que no se confirme, el que repita historial o el que
  choque con las conclusiones de hoy (paso 1b). Si el plan trae los campos de Marco (`titulo`, `descripcion`, `tags`),
  usarlos en el JSON (paso 3) y en Metricool, comprobando que cumplen las reglas del
  paso 3 (longitudes, 3-5 hashtags, tendencias solo si tienen relación real). Si un tema trae `prueba_titulo`, copiarlo
  tal cual en su JSON para que Pau pueda comparar las variantes. La locución de Nora (`voz`) va en
  `es.voz` del JSON (ver paso 3). El plan viene revisado por Irene (campo `revision`):
  si un tema trae `revisar`, cambiar ese dato o afirmación por otro verificado antes de escribir el JSON.
  Sin plan, elegir como siempre:
- «Animales increíbles»: **un solo animal** por episodio (pulpo, ajolote, colibrí, tardígrado, oso polar, T. rex…), nunca
  repetido (comprobar `content/`), con sus 3 datos más sorprendentes. Mamíferos, aves, insectos, peces, dinosaurios…: variar.
- Los otros dos (vof y datos) de categorías distintas entre sí y distintas de animales. Temas posibles (y cualquier otro apto): animales, espacio, cuerpo humano, océano,
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
Un archivo por tema: `content/AAAA-MM-DD_HH_tema.json` (HH = hora del Short: 11, 14 o 19). **Solo la clave `es`**
(no escribir `en`, `primer_comentario_en` ni nada en inglés).
- «Animales increíbles» con el formato de `tools/ejemplo_animales.json`: `"formato": "datos"`, `"serie": "Animales increíbles"`,
  `"episodio"`: nº (el número de JSON con `"serie": "Animales increíbles"` que ya hay en `content/` + 1). El vídeo pone la
  etiqueta «ANIMALES INCREÍBLES · #N» y el botón «SUSCRÍBETE para el próximo episodio». Título:
  "Animales increíbles #N: <animal> <emoji>".
- «3 datos» (`"formato": "datos"`) con el formato de `content/2026-11-04_20_inventos.json` (sin `en`).
- Tema A (`"formato": "vof"`) con el formato de `tools/ejemplo_vof.json`: `"episodio"`: nº de episodio (el número de JSON
  con `"formato": "vof"` que ya hay en `content/` + 1); `hook`: [título ≤ 34 car. en MAYÚSCULAS, p. ej. "3 MITOS DEL
  ESPACIO", subtítulo "¿cuántos aciertas?"]; `facts`: 3 × [emoji, afirmación ≤ 60 car., true/false, explicación ≤ 50 car.];
  `outro`: ["¿Cuántas acertaste?", "Comenta cuántas"]. El vídeo pone solo el nombre de la serie, el nº de episodio,
  los botones VERDADERO/FALSO, la cuenta atrás 3-2-1 y la revelación.
Campos comunes:
- `hook`: [**PREGUNTA gancho en MAYÚSCULAS, ≤ 34 caracteres**, que cree curiosidad y se entienda en 1 segundo
  (p. ej. "¿TIENES MÁS HUESOS QUE TU MADRE?", "¿SABES QUÉ ANIMAL TIENE 3 CORAZONES?")], [subtítulo corto, p. ej.
  "la respuesta te sorprenderá"]; `hook_emoji`; `cat` (categoría de YouTube)
- **Sin emojis dentro de los textos en pantalla** (la fuente no los tiene); los emojis van solo en `hook_emoji` y en los facts.
- `facts`: 3 × [emoji, frase inicial ≤ 24 car., REMATE EN MAYÚSCULAS ≤ 18 car., cierre ≤ 40 car.]
- `outro`: ["¿Cuál no sabías?" o pregunta parecida], [petición **facilísima** de comentar, ≤ 24 car., sin emojis:
  "Comenta SÍ si lo sabías", "Comenta tu favorito", "Comenta 1, 2 o 3"] (el final se funde con el inicio para que el
  Short se repita en bucle). El script añade solo un botón rojo de
  suscripción bajo el outro («datos nuevos cada día» o «para el próximo episodio»): no hace falta escribirlo.
- `voz` (dentro de `es`): la **locución** que dice la voz de ElevenLabs. La escribe Nora en el plan.
  Cada frase tiene que caber en su tramo (el script avisa si no): cuenta las palabras.
  - «datos» y «Animales increíbles»: [gancho ≤ 4 palabras, dato 1 ≤ 10, dato 2 ≤ 10, dato 3 ≤ 10, final ≤ 4].
  - «vof»: [gancho ≤ 4, [afirmación ≤ 6, revelación], [afirmación, revelación], [afirmación, revelación], final ≤ 4], donde la
    revelación es "¡Falso!" / "¡Verdadero!" + como mucho 3 palabras ("¡Falso! Sí ven.").
  Tono cercano y con energía; frases cortas; el REMATE o la cifra se dicen tal cual salen en pantalla. Si falta `voz`,
  se lee la pantalla (en la serie, solo el veredicto en la revelación).
- `primer_comentario`: comentario que se publica con el vídeo, ≤ 150 caracteres. Lo más fácil posible de contestar: con
  un emoji, un número o SÍ/NO (p. ej. "Comenta 🐙 si sabías lo de los 3 corazones", "¿Cuántas acertaste? 0, 1, 2 o 3 👇").
  Nada de pedir likes. Así hay conversación desde el primer minuto.
- `estilo_gancho`: etiqueta del tipo de gancho usado, para medir qué funciona: `pregunta-tu` ("¿Sabías que TÚ…?"),
  `reto` ("Seguro que no sabías…"), `comparacion` ("Más grande que…"), `numero` ("100.000 veces al día"),
  `misterio` ("Nadie sabe por qué…"). Usar estilos distintos en los temas de días seguidos.
- `titulo` (≤ 60 car., con emoji; en las series empieza por "¿Verdadero o falso? #N" o "Animales increíbles #N"),
  `descripcion` (1 frase + "Suscríbete para datos nuevos cada día", o en las series
  "Suscríbete para no perderte el próximo episodio" + hashtags), `tags` (4-6).
- **Hashtags** (en la descripción, en el idioma del vídeo), **entre 3 y 5 en total**:
  `#Shorts` + 1-2 del tema (p. ej. #dinosaurios) + 1-2 **en tendencia** solo si tienen relación real con el vídeo
  (p. ej. #Halloween en un vídeo de murciélagos el 31 de octubre). **Nunca** hashtags de tendencia sin relación con el contenido:
  YouTube los considera engañosos y puede quitar el vídeo. Nunca más de 15 hashtags (YouTube los ignora todos).

## 4. Crear los 3 vídeos
Primero comprobar la voz: `python3 tools/voz.py --check`. Debe decir `voz: OK · ElevenLabs · …`. La clave **no** se escribe en
ningún sitio: está guardada como secreto de red del entorno (host `api.elevenlabs.io`, cabecera `xi-api-key`) y se añade sola.
Si dice `voz: NO (motivo)`, **no parar**: los vídeos salen solo con música y se avisa del motivo en el mensaje final.

Dependencias: si `import numpy, PIL` falla (o PIL da error al importar), `python3 -m pip install --break-system-packages --force-reinstall numpy pillow`. La fuente Poppins va en `tools/fonts/`.
Para cada JSON (salida fuera del repo, p. ej. en una carpeta `media/` temporal):
```
python3 tools/make_short.py content/<archivo>.json es <carpeta_trabajo> <media>/<archivo>_es.mp4
```
El script escribe `voz: sí · …` o `voz: NO (motivo)`, y `voz: AVISO frase N…` si una frase no cabe: en ese caso acortar esa
frase de `voz` y volver a renderizar ese vídeo (las frases que no cambian salen de la caché y no gastan créditos).
Los vídeos duran 15,2 s («datos» y «Animales increíbles») o 16,4 s («vof»). Tarda ~15 s por vídeo. Revisión: hoja de
contactos con fotogramas en 0, 0.8, 3.6, 7.6, 11.6 y 14.7 s («datos») o en 0, 2.2, 3.9, 8.3 y 15.9 s («vof»: portada,
cuenta atrás, revelación, outro) de todos los vídeos
(miniaturas de 180 px) y mirarla. Si un texto se corta o se solapa, acortarlo y volver a renderizar ese vídeo.

## 5. Subir a GitHub
- Vídeos: crear un repo nuevo vacío con solo los mp4 del día y hacer **force push a la rama `media`**
  (`git init -b media`, add, commit, `git push -f https://github.com/aeixxx754/aleix-shorts media:media`).
  Así la rama solo guarda los vídeos del día y el repositorio no crece. Metricool copia el vídeo a sus servidores
  al programarlo, así que no hace falta conservarlo.
- URL pública: `https://raw.githubusercontent.com/aeixxx754/aleix-shorts/media/<archivo>_es.mp4`
- Contenido: commit de los JSON de `content/` en `main` y push. **No** subir vídeos a `main`.

## 6. Programar en Metricool
- blogId `7763971`, zona horaria `Europe/Madrid`.
- Antes, `getScheduledPosts` del día (ignorar los borradores): si una hora ya tiene un Short de YouTube, no programar otro en esa hora.
- Animales increíbles 11:00 · ¿Verdadero o falso? 14:00 · 3 datos 19:00. Si la tarea termina tarde y una hora ya ha pasado,
  moverlo a la siguiente hora libre (como mínimo 45 min después de ahora) y no más tarde de las 22:00.
- **Solo YouTube** (no publicar en TikTok): `providers: [{"network":"youtube"}]`, `autoPublish: true`,
  `draft: false`, `media: [URL raw]`, `text`: descripción, `firstCommentText`: `primer_comentario`,
  `youtubeData`: `{title, type:"short", privacy:"public", tags, category: cat, madeForKids:false, isAiGeneratedContent:false}`.
  `madeForKids:false`: el canal es para todas las edades (público general), no está dirigido principalmente a niños.
  Categoría: PETS_ANIMALS para animales; EDUCATION o SCIENCE_TECHNOLOGY para el resto.
- Programar primero uno y comprobar que Metricool acepta la URL; después el resto.
  Si Metricool rechaza `firstCommentText` en YouTube, programar sin él y decirlo en el aviso final.

## 7. Cerrar
- Añadir a `historial.md` una línea por tema: fecha | hora | tema | los 3 datos. Commit y push a `main`.
- Avisar a Aleix con un resumen corto: los 3 temas con sus horas (y el nº de episodio de cada serie) y cuántos Shorts se han programado, y si llevan voz (y si no, por qué).
- Dejarlo también en la oficina: una entrada en `tablon` (doc_id `AAAAMMDD-HHMM-aleix`) con
  `{fecha: ms epoch, agenteId: "aleix", nombre: "Aleix", tipo: "publicado" (o "alerta" si algo falló), turno: "manana",
  titulo: "Shorts del <día>", texto: el mismo resumen}`; marcar el plan de hoy con `estado: "usado"` si se usó;
  y volver a poner al agente `aleix` en `disponible`.
- Si algo falla: no programar a medias los temas afectados; programar los que estén bien y explicar qué falló.
  Si Metricool rechaza por límite de publicaciones del plan, parar y avisar. Si en Metricool aparecen publicaciones de días
  anteriores fallidas por límite de subidas de YouTube, mencionarlo en el aviso.
