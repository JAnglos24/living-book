# Capítulo 5 — Prompts de imagen

Especificación de las 13 fotografías del capítulo ("Materiales Digitales: APIs, Datos y Restricciones" / "Digital Materials: APIs, Data and Constraints"). Mismo criterio visual que los capítulos 2 al 4: fotografía editorial de estudio y documental, no ilustración ni 3D, sin texto ni logos visibles, sin rostros reconocibles (manos, objetos, entornos — no retratos frontales). Como en el capítulo 4, hay **dos formatos**: dos láminas panorámicas 16:9 que se leen a ancho completo y once retratos 4:5 para el resto de las secciones longform.

**Hilo conductor del capítulo:** un termo de acero de doble pared en color cobalto es el objeto-maestro. Aparece (o se insinúa) en casi todas las imágenes para que el lector lo reconozca como el "personaje" del capítulo. Los términos digitales (APIs, datos, pagos) se muestran siempre a través de objetos físicos: nunca pantallas con interfaces, nunca iconografía de nube o de IA.

## Dirección de arte (aplica a las 13)

- **Estilo:** fotografía editorial, luz natural suave o de estudio, profundidad de campo baja, tono desaturado y neutro (grises, blancos, acero cepillado) con **un único acento cobalto** (`#0057D9`). En este capítulo el acento casi siempre es el termo, o una pieza pequeña (etiqueta, muestra, contenedor).
- **Composición:** cerca del sujeto, encuadre de revista de negocios (*Monocle*, *The Economist 1843*). Espacio limpio alrededor del objeto; nada de bodegones recargados.
- **El termo:** cuerpo cilíndrico de acero con acabado cobalto mate, tapa roscada simple, **sin marca, sin logotipo, sin texto grabado**. Mismo modelo en todas las imágenes en las que aparezca.
- **Prohibido:** texto legible de cualquier tipo (incluye pantallas, etiquetas, tickets, plaquetas, marcas de graduación legibles), **logos y marcas reales** (terminales de pago, paqueterías, navegadores, teléfonos, líneas navieras), rostros mirando a cámara, manos con joyería o rasgos identificables, iconografía de IA o de nube (robots, redes brillantes, candados luminosos), mapas con nombres de calles.
- **Formato de archivo:** `.jpg`, sRGB, sin marca de agua.
- **Medidas:**
  - **Láminas (2):** relación **16:9**, mínimo **2400 × 1350 px**, entregable recomendado **3200 × 1800 px**.
  - **Retratos (11):** relación **4:5**, mínimo **1600 × 2000 px**, entregable recomendado **2400 × 3000 px**.
  - Peso optimizado < 400 KB en ambos casos.
- **Nomenclatura:** `chapter-05-<slug>.jpg` (mismo patrón que los capítulos anteriores). Los archivos se colocan junto al HTML; si falta alguno, el HTML muestra un recuadro con la proporción correcta y el layout no se mueve.
- **Foco (focal point):** en los retratos, el sujeto principal queda en el tercio central del encuadre, para que un recorte por `object-fit: cover` no lo pierda.

---

## 1. `chapter-05-cobalt-flask-table.jpg` — Lámina 5.1 (16:9)
**Sección:** "Antes del primer dibujo" / "Before the first drawing" · **Cubierta del capítulo (`cover_image`)**
**Medidas:** 16:9 · 3200×1800 px
**Prompt:**
> Editorial studio photograph of a single cobalt-blue double-wall steel vacuum flask with a closed screw lid, standing upright on a bare pale wooden table. Soft daylight from a window at the left, long gentle shadow to the right. No logo, no engraving, no printed text anywhere on the body or lid. Plain neutral wall behind, slightly out of focus. The flask is the only saturated object in the frame; everything else in desaturated grays and warm whites. The object sits in the left third of a wide 16:9 composition, leaving calm empty space to the right. Documentary product photography, calm and exact, no people, no props.

**Texto alternativo:** "A cobalt vacuum flask with a closed lid standing on a plain table in soft daylight."
**Pie:** "A cobalt double-wall flask on a bare table: the whole product at a glance, before anyone asks what it is made of."

