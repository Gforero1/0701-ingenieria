#!/usr/bin/env python3
"""Genera las páginas de public/ a partir de contenido.py. Uso: python3 build.py"""
import html, os, re
from contenido import EMPRESA as E, SERVICIOS, CLIENTES, OBRAS, CUADRO

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
V = "12"
esc = html.escape
MARCA = open(os.path.join(RAIZ, "img", "marca.svg")).read()
LOGO = open(os.path.join(RAIZ, "img", "logo.svg")).read()


def svg(src, clase, etiqueta=None):
    s = src.replace("<svg ", f'<svg class="{clase}" ' + (f'role="img" aria-label="{etiqueta}" ' if etiqueta else 'aria-hidden="true" focusable="false" '), 1)
    return s


def img(nombre, alt, base, tam="(min-width: 900px) 50vw, 100vw", clase="", carga="lazy", prioridad=False):
    """Fotos en dos anchos: -800 y -1600."""
    w, h = DIM.get(nombre, (1600, 1200))
    extra = ' fetchpriority="high"' if prioridad else ""
    return (f'<img class="{clase}" src="{base}img/fotos/{nombre}-800.webp" '
            f'srcset="{base}img/fotos/{nombre}-800.webp 800w, {base}img/fotos/{nombre}-1600.webp 1600w" '
            f'sizes="{tam}" width="{w}" height="{h}" alt="{esc(alt)}" loading="{carga}" decoding="async"{extra}>')


def cargar_dim():
    d = {}
    ruta = os.path.join(RAIZ, "img", "fotos", "dimensiones.txt")
    if os.path.exists(ruta):
        for linea in open(ruta):
            n, w, h = linea.split()
            d[n] = (int(w), int(h))
    return d


DIM = cargar_dim()


def cabeza(titulo, descripcion, base, canonica):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
<meta name="theme-color" content="#0d2a4a">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_VE">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:image" content="{base}img/compartir.jpg">
<link rel="icon" href="{base}img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{base}img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{base}img/apple-touch-icon.png">
<link rel="preload" href="{base}fonts/redhat-display.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}css/estilos.css?v={V}">
</head>
"""


def cabecera(base, activa=""):
    def a(href, txt, clave):
        cur = ' aria-current="page"' if clave == activa else ""
        return f'<a href="{href}"{cur}>{txt}</a>'
    return f"""<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="cab">
  <div class="cab__in">
    <a class="cab__logo" href="{base}" aria-label="0701 Ingeniería C.A., inicio">{svg(LOGO, 'logo')}</a>
    <button class="cab__menu" type="button" aria-expanded="false" aria-controls="nav">Menú</button>
    <nav id="nav" class="nav" aria-label="Principal">
      {a(base + '#servicios', 'Servicios', 'servicios')}
      {a(base + 'obras/', 'Obras', 'obras')}
      {a(base + '#empresa', 'Empresa', 'empresa')}
      <a class="nav__cta" href="{base}#contacto">Contacto</a>
    </nav>
  </div>
</header>
"""


def contacto(base):
    return f"""<section id="contacto" class="contacto">
  {svg(MARCA, 'contacto__marca')}
  <div class="env contacto__in">
    <div>
      <p class="antetitulo">Contacto</p>
      <h2 class="titulo">Cuéntenos qué necesita <span>construir, reparar o medir</span></h2>
      <p class="contacto__txt">Respondemos por WhatsApp y por correo. Si tiene planos, fotos o una orden de trabajo, envíela con el mensaje.</p>
      <div class="acciones">
        <a class="boton boton--marino" href="{E['whatsapp']}" rel="noopener">Escribir por WhatsApp</a>
        <a class="boton boton--linea" href="mailto:{E['correo']}">{E['correo']}</a>
      </div>
    </div>
    <dl class="contacto__datos">
      <div><dt>Teléfonos</dt><dd><a href="tel:{E['tel1_href']}">{E['tel1']}</a><br><a href="tel:{E['tel2_href']}">{E['tel2']}</a></dd></div>
      <div><dt>Dirección</dt><dd>{E['direccion'][0]}<br>{E['direccion'][1]}</dd></div>
      <div><dt>RIF</dt><dd>{E['rif']}</dd></div>
    </dl>
  </div>
