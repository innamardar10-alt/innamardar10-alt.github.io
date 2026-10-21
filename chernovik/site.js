(function () {
  var B = document.documentElement.getAttribute('data-base') || '';
  var words = { 'НАХОДКА': B + '/avito-guide/odna-nakhodka/', 'ГИД': B + '/avito-guide/', 'КОДЫ': B + '/kody/' };
  function norm(v) { return (v || '').trim().toUpperCase().replace(/Ё/g, 'Е').replace(/[^А-ЯA-Z0-9]/g, ''); }
  function go(input, status) {
    var w = norm(input.value);
    if (words[w]) { status.textContent = 'Открываю…'; location.href = words[w]; }
    else if (!w) { status.textContent = 'Введите слово из поста или рилса.'; }
    else { status.textContent = 'Такого слова пока нет. Проверьте, как оно написано в посте.'; }
  }

  // поиск по кодовому слову в меню
  var btn = document.querySelector('.lupa');
  var panel = document.getElementById('search');
  if (btn && panel) {
    btn.addEventListener('click', function () {
      var open = panel.hidden;
      panel.hidden = !open;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) panel.querySelector('input').focus();
    });
    panel.querySelector('form').addEventListener('submit', function (e) {
      e.preventDefault();
      go(panel.querySelector('input'), panel.querySelector('.search-status'));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) { panel.hidden = true; btn.setAttribute('aria-expanded', 'false'); btn.focus(); }
    });
  }

  // поле кодового слова на главной
  var f = document.getElementById('code-form');
  if (f) f.addEventListener('submit', function (e) {
    e.preventDefault();
    go(document.getElementById('code-input'), document.getElementById('code-status'));
  });

  // «Вернуться обратно»: на страницу, откуда пришли; если пришли не с сайта — на страницу уровнем выше
  var backs = document.querySelectorAll('[data-back]');
  for (var i = 0; i < backs.length; i++) {
    backs[i].addEventListener('click', function (e) {
      try {
        var r = document.referrer ? new URL(document.referrer) : null;
        if (r && r.origin === location.origin && r.href !== location.href && history.length > 1) {
          e.preventDefault();
          history.back();
        }
      } catch (_) {}
    });
  }

  // «Наверх»
  var up = document.querySelector('.up');
  if (up) {
    var t = function () { up.classList.toggle('show', window.scrollY > 500); };
    window.addEventListener('scroll', t, { passive: true });
    t();
  }
})();