## 2. `chapter-05-three-uses.jpg`
**Sección:** "El propósito dentro del objeto" / "The purpose inside the object"
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Editorial still life of three unbranded drinkware pieces standing in a row on a pale seamless surface, each clearly built for a different use: a slim cobalt-blue commuter flask with a closed lid, a taller wider flask with a textured grip next to a heavy work glove resting against it, and a short open-top desk tumbler in brushed steel. Same soft overhead studio light on all three, shallow depth of field, the cobalt flask in the center. No labels, no logos, no legible text, no faces. Muted grays with one cobalt accent. 4:5 portrait.

**Texto alternativo:** "Three unbranded drinkware pieces side by side: a slim commuter flask, a tall flask held in a gloved hand and an open desk tumbler."
**Pie:** "One need, three jobs: the commute, the job site and the desk."

## 3. `chapter-05-flask-components.jpg`
**Sección:** "Un material tiene dirección" / "A material has an address"
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Overhead documentary still life of a cobalt-blue steel flask disassembled and laid out in a tidy exploded arrangement on a pale gray surface: the outer vessel, the inner vessel, the screw lid and a black rubber gasket, each separated by a few centimeters like parts on a workbench. Soft top light, crisp edges, shallow depth of field on the gasket in the foreground. No logos, no text, no markings on any part. Cobalt as the single accent; the rest brushed steel, black rubber and pale gray. Editorial industrial photography, no hands, no faces, 4:5 portrait.

**Texto alternativo:** "A flask taken apart into vessel, lid and rubber gasket, laid out on a pale surface."
**Pie:** "The vessel can be made locally while the gasket travels."

## 4. `chapter-05-weld-seam.jpg`
**Sección:** "El proceso cambia el material" / "The process changes the material"
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Extreme close-up documentary macro photograph of the brushed stainless-steel base of a vacuum flask, showing a clean circular joined seam and fine machining lines in the metal, lit by raking side light that picks out the texture. A thin band of cobalt-blue coating visible at the edge of the frame as the only color. Shallow depth of field, the seam sharp across the middle third. No stamped text, no logo, no serial number, no hands. Editorial manufacturing photography, cool neutral tones, 4:5 portrait.

**Texto alternativo:** "Close-up of the brushed stainless-steel base of a flask showing a joined seam."
**Pie:** "Each stage inherits the condition the previous one left."

## 5. `chapter-05-cobalt-finish-samples.jpg`
**Sección:** "El color llega al mercado" / "Color meets the market"
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Studio still life of four small coated steel swatches in a vertical row on a neutral gray surface, each a slightly different shade of cobalt blue (one a touch greener, one a touch darker, one glossier, one matte), photographed under the same low raking light so the differences in sheen and tone are visible. Blank swatches, no labels, no numbers, no printed text. A single cobalt flask softly out of focus in the background. Shallow depth of field, calm color-matching-lab feel, no hands, no faces. 4:5 portrait.

**Texto alternativo:** "Four coated steel swatches in slightly different cobalt blues under the same raking light."
**Pie:** "One name for the color, four different batches."

## 6. `chapter-05-measuring-jug.jpg`
**Sección:** "La capacidad necesita un idioma" / "Capacity needs a language"
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Documentary still life of a clear glass measuring jug filled with water, standing beside an unbranded cobalt-blue flask with its lid off, on a clean kitchen counter in soft window light. The water line sits just under the rim of the flask's opening, suggesting the difference between brim capacity and usable capacity. The jug's graduation marks are present but blurred and illegible, no numbers or letters readable anywhere. Shallow depth of field, cool neutral palette with the flask as the cobalt accent. No hands, no faces, no logos. 4:5 portrait.

**Texto alternativo:** "A glass measuring jug with unreadable markings beside a flask, the water level close to the rim of the opening."
**Pie:** "Capacity measured to the brim is not capacity you can use."

## 7. `chapter-05-drinkware-shelf.jpg` — Lámina 5.2 (16:9)
**Sección:** "Del termo al marketplace" / "From vessel to marketplace"
**Medidas:** 16:9 · 3200×1800 px
**Prompt:**
> Wide editorial photograph of a plain white shelving unit in a small stockroom, holding a mix of unbranded flasks, tumblers and bottles in different sizes and finishes, arranged unevenly as if stocked by several different sellers: some upright, some on their sides, a few in plain brown cardboard sleeves with no printing. One cobalt-blue flask stands near the center of the middle shelf as the only saturated object. Soft diffused overhead light, shallow depth of field fading the outer shelves, subtle sense of an unsorted catalog rather than a store display. No labels, no price tags, no barcodes, no legible text, no people. Documentary logistics photography, 16:9 horizontal plate.