</section>
"""


def pie(base):
    return f"""<footer class="pie">
  <div class="env pie__in">
    <div class="pie__marca">{svg(LOGO, 'logo logo--blanco', '0701 Ingeniería C.A.')}<p>Ingeniería, construcción y mantenimiento en el oriente de Venezuela desde 2006.</p></div>
    <div><h2>Navegación</h2><ul><li><a href="{base}#servicios">Servicios</a></li><li><a href="{base}obras/">Obras</a></li><li><a href="{base}obras/#cuadro">Cuadro de obras</a></li><li><a href="{base}#empresa">Empresa</a></li></ul></div>
    <div><h2>Contacto</h2><ul><li><a href="{E['whatsapp']}" rel="noopener">WhatsApp</a></li><li><a href="tel:{E['tel1_href']}">{E['tel1']}</a></li><li><a href="tel:{E['tel2_href']}">{E['tel2']}</a></li><li><a href="mailto:{E['correo']}">{E['correo']}</a></li></ul></div>
    <div><h2>Empresa</h2><ul><li>{E['nombre']}</li><li>RIF {E['rif']}</li><li>{E['sede']}</li></ul></div>
  </div>
  <div class="env pie__base"><span>© 2026 {E['nombre']}</span><span>Web: <a href="https://muelle0.com" rel="noopener">muelle0</a></span></div>
</footer>
<div class="visor" hidden><button class="visor__cerrar" type="button" aria-label="Cerrar">Cerrar</button><img alt=""><p class="visor__pie"></p></div>
<script src="{base}js/main.js?v={V}" defer></script>
</body>
</html>
"""


def tarjeta_obra(o, base, grande=False):
    clase = "obra-t obra-t--grande" if grande else "obra-t"
    if o["slug"] == "plaza-mayor":
        media = f"""<div class="obra-t__plano">{svg(MARCA, 'obra-t__marca')}<dl><div><dt>Edificios</dt><dd>45.000 m²</dd></div><div><dt>Estacionamiento</dt><dd>60.000 m²</dd></div><div><dt>Muelle</dt><dd>750 ml</dd></div></dl></div>"""
    else:
        media = img(o["fotos"][0][0], o["fotos"][0][1], base, "(min-width: 900px) 60vw, 100vw" if grande else "(min-width: 900px) 33vw, 100vw", "obra-t__img")
    lista = ('<ul class="obra-t__lista">' + "".join(f"<li>{esc(x)}</li>" for x in o["alcance"][:4]) + "</ul>") if grande else ""
    return f"""<a class="{clase}" href="{base}obras/{o['slug']}/">
  <div class="obra-t__media">{media}</div>
  <div class="obra-t__txt">
    <p class="obra-t__meta">{o['periodo']} · {esc(o['ubicacion'])}</p>
    <h3>{esc(o['titulo'])}</h3>
    <p>{esc(o['resumen'])}</p>
    {lista}<span class="obra-t__ver">Memoria descriptiva</span>
  </div>
</a>"""


def tabla_cuadro():
    filas = "\n".join(f"<tr><td>{a}</td><td>{esc(c)}</td><td>{esc(d)}</td><td>{esc(l)}</td></tr>" for a, c, d, l in CUADRO)
    return f"""<div class="tabla-env"><table class="tabla">
<thead><tr><th scope="col">Año</th><th scope="col">Cliente</th><th scope="col">Descripción</th><th scope="col">Lugar</th></tr></thead>
<tbody>
{filas}
</tbody></table></div>"""


def inicio():
    b = ""
    servicios = "\n".join(f"""<li class="srv">
  <div class="srv__img">{img(s['img'], s['titulo'], b, '(min-width: 1100px) 33vw, (min-width: 720px) 50vw, 100vw')}</div>
  <h3>{s['titulo']}</h3>
  <p>{s['texto']}</p>
