# 0701 Ingeniería C.A.

Web de 0701 Ingeniería C.A. (Lechería, Anzoátegui), empresa del Ing. Gabriel A. Forero León. Hecha por muelle0.

## Arquitectura

Estática, sin dependencias: `public/` con HTML, CSS y JS. Se publica en Cloudflare Pages (directorio de salida `public`, sin comando de build). Sin secretos ni admin por ahora.

- `public/index.html`: una sola página con seis "láminas" (portada, obras, servicios, cuadro de obras, empresa, contacto) y el pie como cajetín de plano.
- `public/css/estilos.css`, `public/js/main.js` (menú móvil y cotas a escala).
- `public/_headers`: CSP estricta y caché. Nada inline: el JSON-LD es un bloque de datos y no se ejecuta.
- `fuentes/`: fotos originales que mandó la familia (1080 px). Las del brochure se extrajeron del PDF y son pequeñas (300 a 900 px).

Desarrollo local: `cd public && python3 -m http.server 8790`.

## Dirección de diseño (aprobada)

- **Concepto:** la web es un juego de planos. Cada sección es una lámina ("Lám. 02 · Obras"), el pie es un cajetín con RIF y representante legal, y las magnitudes reales de Plaza Mayor se dibujan como cotas a la misma escala. Fondo cuadriculado solo en la portada y en el plano de Plaza Mayor.
- **Tipografía:** Archivo variable (titulares a `font-stretch:74%`, peso 640; texto a 100%), IBM Plex Mono para etiquetas, cotas, años y lugares. Alojadas en `public/fonts`.
- **Colores:** `#0d2a4a` marino (fondo del brochure), `#1d4569` azul (muestreado del logo), `#f1b432` amarillo (acento del brochure), `#f5f3ee` papel de plano, `#23272b` grafito.
- **Componentes:** botón rectangular marino con filete amarillo a la izquierda; enlaces subrayados; cotas con líneas de extensión y trazos a 45°. Cada obra sigue el mismo orden: dos fotos, año y lugar, título, el reto / lo que hicimos, cliente.
- **No tiene:** "¿Por qué elegirnos?", contadores animados, testimonios, fotos de stock del brochure (ingeniero con laptop, almacén, topógrafos, asfaltado aéreo), números decorativos.
- **Logo:** PNG del brochure con el fondo convertido en transparencia (azul y blanco), sin la línea del RIF. Pendiente el archivo vectorial original.

## Pendientes del cliente

- Proyecto Farmacia SAAS de Anaco: alcance, año y fotos.
- Alquiler de equipos: andamios y herramientas que se puedan ofrecer.
- Proyectos 2025 y 2026 que falten, y más historia de la empresa.
- Fotos originales en alta (Digitel, Tijerazo, Polar, Plaza Mayor) y vídeos cortos de obra para minivídeos.
- Logo en vector.
- Confirmar Marina Kalina: en el brochure aparece con cliente Cervecería Polar y lugar Planta Barcelona, que parece un error; en la web va como "Marina Kalina, Anzoátegui".
- Confirmar si Cocoyar y Perfoca siguen como aliados.
- Dominio (luego actualizar og:image absoluta, canonical y sitemap).
