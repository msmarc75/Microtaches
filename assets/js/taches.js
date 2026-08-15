/* Catalogue des lots de missions : filtres par famille et rendu des cartes. */
(function () {
  "use strict";

  var T = window.Tacheo;
  var grid = document.getElementById("task-grid");
  var filters = document.getElementById("filters");
  if (!grid) return;

  var tasks = window.TACHEO_TASKS || [];
  var categories = ["Toutes"].concat(tasks.map(function (t) { return t.category; })
    .filter(function (c, i, arr) { return arr.indexOf(c) === i; }));
  var active = "Toutes";

  function renderFilters() {
    filters.innerHTML = categories.map(function (c) {
      return '<button class="chip' + (c === active ? " is-on" : "") + '" data-cat="' +
        T.escapeHtml(c) + '">' + T.escapeHtml(c) + "</button>";
    }).join("");
    T.qsa(".chip", filters).forEach(function (chip) {
      chip.addEventListener("click", function () {
        active = chip.getAttribute("data-cat");
        renderFilters();
        renderGrid();
      });
    });
  }

  function renderGrid() {
    var state = T.Account.state();
    var visible = tasks.filter(function (t) { return active === "Toutes" || t.category === active; });

    grid.innerHTML = visible.map(function (t) {
      var done = state.tasks.done[t.id] || 0;
      return '<article class="card card-hover task-card">' +
        '<div class="card-ico">' + t.icon + "</div>" +
        '<span class="badge badge-violet">' + T.escapeHtml(t.category) + "</span>" +
        "<h3>" + T.escapeHtml(t.title) + "</h3>" +
        '<p class="small muted">' + T.escapeHtml(t.summary) + "</p>" +
        '<div class="task-meta">' +
          '<span class="badge">⏱️ ' + t.minutes + " min</span>" +
          '<span class="badge">📦 ' + t.items.length + " éléments</span>" +
          '<span class="badge">🎯 ' + T.escapeHtml(t.level) + "</span>" +
          (done ? '<span class="badge badge-green">✓ ' + done + " fois</span>" : "") +
        "</div>" +
        '<div class="task-foot">' +
          '<span class="pay">+' + t.credits + " cr<small>" + T.creditsToEuros(t.credits) + "</small></span>" +
          '<a class="btn btn-sm btn-primary" href="tache.html?id=' + encodeURIComponent(t.id) + '">Ouvrir le lot</a>' +
        "</div></article>";
    }).join("");

    if (!visible.length) {
      grid.innerHTML = '<p class="muted">Aucun lot disponible dans cette famille pour le moment.</p>';
    }
  }

  renderFilters();
  renderGrid();
})();