</li>""" for s in SERVICIOS)
    obras = tarjeta_obra(OBRAS[0], b, True) + "\n<div class=\"obras__rejilla\">" + "\n".join(tarjeta_obra(o, b) for o in OBRAS[1:]) + "</div>"
    clientes = "".join(f"<li>{esc(c)}</li>" for c in CLIENTES)
    ld = ('{"@context":"https://schema.org","@type":"GeneralContractor","name":"0701 Ingeniería C.A.","taxID":"J-31628414-0","foundingDate":"2006-08",'
          '"email":"0701bim@gmail.com","telephone":["+58 424-862-9487","+58 412-840-7792"],"founder":{"@type":"Person","name":"Gabriel A. Forero León","jobTitle":"Ingeniero civil estructural"},'
          '"address":{"@type":"PostalAddress","streetAddress":"Calle Sur, Edif. Arabella, piso 9, apto. 91, sector Venecia","addressLocality":"Lechería","addressRegion":"Anzoátegui","postalCode":"6016","addressCountry":"VE"},'
          '"areaServed":"Anzoátegui, Venezuela"}')
    h = cabeza("0701 Ingeniería C.A. | Ingeniería, construcción y mantenimiento en Anzoátegui",
               "Empresa de ingeniería, construcción y mantenimiento con sede en Lechería, Anzoátegui, desde 2006. Concreto armado y acero para plantas industriales, centros comerciales y torres de telecomunicaciones.", b, "/")
    h = h.replace("</head>", f'<script type="application/ld+json">{ld}</script>\n</head>')
    return h + cabecera(b) + f"""
<main id="contenido">

<section class="portada">
  <div class="portada__foto">{img('deposito-columnas', 'Columnas de concreto armado y nave metálica del depósito para Tijerazo', b, '100vw', carga='eager', prioridad=True)}</div>
  <div class="portada__franja" aria-hidden="true"></div>
  <div class="portada__cuna" aria-hidden="true"></div>
  <div class="portada__panel" aria-hidden="true"></div>
  {svg(MARCA, 'portada__marca')}
  <div class="env portada__txt">
    <p class="antetitulo antetitulo--claro">Lechería · Anzoátegui · Desde 2006</p>
    <h1>Ingeniería, construcción y mantenimiento <span>para la industria y la edificación</span></h1>
    <div class="acciones">
      <a class="boton" href="{E['whatsapp']}" rel="noopener">Hablar de un proyecto</a>
      <a class="enlace enlace--claro" href="obras/">Ver obras</a>
    </div>
  </div>
</section>

<section class="intro">
  <div class="env intro__in">
    <div class="intro__cab">
      <p class="antetitulo">Nuestra organización</p>
      <h2 class="titulo">Concreto armado y acero <span>desde 2006</span></h2>
    </div>
    <div class="intro__txt">
      <p class="intro__entrada">0701 Ingeniería C.A. diseña, construye y mantiene instalaciones industriales y edificaciones en el oriente de Venezuela. Trabajamos en plantas de producción, centros comerciales, tiendas y torres de telecomunicaciones, para la industria petrolera, del gas, la minería, el comercio y la construcción civil.</p>
      <p>La empresa la dirige un ingeniero civil estructural con más de 35 años de oficio, postgrado en Ingeniería de Mantenimiento y BIM Manager, que con su equipo acompaña al cliente desde el diagnóstico inicial hasta la implementación.</p>
    </div>
    <dl class="cifras">
      <div><dt>Fundación</dt><dd>2006</dd><p>En Lechería, estado Anzoátegui</p></div>
      <div><dt>Experiencia del director</dt><dd>35+</dd><p>Años de ingeniería estructural</p></div>
      <div><dt>Plaza Mayor</dt><dd>105.000 m²</dd><p>De edificios y estacionamiento a nuestro cargo</p></div>
    </dl>
  </div>
</section>

<section id="servicios" class="servicios">
  <div class="env">
    <div class="servicios__cab">
      <p class="antetitulo antetitulo--claro">Servicios</p>
      <h2 class="titulo titulo--claro">Nuestros <span>servicios</span></h2>
      <p class="servicios__entrada">De la ingeniería conceptual al mantenimiento de la planta en operación, con equipo propio y aliados para topografía y geotecnia.</p>
    </div>
    <ul class="srv-rejilla">
{servicios}
    </ul>
  </div>
