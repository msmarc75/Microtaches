/* Exécution d'un lot de missions : écran d'introduction, enchaînement des
   éléments à traiter selon le type de mission, puis écran de validation. */
(function () {
  "use strict";

  var T = window.Tacheo;
  var view = document.getElementById("task-view");
  if (!view) return;

  var id = new URLSearchParams(window.location.search).get("id");
  var task = (window.TACHEO_TASKS || []).filter(function (t) { return t.id === id; })[0];

  if (!task) {
    view.innerHTML = '<div class="card"><h1 style="font-size:1.4rem">Lot introuvable</h1>' +
      '<p class="muted">Ce lot n\'existe pas ou n\'est plus disponible.</p>' +
      '<a class="btn btn-primary" href="taches.html">Retour aux missions</a></div>';
    return;
  }

  document.title = task.title + " — Tacheo";

  var index = 0;
  var answers = [];

  function normalize(value) {
    return String(value).toLowerCase().trim()
      .replace(/\s+/g, " ")
      .replace(/€/g, "")
      .replace(/\./g, ",")
      .trim();
  }

  function progressBar() {
    var pct = (index / task.items.length) * 100;
    return '<div class="runner-bar"><span style="width:' + pct + '%"></span></div>' +
      '<p class="small muted">Élément ' + (index + 1) + " sur " + task.items.length +
      " · +" + task.credits + " crédits pour le lot complet</p>";
  }

  function intro() {
    view.innerHTML = '<div class="runner">' +
      '<div class="card-ico">' + task.icon + "</div>" +
      '<span class="badge badge-violet">' + T.escapeHtml(task.category) + "</span>" +
      "<h1 style=\"font-size:1.6rem;margin-top:12px\">" + T.escapeHtml(task.title) + "</h1>" +
      '<p class="lead">' + T.escapeHtml(task.summary) + "</p>" +
      '<div class="kpi-row" style="margin:22px 0">' +
        '<div class="kpi"><small>Rémunération</small><b>+' + task.credits + " cr</b><span class=\"small muted\">" +
          T.creditsToEuros(task.credits) + "</span></div>" +
        '<div class="kpi"><small>Durée estimée</small><b>' + task.minutes + " min</b><span class=\"small muted\">pour le lot</span></div>" +
        '<div class="kpi"><small>Éléments</small><b>' + task.items.length + "</b><span class=\"small muted\">à traiter</span></div>" +
      "</div>" +
      '<div class="alert alert-violet"><span class="alert-ico">📋</span><div>' +
        "<strong>Consignes</strong><ul class=\"small\" style=\"padding-left:1.1em;margin:8px 0 0\">" +
        task.brief.map(function (b) { return "<li>" + T.escapeHtml(b) + "</li>"; }).join("") +
      "</ul></div></div>" +
      '<p class="small muted">Le lot doit être terminé pour être rémunéré. Vous pouvez l\'interrompre, ' +
      "mais les éléments déjà traités seront perdus.</p>" +
      '<button class="btn btn-lg btn-primary btn-block" id="start">Commencer le lot</button></div>';

    document.getElementById("start").addEventListener("click", function () {
      index = 0; answers = []; step();
    });
  }

  /* ---- Rendu d'un élément selon le type de mission ---- */

  function bodyFor(item) {
    switch (task.type) {
      case "classify":
        return '<div class="sample sample-big" role="img" aria-label="Visuel à classer">' + item.visual + "</div>" +
          '<p class="field-label">Quelle catégorie correspond à ce visuel ?</p>' +
          '<div class="answer-grid">' + item.options.map(function (o, i) {
            return '<button type="button" class="answer-btn" data-value="' + i + '">' + T.escapeHtml(o) + "</button>";
          }).join("") + "</div>";

      case "choice":
        return '<div class="sample">' + T.escapeHtml(item.text) + "</div>" +
          '<p class="field-label">Quelle décision appliquez-vous ?</p>' +
          '<div class="answer-grid">' + task.options.map(function (o, i) {
            return '<button type="button" class="answer-btn" data-value="' + i + '">' + T.escapeHtml(o) + "</button>";
          }).join("") + "</div>";

      case "survey":
        return '<div class="sample">' + T.escapeHtml(item.question) + "</div>" +
          '<div class="answer-grid">' + item.options.map(function (o, i) {
            return '<button type="button" class="answer-btn" data-value="' + i + '">' + T.escapeHtml(o) + "</button>";
          }).join("") + "</div>";

      case "verify":
        return '<div class="sample"><strong>Fiche A</strong><br>' + T.escapeHtml(item.a) + "</div>" +
          '<div class="sample"><strong>Fiche B</strong><br>' + T.escapeHtml(item.b) + "</div>" +
          '<p class="field-label">Ces deux fiches décrivent-elles la même réalité ?</p>' +
          '<div class="answer-grid">' +
            '<button type="button" class="answer-btn" data-value="1">Oui, elles correspondent</button>' +
            '<button type="button" class="answer-btn" data-value="0">Non, elles diffèrent</button>' +
            '<button type="button" class="answer-btn" data-value="2">Impossible de trancher</button>' +
          "</div>";

      case "entry":
        var rows = Object.keys(item.sample).map(function (k) {
          return "<tr><th>" + T.escapeHtml(k) + "</th><td>" + T.escapeHtml(item.sample[k]) + "</td></tr>";
        }).join("");
        return '<div class="sample"><table class="table">' + rows + "</table></div>" +
          '<form id="entry-form">' + item.fields.map(function (f) {
            return '<div class="field"><label for="f-' + f.name + '">' + T.escapeHtml(f.label) + "</label>" +
              '<input type="text" id="f-' + f.name + '" data-expect="' + T.escapeHtml(f.expect || "") + '" required></div>';
          }).join("") +
          '<button class="btn btn-primary btn-block" type="submit">Valider cet élément</button></form>';

      case "transcribe":
        return '<div class="sample" style="text-align:center">' +
            '<button type="button" class="btn btn-ghost" id="play">▶ Écouter l\'extrait</button>' +
            '<p class="tiny muted mt-2 mb-0">Extrait de moins de 20 secondes — réécoute possible.</p>' +
            '<p class="small mt-2 hide" id="fallback"></p>' +
          "</div>" +
          '<form id="entry-form"><div class="field">' +
            '<label for="f-text">Retranscription</label>' +
            '<textarea id="f-text" required placeholder="Saisissez ici le contenu de l\'extrait…"></textarea>' +
            '<p class="hint">Ponctuation attendue. Mot inaudible : [inaudible].</p></div>' +
          '<button class="btn btn-primary btn-block" type="submit">Valider cet élément</button></form>';

      default:
        return "<p>Type de mission non pris en charge.</p>";
    }
  }

  function step() {
    if (index >= task.items.length) return finish();
    var item = task.items[index];

    view.innerHTML = '<div class="runner">' + progressBar() +
      '<h2 style="font-size:1.15rem">' + T.escapeHtml(task.title) + "</h2>" +
      '<div class="runner-item">' + bodyFor(item) + "</div>" +
      '<p class="small muted mt-3 mb-0"><a href="taches.html">Interrompre le lot</a></p></div>';

    /* Réponses par bouton */
    T.qsa(".answer-btn", view).forEach(function (btn) {
      btn.addEventListener("click", function () {
        answers.push(btn.getAttribute("data-value"));
        index++;
        step();
      });
    });

    /* Réponses par formulaire (saisie et transcription) */
    var form = document.getElementById("entry-form");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var values = {};
        var ok = true;

        T.qsa("input, textarea", form).forEach(function (field) {
          var holder = field.closest(".field");
          var old = holder.querySelector(".error-text");
          if (old) old.remove();
          field.classList.remove("input-error");

          var value = field.value.trim();
          var expect = field.getAttribute("data-expect");
          var minimum = task.type === "transcribe" ? 20 : 1;

          if (value.length < minimum) {
            ok = false;
            field.classList.add("input-error");
            var p = document.createElement("p");
            p.className = "error-text";
            p.textContent = task.type === "transcribe"
              ? "La retranscription semble trop courte."
              : "Ce champ est obligatoire.";
            holder.appendChild(p);
            return;
          }
          if (expect && normalize(expect) !== normalize(value)) {
            ok = false;
            field.classList.add("input-error");
            var q = document.createElement("p");
            q.className = "error-text";
            q.textContent = "La saisie ne correspond pas au document affiché. Vérifiez ce champ.";
            holder.appendChild(q);
            return;
          }
          values[field.id] = value;
        });

        if (!ok) return;
        answers.push(values);
        index++;
        step();
      });
    }

    /* Lecture de l'extrait audio, par synthèse vocale du navigateur */
    var play = document.getElementById("play");
    if (play) {
      play.addEventListener("click", function () {
        var text = task.items[index].audio;
        if (!("speechSynthesis" in window)) {
          var fb = document.getElementById("fallback");
          fb.textContent = "Lecture audio indisponible sur ce navigateur. Contenu de l'extrait : « " + text + " »";
          fb.classList.remove("hide");
          return;
        }
        window.speechSynthesis.cancel();
        var utter = new SpeechSynthesisUtterance(text);
        utter.lang = "fr-FR";
        utter.rate = 0.95;
        window.speechSynthesis.speak(utter);
      });
    }
  }

  function finish() {
    if ("speechSynthesis" in window) window.speechSynthesis.cancel();
    T.Account.creditTask(task, task.credits);
    var s = T.Account.state();

    view.innerHTML = '<div class="runner center">' +
      '<div class="card-ico ico-green" style="margin:0 auto 14px">✓</div>' +
      '<h1 style="font-size:1.5rem">Lot terminé</h1>' +
      '<p class="lead">Les ' + task.items.length + " éléments ont été soumis au contrôle qualité.</p>" +
      '<div class="alert alert-green" style="text-align:left"><span class="alert-ico">💶</span>' +
        "<p class=\"mb-0\"><strong>+" + task.credits + " crédits</strong> (" + T.creditsToEuros(task.credits) +
        ") ont été versés sur votre portefeuille. Nouveau solde : <strong>" +
        s.wallet.credits.toLocaleString("fr-FR") + " crédits</strong>.</p></div>" +
      '<div class="btn-row" style="justify-content:center">' +
        '<a class="btn btn-primary" href="taches.html">Traiter un autre lot</a>' +
        '<a class="btn btn-ghost" href="portefeuille.html">Voir mon portefeuille</a>' +
      "</div></div>";

    T.toast("Lot validé : +" + task.credits + " crédits.", "ok");
  }

  intro();
})();
