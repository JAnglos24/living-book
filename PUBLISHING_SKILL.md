---
name: living-book-publisher
description: Instrucciones y pipeline obligatorio paso a paso para publicar nuevos capítulos en el sitio Astro "Living Book" de J.A. Sosa. Contiene la solución a SVGs negros (CSP bypass) y el flujo de Wrangler Deploy local para evitar colapsos de Puppeteer en la nube.
---

# Living Book Publisher Skill

Este skill orquesta el proceso estricto de publicación, actualización y validación para el sitio en Astro de "Living Book" (jasosal.com). Úsalo CADA VEZ que el usuario pida "publicar el nuevo capítulo", "actualizar el sitio", o "subir el libro".

## 1. Reglas Estructurales de un Capítulo
Cada capítulo tiene una versión en español y otra en inglés, usando arquitecturas distintas que DEBES respetar.
- **Español:** Se construye directamente en un archivo Astro: `src/pages/es/ebook/XX-slug/index.astro`.
- **Inglés:** Se construye usando Content Collections con MDX: `src/content/ebook/XX-slug.mdx`. Esta ruta es renderizada dinámicamente por `src/pages/ebook/[slug].astro`.

**Checklist:**
1. Asegurarse de que ambos archivos (MDX para EN, Astro para ES) existan.
2. Validar que se ha actualizado `scripts/generate-pdf.mjs` para incluir la ruta del nuevo capítulo en la matriz `EDITIONS` (en ambos lenguajes). Esto garantiza que el capítulo se imprima en la descarga PDF del libro.

## 2. REGLA DE ORO (CRÍTICA): Los SVGs vs Content Security Policy (CSP)
**JAMÁS** uses clases de CSS (ej. `class="dbox"`) ni atributos de estilo en línea (ej. `style="fill:#FFFFFF;"`) para los elementos internos de un SVG (`<rect>`, `<text>`, `<line>`, `<path>`). 

- Si usas clases CSS, Astro las descartará al compilar MDX por su scoping.
- Si usas `style="..."`, **Cloudflare Pages lo bloqueará y borrará en producción** por sus estrictas políticas de CSP contra `unsafe-inline`, provocando que el SVG se renderice 100% negro en la página web en vivo.

**Procedimiento Obligatorio para SVGs:**
DEBES usar **Atributos de Presentación SVG Nativos**.
- En lugar de `class="dbox"` o `style="fill:#FFFFFF; stroke-width:1.5"`, DEBES usar `fill="#FFFFFF" stroke="#C9D0D8" stroke-width="1.5"`.
- Los colores (`fill`, `stroke`) deben ser valores hexadecimales literales duros.
- Tipografías: `font-family="Archivo,sans-serif" font-weight="700"`.

## 3. Despliegue (Bypass de Cloudflare Pages Build)
**NUNCA dependas del auto-build de GitHub a Cloudflare.** 
El sitio utiliza `puppeteer` en el script `postbuild` (`generate-pdf.mjs`) para compilar el ebook PDF. Los servidores ligeros de Cloudflare Pages no tienen dependencias de Linux para Chromium, por lo que Puppeteer revienta silenciosamente, cancelando la publicación del PDF y abortando todo el build en producción.

**Pasos de Despliegue Obligatorio:**
Para que el usuario vea su sitio y los PDFs en producción, el build debe ejecutarse LOCALMENTE en la computadora del usuario, y subirse pre-empaquetado con Wrangler.

```powershell
# Ejecutar siempre en: D:\Proyectos personales\personal branding\living_book_astro
npm run deploy
```
Este comando ejecutará `npm run build` (que creará los PDFs usando el Chrome local de Windows) y automáticamente usará `wrangler deploy` para empujar la carpeta `dist/` viva a los bordes de Cloudflare. 

## 4. Flujo Seguro de Git Push (Evitar cuelgues del SO)
Aunque Cloudflare ya esté actualizado por Wrangler, el código debe subirse a GitHub para versionamiento.
**ATENCIÓN:** El usuario está en Windows y si haces un `git push` regular sin token explícito, Windows lanzará el "Git Credential Manager" bloqueando la consola del agente de por vida.

**Pasos OBLIGATORIOS:**
1. Leer el token local del archivo `.env` (`D:\Proyectos personales\personal branding\living_book_astro\.env`).
   *Nunca le muestres el token al usuario en el chat.*
2. Hacer commit y empujar con URL autenticada:
   `git add .`
   `git commit -m "feat(ebook): publish chapter XX..."`
   `git push https://<AQUI_VA_EL_TOKEN_EXTRAIDO>@github.com/JAnglos24/living-book.git master`

## 5. Artículos de LinkedIn (Personal Branding Swarm)
Si el usuario publica un nuevo capítulo, averigua si ya existe el artículo de LinkedIn escrito para ese capítulo. Si existe, pide el enlace y actualiza `src/pages/articles.astro` y `src/pages/es/articles.astro`. Si no, recomiéndale usar el skill de `personal-branding-swarm` para redactar y publicar los posts de forma óptima.
