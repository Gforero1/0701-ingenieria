(function () {
  'use strict';
  document.documentElement.classList.add('js');

  // Menú en móvil
  var boton = document.querySelector('.menu-boton');
  var menu = document.getElementById('menu');
  if (boton && menu) {
    boton.addEventListener('click', function () {
      var abierto = menu.classList.toggle('abierta');
      boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
      boton.textContent = abierto ? 'Cerrar' : 'Menú';
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        menu.classList.remove('abierta');
        boton.setAttribute('aria-expanded', 'false');
        boton.textContent = 'Menú';
      }
    });
  }

  // Cotas a escala: el largo sale de data-l y la línea se traza al entrar en pantalla
  var cotas = document.querySelectorAll('.cota[data-l]');
  cotas.forEach(function (c) {
    var l = parseFloat(c.getAttribute('data-l'));
    if (l > 0 && l <= 1) {
      c.style.setProperty('--l', l);
      if (l < 0.3) c.classList.add('cota--corta');
    }
  });
  var todas = document.querySelectorAll('.cota');
  if (!('IntersectionObserver' in window)) {
    todas.forEach(function (c) { c.classList.add('vista'); });
    return;
  }
  var vigia = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('vista'); vigia.unobserve(e.target); }
    });
  }, { threshold: 0.6 });
  todas.forEach(function (c) { vigia.observe(c); });
})();
