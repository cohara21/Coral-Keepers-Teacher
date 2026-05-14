(function () {
  function initUnitTabs() {
    var cards = document.querySelectorAll('.sidebar .unit-card');
    var panels = document.querySelectorAll('.unit-panel');
    if (!cards.length || !panels.length) return;

    function showUnit(id) {
      for (var i = 0; i < panels.length; i++) {
        panels[i].hidden = panels[i].getAttribute('data-unit') !== id;
      }
      for (var j = 0; j < cards.length; j++) {
        var c = cards[j];
        var on = c.getAttribute('data-unit') === id;
        if (on) c.classList.add('active');
        else c.classList.remove('active');
        c.setAttribute('aria-pressed', on ? 'true' : 'false');
      }
      try {
        history.replaceState(null, '', '#unit-' + id);
      } catch (e) {}
    }

    for (var k = 0; k < cards.length; k++) {
      cards[k].addEventListener('click', function () {
        showUnit(this.getAttribute('data-unit'));
      });
    }

    var m = (location.hash || '').match(/^#unit-(\d+)/);
    showUnit(m ? m[1] : '1');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUnitTabs);
  } else {
    initUnitTabs();
  }
})();