</section>

<section class="obras" id="obras">
  <div class="env">
    <div class="obras__cab">
      <div><p class="antetitulo">Experiencia en obras</p><h2 class="titulo">Obras <span>recientes</span></h2></div>
      <a class="enlace" href="obras/">Todas las obras y el cuadro desde 2008</a>
    </div>
    {obras}
  </div>
</section>

<section class="clientes" aria-label="Clientes">
  <div class="env clientes__in"><p class="antetitulo">Han confiado en nosotros</p><ul>{clientes}</ul></div>
</section>

<section id="empresa" class="empresa">
  <div class="env empresa__in">
    <figure class="empresa__foto"><div class="empresa__marco">{img('gabriel-forero', 'El ingeniero Gabriel Forero en la obra del depósito, con la cuadrilla montando la estructura detrás', b, '(min-width: 900px) 45vw, 100vw')}</div><figcaption>Ing. Gabriel A. Forero León en la obra del depósito, 2026.</figcaption></figure>
    <div class="empresa__txt">
      <p class="antetitulo">Empresa</p>
      <h2 class="titulo">Dirigida por <span>un ingeniero estructural</span></h2>
      <p>El <strong>Ing. Gabriel A. Forero León</strong>, representante legal de 0701, es ingeniero civil estructural con más de 35 años de experiencia, postgrado en Ingeniería de Mantenimiento y BIM Manager.</p>
      <div class="mv">
        <div><h3>Misión</h3><p>Dar soluciones integrales de ingeniería, construcción y mantenimiento, con asesoría experta y gestión eficiente, para que los procesos y proyectos de nuestros clientes rindan más.</p></div>
        <div><h3>Visión</h3><p>Ser el aliado preferido de la industria y la infraestructura del oriente del país, con excelencia operativa, prácticas seguras y respeto por el entorno.</p></div>
      </div>
      <h3 class="empresa__sub">Aliados</h3>
      <dl class="aliados">
        <div><dt>Servicios Integrales Cocoyar C.A.</dt><dd>Aerofotogrametría y LIDAR con drones (más de 12.000 hectáreas levantadas), escáner láser, batimetría, mapeo móvil y sistemas de información geográfica.</dd></div>
        <div><dt>Perfoca</dt><dd>Geotecnia, estudios de suelo, estabilidad de taludes, micropilotaje, fundaciones y perforación de pozos de agua.</dd></div>
      </dl>
    </div>
  </div>
</section>

</main>
""" + contacto(b) + pie(b)


def indice_obras():
    b = "../"
    tarjetas = "\n".join(tarjeta_obra(o, b) for o in OBRAS)
    return cabeza("Obras | 0701 Ingeniería C.A.", "Obras de 0701 Ingeniería C.A. desde 2008: Cervecería Polar, Centro Comercial Plaza Mayor, tiendas Tijerazo, torres de Digitel, Edificio Zantronic y Hotel Eurobuilding.", b, "/obras/") + cabecera(b, "obras") + f"""
<main id="contenido">
<section class="cabeza-pag">
  {svg(MARCA, 'cabeza-pag__marca')}
  <div class="env">
    <p class="antetitulo antetitulo--claro">Experiencia en obras</p>
    <h1>Obras</h1>
    <p class="cabeza-pag__txt">Cada obra tiene su memoria descriptiva: objeto, descripción, alcance de los trabajos, datos técnicos y registro fotográfico. Al final, el cuadro con todas las obras desde 2008.</p>
  </div>
</section>
<section class="obras obras--pag">
  <div class="env"><div class="obras__rejilla obras__rejilla--pag">{tarjetas}</div></div>
</section>
<section id="cuadro" class="cuadro">
  <div class="env">
    <p class="antetitulo">Cuadro de obras</p>
    <h2 class="titulo">Cuadro <span>de obras</span></h2>
    {tabla_cuadro()}
  </div>