**Texto alternativo:** "A shelf of unbranded flasks and tumblers in mixed sizes, arranged unevenly, with one cobalt flask near the center."
**Pie:** "Many sellers, one shelf: the catalog is assembled from sources that never agreed on a format."

## 8. `chapter-05-card-terminal.jpg`
**Sección:** "El pago empieza con el modelo" / "Payment begins with the model"
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Documentary close-up of a blank, unbranded handheld payment terminal lying on a pale counter next to a closed cobalt-blue flask, shot from a slightly low angle in soft shop light. The terminal's screen is dark and its keys have no printed numbers or letters, no brand mark, no card network symbols. Shallow depth of field, the terminal sharp in the middle third and the flask softly out of focus behind it. Neutral grays and warm whites, cobalt as the only accent. No hands, no faces, no receipts, no legible text. 4:5 portrait.

**Texto alternativo:** "A blank handheld payment terminal on a counter next to a closed flask."
**Pie:** "Who sells, who receives funds and who refunds is settled before the checkout screen exists."

## 9. `chapter-05-two-parcels.jpg`
**Sección:** "El pedido sobrevive al pago" / "The order outlives checkout"
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Documentary still life of two small plain cardboard parcels placed side by side on a pale floor near a doorway, one tall and narrow (the size of a flask), one small and flat (the size of a lid), each closed with plain tape and a blank white label with no printing, no barcode, no address, no carrier marking. A thin cobalt-blue ribbon tied around the tall parcel as the single accent. Soft natural light from the door, shallow depth of field. No hands, no faces, no logos, no legible text. Editorial logistics photography, 4:5 portrait.

**Texto alternativo:** "Two small cardboard parcels with blank labels side by side, one holding a flask and one a replacement lid."
**Pie:** "One purchase for the customer, two shipments for the operation."

## 10. `chapter-05-doorstep-intercom.jpg`
**Sección:** "Un pin no es una entrega" / "A pin is not delivery"
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Documentary photograph of the entrance to an apartment building seen from the street: a metal gate with a plain intercom panel on the wall beside it, the panel's buttons and name slots blank and out of focus so nothing is legible, a side door slightly ajar further along the wall. Late-afternoon light, shallow depth of field with the intercom sharp in the middle third. A small cobalt-blue door handle or door frame on the side door as the single saturated accent. No people, no street signs, no house numbers, no legible text, no brand marks. Editorial urban photography, muted neutral palette, 4:5 portrait.

**Texto alternativo:** "A building entrance with a gate and an unlabeled intercom panel, softly out of focus."
**Pie:** "The coordinate points at the building; the courier needs the entrance."

## 11. `chapter-05-container-yard.jpg`
**Sección:** "La geografía llega a las copias" / "Geography reaches the copies"
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Documentary photograph of rows of stacked shipping containers at a port in overcast light, shot from a low angle between two stacks so the rows recede toward the vanishing point. All containers in plain weathered gray, white and rust tones with no company names, no logos, no container numbers, no legible markings; a single cobalt-blue container in one of the near rows as the only saturated object. Shallow depth of field, cool neutral palette. No people, no vehicles with markings, no signage. Editorial logistics photography, 4:5 portrait.

**Texto alternativo:** "Rows of plain, unmarked shipping containers at a port, with a single cobalt container in one row."
**Pie:** "Data, like cargo, leaves a record at every stop."

## 12. `chapter-05-key-ring.jpg`
**Sección:** "La seguridad se vuelve comportamiento del producto" / "Security becomes product behavior"
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Studio still life of a ring holding six plain metal keys of clearly different sizes and shapes, resting on a shallow brushed-metal tray against a pale gray background, soft overhead light, crisp reflections in the tray. One of the keys carries a small cobalt-blue plastic tag with no printing; the others are bare. Shallow depth of field, the ring in the middle third of the frame. No labels, no numbers, no brand stamps on the keys, no hands, no faces, no padlock or shield iconography. Editorial still-life photography, 4:5 portrait.

