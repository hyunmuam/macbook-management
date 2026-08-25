// 명령 복사. file:// 에서는 navigator.clipboard가 막히므로 execCommand로 물러선다.
document.querySelectorAll('.cmd .copy, .snip .copy').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var text = btn.parentElement.querySelector('code').textContent;
    var done = function () {
      btn.textContent = '복사됨';
      btn.classList.add('done');
      setTimeout(function () { btn.textContent = '복사'; btn.classList.remove('done'); }, 1400);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else { fallback(); }
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { btn.textContent = '실패'; }
      document.body.removeChild(ta);
    }
  });
});

// 현재 읽는 절을 목차에 표시하고, 그 절의 하위만 펼친다.
// 화면 교차가 아니라 스크롤 위치로 판정한다. 짧은 절이 건너뛰어지지 않는다.
(function () {
  var links = {};
  document.querySelectorAll('.toc a').forEach(function (a) {
    links[decodeURIComponent(a.getAttribute('href').slice(1))] = a;
  });
  var targets = Array.prototype.slice
    .call(document.querySelectorAll('section[id], .rule[id], .sub h3[id], h4[id]'))
    .filter(function (el) { return links[el.id]; });
  if (!targets.length) { return; }

  var current = null;
  function update() {
    var line = 96;  // 이 높이를 지난 마지막 제목이 현재 절이다
    var found = targets[0];
    for (var i = 0; i < targets.length; i++) {
      if (targets[i].getBoundingClientRect().top <= line) { found = targets[i]; } else { break; }
    }
    if (found === current) { return; }
    current = found;
    Object.keys(links).forEach(function (id) { links[id].classList.remove('here'); });
    document.querySelectorAll('.toc li.open').forEach(function (li) { li.classList.remove('open'); });
    var a = links[found.id];
    a.classList.add('here');
    var li = a.closest('li');
    var top = li;
    while (top.parentElement.closest('li')) { top = top.parentElement.closest('li'); }
    top.classList.add('open');
    if (top !== li) { top.querySelector('a').classList.add('here'); }
    var box = document.querySelector('.toc');
    if (box && a.offsetTop < box.scrollTop) { box.scrollTop = a.offsetTop - 40; }
    if (box && a.offsetTop > box.scrollTop + box.clientHeight - 40) {
      box.scrollTop = a.offsetTop - box.clientHeight + 80;
    }
  }

  var ticking = false;
  function onScroll() {
    if (ticking) { return; }
    ticking = true;
    requestAnimationFrame(function () { update(); ticking = false; });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();
