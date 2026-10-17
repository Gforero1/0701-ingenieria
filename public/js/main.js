(function () {
  'use strict';
  var raiz = document.documentElement;
  raiz.classList.add('js');
  var reducir = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Menú en móvil
  var boton = document.querySelector('.cab__menu');
  var nav = document.getElementById('nav');
  function cerrarMenu() {
    nav.classList.remove('abierta');
    boton.setAttribute('aria-expanded', 'false');
    boton.textContent = 'Menú';
  }
  if (boton && nav) {
    boton.addEventListener('click', function () {
      var abierto = nav.classList.toggle('abierta');
      boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
      boton.textContent = abierto ? 'Cerrar' : 'Menú';
    });
    nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') cerrarMenu(); });
  }

  // Aparición al hacer scroll (tarjetas de obras y servicios)
  var aparecen = document.querySelectorAll('.srv, .obra-t, .cifras > div');
  if (!reducir && 'IntersectionObserver' in window) {
    var vigia = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('vista'); vigia.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });
    aparecen.forEach(function (el) { el.classList.add('revela'); vigia.observe(el); });
  }

  // Índice de la memoria descriptiva: marca la sección visible
  var enlaces = document.querySelectorAll('.memo__indice a');
  if (enlaces.length && 'IntersectionObserver' in window) {
    var porId = {};
    enlaces.forEach(function (a) { porId[a.getAttribute('href').slice(1)] = a; });
    var vigiaSec = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) {
          enlaces.forEach(function (a) { a.classList.remove('activo'); });
          var a = porId[e.target.id];
          if (a) a.classList.add('activo');
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.memo__sec').forEach(function (s) { vigiaSec.observe(s); });
  }

  // Visor de fotos del registro fotográfico
  var visor = document.querySelector('.visor');
  var fotos = document.querySelectorAll('.galeria__a');
  if (visor && fotos.length) {
    var vImg = visor.querySelector('img');
    var vPie = visor.querySelector('.visor__pie');
    var vCerrar = visor.querySelector('.visor__cerrar');
    var origen = null;
    function cerrar() {
      visor.hidden = true;
      vImg.removeAttribute('src');
      document.body.style.overflow = '';
      if (origen) origen.focus();
    }
    fotos.forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        origen = a;
        vImg.src = a.getAttribute('href');
        vImg.alt = a.getAttribute('data-pie') || '';
        vPie.textContent = a.getAttribute('data-pie') || '';
        visor.hidden = false;
        document.body.style.overflow = 'hidden';
        vCerrar.focus();
      });
    });
    vCerrar.addEventListener('click', cerrar);
    visor.addEventListener('click', function (e) { if (e.target === visor) cerrar(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !visor.hidden) cerrar(); });
  }
})();