**Texto alternativo:** "A ring of several keys of different sizes, one with a cobalt tag, resting on a metal tray."
**Pie:** "Different keys for different doors: access follows responsibility."

## 13. `chapter-05-flask-and-phone.jpg`
**Sección:** "Lo que nos enseña el termo" / "What the flask teaches us" (cierre del capítulo)
**Medidas:** 4:5 · 2400×3000 px
**Prompt:**
> Documentary still life pairing a cobalt-blue vacuum flask standing upright next to a plain unbranded smartphone lying face-up, both on the same pale neutral surface under matched soft studio light. The phone's lock screen shows only a softly glowing cobalt-blue abstract geometric shape, no icons, no clock, no notifications, no text, no brand marks, and the phone's body has no visible logo. Shallow depth of field connecting the two objects visually as the same question in two materials. Muted grays with cobalt as the shared accent. No hands, no faces. Closing image of the chapter, 4:5 portrait.

**Texto alternativo:** "A cobalt flask and a smartphone showing an abstract cobalt shape on its lock screen, side by side on one surface."
**Pie:** "The same question, in two materials."

---

## Diagramas (se maquetan en código, no son fotografías)

Los dos diagramas del capítulo son SVG incrustado en el HTML, con el mismo estilo que los de los capítulos 3 y 4 (cajas blancas con borde gris, una caja cobalto como énfasis, texto en Archivo). No requieren archivo de imagen.

| Figura | Contenido | Estructura |
|--------|-----------|------------|
| 5.1 | El viaje de un valor de capacidad | Fabricante → Hoja del vendedor → **Registro canónico** (énfasis cobalto) → bifurca en Búsqueda y filtros / Presentación al comprador |
| 5.2 | Una compra, seis materiales | Capacidad → Stock → Dirección → Transportista → Pago → **Pedido** (énfasis cobalto), con la propiedad clave de cada caja debajo del nombre |

---

## Tabla resumen

| # | Archivo | Sección | Formato | Medidas |
|---|---------|---------|---------|---------|
| 1 | chapter-05-cobalt-flask-table.jpg | Antes del primer dibujo — Lámina 5.1 (cubierta) | 16:9 | 3200×1800 |
| 2 | chapter-05-three-uses.jpg | El propósito dentro del objeto | 4:5 | 2400×3000 |
| 3 | chapter-05-flask-components.jpg | Un material tiene dirección | 4:5 | 2400×3000 |
| 4 | chapter-05-weld-seam.jpg | El proceso cambia el material | 4:5 | 2400×3000 |
| 5 | chapter-05-cobalt-finish-samples.jpg | El color llega al mercado | 4:5 | 2400×3000 |
| 6 | chapter-05-measuring-jug.jpg | La capacidad necesita un idioma | 4:5 | 2400×3000 |
| 7 | chapter-05-drinkware-shelf.jpg | Del termo al marketplace — Lámina 5.2 | 16:9 | 3200×1800 |
| 8 | chapter-05-card-terminal.jpg | El pago empieza con el modelo | 4:5 | 2400×3000 |
| 9 | chapter-05-two-parcels.jpg | El pedido sobrevive al pago | 4:5 | 2400×3000 |
| 10 | chapter-05-doorstep-intercom.jpg | Un pin no es una entrega | 4:5 | 2400×3000 |
| 11 | chapter-05-container-yard.jpg | La geografía llega a las copias | 4:5 | 2400×3000 |
| 12 | chapter-05-key-ring.jpg | La seguridad se vuelve comportamiento del producto | 4:5 | 2400×3000 |
| 13 | chapter-05-flask-and-phone.jpg | Lo que nos enseña el termo (cierre) | 4:5 | 2400×3000 |

Notas:
- Las secciones "Una API contiene una promesa" y "Deja que la evidencia cambie el diseño" se maquetan como cita + ensayo y no llevan fotografía; "Mapa de los materiales digitales" (el método de cuatro etapas) se maqueta como proceso de cuatro pasos.
- Las 13 imágenes se usan igual en la versión EN y ES del capítulo (sin texto embebido); solo cambia el `alt` en el HTML.
- La imagen 1 es también la `cover_image` del capítulo en el frontmatter; para la vista previa de LinkedIn, exportar una variante 1200×630 recortada desde esta misma lámina.
