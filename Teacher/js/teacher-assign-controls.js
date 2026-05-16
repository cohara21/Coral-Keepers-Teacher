(function () {
  var STORAGE_KEY = 'ck_teacher_post_assign_v1';
  var documentCloseBound = false;

  function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text == null ? '' : String(text);
    return div.innerHTML;
  }

  function loadMap() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    } catch (e) {
      return {};
    }
  }

  function saveMap(map) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(map));
    } catch (e) {}
  }

  function pagePrefix() {
    return location.pathname.replace(/.*\//, '') || 'post';
  }

  function storageId(index) {
    return pagePrefix() + ':' + index;
  }

  function clickInsideAssignUi(target) {
    if (!target || !target.closest) return false;
    return !!target.closest('.assign-container');
  }

  function closeAllAssignDropdowns() {
    var alld = document.querySelectorAll('.assign-dropdown.show');
    for (var k = 0; k < alld.length; k++) alld[k].classList.remove('show');
    var btns = document.querySelectorAll('.assign-container .topic-action-btn');
    for (var b = 0; b < btns.length; b++) btns[b].setAttribute('aria-expanded', 'false');
    var opens = document.querySelectorAll('.assign-container.ck-assign-open');
    for (var o = 0; o < opens.length; o++) opens[o].classList.remove('ck-assign-open');
  }

  function setCoryActive(active) {
    if (active) document.body.classList.add('ck-cory-active');
    else document.body.classList.remove('ck-cory-active');
  }

  function clickInsideCory(target) {
    if (!target || !target.closest) return false;
    return !!target.closest('#cory-iframe');
  }

  function ensureAssignStyles() {
    if (document.getElementById('ck-assign-controls-style')) return;
    var s = document.createElement('style');
    s.id = 'ck-assign-controls-style';
    s.textContent =
      '.assign-container{z-index:10010!important;position:relative}' +
      '.assign-container.ck-assign-open{z-index:10020!important}' +
      '.assign-dropdown{z-index:10030!important}' +
      '#cory-iframe{z-index:10000!important}' +
      'body.ck-cory-active #cory-iframe{z-index:10040!important}';
    document.head.appendChild(s);
  }

  var CHECK_SVG =
    '<svg class="assign-icon check" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>';
  var CHEVRON_SVG =
    '<svg class="assign-icon chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>';

  function initAssignControls() {
    ensureAssignStyles();

    var wrap = document.querySelector('.content-wrap');
    if (wrap) wrap.style.overflow = 'visible';

    if (!documentCloseBound) {
      documentCloseBound = true;
      document.addEventListener('click', function (ev) {
        if (clickInsideCory(ev.target)) {
          setCoryActive(true);
          closeAllAssignDropdowns();
          return;
        }
        setCoryActive(false);
        if (clickInsideAssignUi(ev.target)) return;
        closeAllAssignDropdowns();
      });
    }

    var coryIframe = document.getElementById('cory-iframe');
    if (coryIframe && !coryIframe.getAttribute('data-ck-layer-bound')) {
      coryIframe.setAttribute('data-ck-layer-bound', 'true');
      coryIframe.addEventListener('pointerdown', function () {
        setCoryActive(true);
        closeAllAssignDropdowns();
      });
      coryIframe.addEventListener('focus', function () {
        setCoryActive(true);
        closeAllAssignDropdowns();
      });
    }

    var map = loadMap();
    var assignContainers = document.querySelectorAll('.assign-container');
    var i;

    for (i = 0; i < assignContainers.length; i++) {
      (function (container, index) {
        var btn = container.querySelector('.topic-action-btn');
        if (!btn) return;

        btn.setAttribute('type', 'button');

        var dropdown = container.querySelector('.assign-dropdown');
        if (!dropdown) {
          dropdown = document.createElement('div');
          dropdown.className = 'assign-dropdown';
          container.appendChild(dropdown);
        }

        var sid = storageId(index);
        var raw = map[sid];
        var storedOk = Object.prototype.hasOwnProperty.call(map, sid) && raw != null && typeof raw === 'object';

        function persist(entry) {
          var m = loadMap();
          m[sid] = entry;
          saveMap(m);
        }

        function renderUnassigned() {
          dropdown.innerHTML =
            '<button type="button" class="dropdown-item" data-action="quick">Quick Assign</button>' +
            '<button type="button" class="dropdown-item" data-action="date">Add Due Date...</button>' +
            '<button type="button" class="dropdown-item" data-action="visibility">Schedule Visibility...</button>';
          attachItemEvents();
        }

        function renderAssigned() {
          dropdown.innerHTML =
            '<button type="button" class="dropdown-item" data-action="edit-date">Edit Due Date...</button>' +
            '<button type="button" class="dropdown-item" data-action="edit-visibility">Edit Visibility...</button>' +
            '<button type="button" class="dropdown-item destructive" data-action="unassign">Unassign</button>';
          attachItemEvents();
        }

        function setAssigned(label, skipPersist) {
          btn.classList.add('assigned');
          btn.classList.remove('unassigned');
          btn.innerHTML = CHECK_SVG + '<span>' + escapeHtml(label) + '</span>';
          btn.setAttribute('aria-expanded', 'false');
          container.classList.remove('ck-assign-open');
          renderAssigned();
          if (!skipPersist) persist({ a: true, l: label });
        }

        function setUnassigned(skipPersist) {
          btn.classList.remove('assigned');
          btn.classList.add('unassigned');
          btn.innerHTML = '<span>Assign</span>' + CHEVRON_SVG;
          btn.setAttribute('aria-expanded', 'false');
          container.classList.remove('ck-assign-open');
          renderUnassigned();
          if (!skipPersist) persist({ a: false });
        }

        function attachItemEvents() {
          var items = dropdown.querySelectorAll('.dropdown-item');
          var j;
          for (j = 0; j < items.length; j++) {
            (function (item) {
              item.addEventListener('click', function (e) {
                e.stopPropagation();
                var action = item.getAttribute('data-action');
                dropdown.classList.remove('show');
                btn.setAttribute('aria-expanded', 'false');
                container.classList.remove('ck-assign-open');

                if (action === 'quick') {
                  setAssigned('Assigned');
                } else if (action === 'date') {
                  var d = window.prompt('Enter Due Date (e.g. April 20, 2026):', 'April 20, 2026');
                  if (d) setAssigned('Due ' + d);
                } else if (action === 'visibility') {
                  var v = window.prompt('Schedule for when? (e.g. Tomorrow 8AM):', 'Tomorrow 8AM');
                  if (v) setAssigned('Scheduled ' + v);
                } else if (action === 'unassign') {
                  setUnassigned();
                } else if (action === 'edit-date' || action === 'edit-visibility') {
                  var u = window.prompt('Update setting:', '');
                  if (u) setAssigned(action === 'edit-date' ? 'Due ' + u : 'Scheduled ' + u);
                }
              });
            })(items[j]);
          }
        }

        btn.addEventListener('click', function (e) {
          e.stopPropagation();
          var willOpen = !dropdown.classList.contains('show');
          var alld = document.querySelectorAll('.assign-dropdown.show');
          for (var j = 0; j < alld.length; j++) {
            if (alld[j] !== dropdown) alld[j].classList.remove('show');
          }
          var otherOpens = document.querySelectorAll('.assign-container.ck-assign-open');
          for (var x = 0; x < otherOpens.length; x++) {
            if (otherOpens[x] !== container) otherOpens[x].classList.remove('ck-assign-open');
          }
          if (willOpen) {
            dropdown.classList.add('show');
            container.classList.add('ck-assign-open');
          } else {
            dropdown.classList.remove('show');
            container.classList.remove('ck-assign-open');
          }
          btn.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
        });

        if (storedOk) {
          if (raw.a === true) setAssigned(raw.l || 'Assigned', true);
          else setUnassigned(true);
        } else {
          if (btn.classList.contains('assigned')) {
            renderAssigned();
          } else {
            renderUnassigned();
          }
        }
      })(assignContainers[i], i);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAssignControls);
  } else {
    initAssignControls();
  }
})();
