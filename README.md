# 0701 Ingeniería C.A.

Web de 0701 Ingeniería C.A. (Lechería, Anzoátegui), empresa del Ing. Gabriel A. Forero León. Hecha por muelle0.

## Arquitectura

Estática, sin dependencias en el navegador. Se publica en Cloudflare Pages con directorio de salida `public` y sin comando de build (las páginas se generan aquí y se suben hechas).

- `contenido.py`: todos los textos, servicios, obras (con su memoria descriptiva) y el cuadro de obras.
- `build.py`: genera `public/index.html`, `public/obras/index.html` y una página de memoria descriptiva por obra en `public/obras/<slug>/`.
- `herramientas/fotos.py`: corrige y exporta las fotos a WebP 800 y 1600 px en `public/img/fotos/`. Si existe la versión mejorada con Real-ESRGAN la usa; si no, la original.
- `public/img/logo.svg` y `marca.svg`: logo vectorizado con `herramientas/logo_vector.py` (PNG del brochure subido x10, suavizado y trazado con potrace) para que aguante a tamaño gigante. Se pintan con `currentColor`.
- `public/_headers`: CSP estricta y caché. Nada inline salvo el JSON-LD, que es un bloque de datos.
- `fuentes/`: fotos originales que mandó la familia.

Flujo: editar `contenido.py`, `python3 build.py`, revisar con `cd public && python3 -m http.server 8790`, commit y push.

### Fotos

- **Mejoradas con ChatGPT (octubre 2026):** 18 fotos del brochure pasaron por ChatGPT con la instrucción de no añadir ni cambiar nada (`fuentes/chatgpt/`, exportadas con `herramientas/fotos_gpt.py`). Cada una se comparó con su original antes de aprobarla. `srv-ingenieria` no se usa de ChatGPT (inventaba la cara): va la original del teléfono que mandó la familia (`fuentes/gabriel-azotea-h.jpg`). `srv-levantamientos` salió bien al segundo intento, pidiendo no escribir marcas. En `digitel-antenas` el cielo gris pasó a azul. Originales del brochure en `fuentes/brochure/`.

Las fotos del brochure venían a 300 a 900 px. Se pasaron por Real-ESRGAN x4plus en CPU (`esrgan.py`, arquitectura RRDBNet sin basicsr) y después por `fotos.py`: CLAHE suave en luminancia, niveles al 0,4 y 99,6 %, saturación +8 %. Las fotos del teléfono (depósito, Plaza Mayor, procura, selfie) ya no pasan por Real-ESRGAN, que les daba aspecto de pintura: van tal cual, a su tamaño original. Las URLs de las fotos llevan `?v=` para que nadie vea la versión vieja en caché.

## Dirección de diseño

- **Portada:** el techo (franja blanca, cuña amarilla y panel marino) se ancla con desplazamientos fijos (`--t`, `--iz`, `--de`) y el texto va debajo, así no se pisan en ninguna altura de pantalla.
- **Origen:** el brochure corporativo 2025. La portada copia su composición: foto arriba, franja blanca y panel marino en forma de techo, cuña amarilla a la izquierda y el 0701 gigante en blanco cortado por el borde inferior.
- **Logo:** el 0701 se usa como supergráfico en portada, cabeceras de página, tarjeta de Plaza Mayor y contacto (blanco sobre marino o en tono sobre tono).
- **Tipografía:** el brochure usa Gotham. Aquí Red Hat Display (titulares en mayúsculas 800, antetítulos con tracking .2em como el "INGENIERIA" del logo) y Red Hat Text para el texto. Alojadas en `public/fonts`.
- **Colores:** `#0d2a4a` marino y `#f1b432` amarillo (muestreados del brochure), `#1d4569` azul (logo), `#0a2240` pie, `#f2f4f7` gris claro.
- **Títulos a dos tonos** como en el brochure ("NUESTROS SERVICIOS"): sobre marino la segunda parte va en amarillo; sobre blanco lleva un subrayado amarillo grueso.
- **Componentes:** botones con el borde derecho en diagonal; antetítulo con barra amarilla; secciones con cortes diagonales; esquinas rectas, sin sombras.
- **Obras:** cada una tiene memoria descriptiva (objeto, descripción, alcance, datos técnicos, registro fotográfico) con índice lateral y visor de fotos.
- **No tiene:** fotos de stock del brochure, testimonios, contadores animados.

## Pendientes del cliente

- Farmacia SAAS de Anaco: alcance, año y fotos.
- Alquiler de equipos (andamios y herramientas): qué se ofrece.
- Proyectos 2025 y 2026 que falten, y más historia de la empresa.
- Plaza Mayor solo tiene una foto: pedir fotos del centro comercial y del edificio de Rio Automercado.
- Fotos originales en alta (Digitel, Tijerazo, Polar, Plaza Mayor) y vídeos cortos de obra para minivídeos.
- Logo en vector original.
- Depósito Tijerazo: confirmar ubicación y alcance exacto (la memoria se escribió a partir de las fotos).
- Marina Kalina: en el brochure aparece con cliente Cervecería Polar y lugar Planta Barcelona, que parece un error; en la web va como "Marina Kalina, Anzoátegui".
- Confirmar si Cocoyar y Perfoca siguen como aliados.
- Dominio (luego og:image absoluta, canonical y sitemap).