</section>
</main>
""" + contacto(b) + pie(b)


def memoria(i, o):
    b = "../../"
    sig = OBRAS[(i + 1) % len(OBRAS)]
    ant = OBRAS[i - 1]
    descr = "".join(f"<p>{esc(p)}</p>" for p in o["descripcion"])
    alcance = "".join(f"<li>{esc(a)}</li>" for a in o["alcance"])
    datos = "".join(f"<tr><th scope=\"row\">{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in o["datos"])
    fotos = "".join(f'<figure><a href="{b}img/fotos/{n}-1600.webp" class="galeria__a" data-pie="{esc(p)}">{img(n, p, b, "(min-width: 900px) 33vw, 50vw")}</a><figcaption>{esc(p)}</figcaption></figure>' for n, p in o["fotos"])
    portada = ""
    if len(o["fotos"]) >= 3:
        f = o["fotos"]
        portada = (f'<div class="mosaico">{img(f[0][0], f[0][1], b, "(min-width: 900px) 66vw, 100vw", "", "eager", True)}'
                   f'{img(f[1][0], f[1][1], b, "(min-width: 900px) 33vw, 50vw")}{img(f[2][0], f[2][1], b, "(min-width: 900px) 33vw, 50vw")}</div>')
    ficha = f"""<dl class="ficha">
      <div><dt>Cliente</dt><dd>{esc(o['cliente'])}</dd></div>
      <div><dt>Ubicación</dt><dd>{esc(o['ubicacion'])}</dd></div>
      <div><dt>Período</dt><dd>{o['periodo']}</dd></div>
      <div><dt>Tipo de obra</dt><dd>{esc(o['tipo'])}</dd></div>
    </dl>"""
    secciones = [("objeto", "Objeto", f"<p>{esc(o['objeto'])}</p>"),
                 ("descripcion", "Descripción de la obra", descr),
                 ("alcance", "Alcance de los trabajos", f'<ul class="alcance">{alcance}</ul>'),
                 ("datos", "Datos técnicos", f'<table class="datos-t"><tbody>{datos}</tbody></table>'),
                 ("registro", "Registro fotográfico", f'<div class="galeria">{fotos}</div>')]
    indice = "".join(f'<li><a href="#{k}"><span>{n}.</span> {t}</a></li>' for n, (k, t, _) in enumerate(secciones, 1))
    cuerpo = "".join(f'<section id="{k}" class="memo__sec"><h2><span>{n}.</span> {t}</h2>{c}</section>' for n, (k, t, c) in enumerate(secciones, 1))
    return cabeza(f"{o['titulo']} | Memoria descriptiva | 0701 Ingeniería C.A.", o["resumen"], b, f"/obras/{o['slug']}/") + cabecera(b, "obras") + f"""
<main id="contenido">
<section class="cabeza-pag cabeza-pag--memo">
  {svg(MARCA, 'cabeza-pag__marca')}
  <div class="env">
    <nav class="migas" aria-label="Ruta"><a href="{b}obras/">Obras</a> <span aria-hidden="true">/</span> {esc(o['corto'])}</nav>
    <p class="antetitulo antetitulo--claro">Memoria descriptiva</p>
    <h1>{esc(o['titulo'])}</h1>
    {ficha}
  </div>
</section>
{f'<div class="memo__portada">{portada}</div>' if portada else ''}
<div class="env memo">
  <aside class="memo__indice"><p>Contenido</p><ol>{indice}</ol></aside>
  <article class="memo__cuerpo">{cuerpo}</article>
</div>
<nav class="memo__nav env" aria-label="Otras obras">
  <a href="{b}obras/{ant['slug']}/"><span>Obra anterior</span>{esc(ant['corto'])}</a>
  <a href="{b}obras/{sig['slug']}/"><span>Obra siguiente</span>{esc(sig['corto'])}</a>
</nav>
</main>
""" + contacto(b) + pie(b)


def escribir(ruta, texto):
    ruta = os.path.join(RAIZ, ruta)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    assert "—" not in texto, f"guion largo en {ruta}"
    open(ruta, "w").write(texto)


escribir("index.html", inicio())
escribir("obras/index.html", indice_obras())
for i, o in enumerate(OBRAS):
    escribir(f"obras/{o['slug']}/index.html", memoria(i, o))
urls = ["", "obras/"] + [f"obras/{o['slug']}/" for o in OBRAS]
print("ok", len(urls), "páginas")
