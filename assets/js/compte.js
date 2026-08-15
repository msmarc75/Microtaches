/* Tableau de bord de l'espace membre : rend l'écran correspondant à l'étape
   du parcours (candidature déposée, en examen, acceptée, activée, refusée). */
(function () {
  "use strict";

  var T = window.Tacheo;
  var root = document.getElementById("dashboard");
  if (!root) return;

  var badge = document.getElementById("stage-badge");
  var poll = null;

  var STAGE_LABEL = {
    "to-apply": ["Aucune candidature", "badge"],
    "review": ["Dossier en cours d'examen", "badge badge-amber"],
    "rejected": ["Dossier non retenu", "badge badge-red"],
    "to-activate": ["Candidature acceptée", "badge badge-green"],
    "active": ["Compte actif", "badge badge-green"]
  };

  function timeline(stage) {
    var s = T.Account.state();
    var steps = [
      { key: "apply", title: "Candidature déposée",
        text: s.application.submittedAt ? "Reçue le " + T.formatDate(s.application.submittedAt, true) : "Formulaire non transmis" },
      { key: "review", title: "Examen du dossier",
        text: "Nos équipes vérifient les informations et le test de consignes." },
      { key: "decision", title: "Décision",
        text: "Notifiée par e-mail et dans cet espace." },
      { key: "activation", title: "Activation du compte",
        text: "Vérification d'identité et ouverture du portefeuille de paiement." },
      { key: "work", title: "Accès aux missions",
        text: "Le catalogue s'ouvre selon votre profil." }
    ];

    var reached = { "to-apply": 0, "review": 1, "rejected": 2, "to-activate": 3, "active": 4 }[stage];

    return '<ul class="timeline">' + steps.map(function (st, i) {
      var cls = i < reached ? "tl-done" : (i === reached ? "tl-current" : "");
      var mark = i < reached ? "✓" : String(i + 1);
      return '<li class="' + cls + '"><span class="tl-dot">' + mark + '</span>' +
             "<div><strong>" + st.title + "</strong><p>" + st.text + "</p></div></li>";
    }).join("") + "</ul>";
  }

  function reviewProgress() {
    var s = T.Account.state();
    var start = new Date(s.application.submittedAt).getTime();
    var end = new Date(s.application.decisionAt).getTime();
    var pct = Math.min(100, Math.max(4, ((Date.now() - start) / (end - start)) * 100));
    return '<div class="runner-bar" style="margin-bottom:12px"><span style="width:' + pct.toFixed(1) + '%"></span></div>';
  }

  function render() {
    var stage = T.Account.stage();
    var s = T.Account.state();
    var label = STAGE_LABEL[stage] || ["", "badge"];
    badge.textContent = label[0];
    badge.className = label[1];

    if (poll) { clearInterval(poll); poll = null; }

    var main = "";
    var side = "";

    if (stage === "to-apply") {
      main = '<div class="card"><h2 style="font-size:1.25rem">Votre dossier n\'a pas encore été déposé</h2>' +
        "<p class=\"muted\">Le formulaire de candidature prend une dizaine de minutes. Il est gratuit et sans engagement.</p>" +
        '<a class="btn btn-primary" href="inscription.html">Déposer ma candidature</a></div>';
      side = '<div class="card"><h3 style="font-size:1rem">Besoin d\'aide ?</h3>' +
        '<p class="small muted mb-0">La <a href="faq.html">FAQ</a> détaille chaque étape du parcours.</p></div>';

    } else if (stage === "review") {
      main = '<div class="card"><h2 style="font-size:1.25rem">Votre dossier est en cours d\'examen</h2>' +
        reviewProgress() +
        '<p class="muted">Référence <strong>' + T.escapeHtml(s.application.ref) + "</strong> — déposé le " +
        T.formatDate(s.application.submittedAt, true) + ".</p>" +
        "<p class=\"muted\">Les candidatures sont étudiées sous 24 à 48 heures ouvrées. La décision apparaîtra " +
        "ici même et vous sera envoyée par e-mail. Aucune action n'est attendue de votre part.</p>" +
        '<p class="small muted mb-0">Cette page se met à jour automatiquement.</p></div>';
      side = '<div class="card"><h3 style="font-size:1rem">Pendant l\'attente</h3>' +
        '<ul class="small muted" style="padding-left:1.1em;margin-bottom:0">' +
        "<li>Préparez une pièce d'identité en cours de validité</li>" +
        "<li>Vérifiez que votre adresse e-mail est bien la bonne</li>" +
        "<li>Parcourez les <a href=\"missions.html\">familles de missions</a></li></ul></div>";
      poll = setInterval(function () {
        var st = T.Account.stage();
        if (st !== "review") { render(); T.toast("La décision sur votre dossier est disponible.", "ok"); }
        else { var bar = root.querySelector(".runner-bar span"); if (bar) bar.style.width = reviewProgress().match(/width:([\d.]+)%/)[1] + "%"; }
      }, 1000);

    } else if (stage === "rejected") {
      main = '<div class="card"><h2 style="font-size:1.25rem">Votre dossier n\'a pas été retenu</h2>' +
        '<div class="alert alert-red"><span class="alert-ico">✕</span><p class="mb-0">Le test de compréhension ' +
        "des consignes n'atteint pas le seuil requis (" + s.application.score + " bonnes réponses sur 5, seuil : " +
        T.CONFIG.passMark + ").</p></div>" +
        "<p class=\"muted\">Ce résultat ne remet pas en cause votre candidature future : un nouveau dossier peut " +
        "être déposé après sept jours. Relisez attentivement les consignes de chaque situation proposée.</p>" +
        '<button class="btn btn-ghost" id="retry">Déposer un nouveau dossier</button></div>';
      side = '<div class="card"><h3 style="font-size:1rem">Contester la décision</h3>' +
        '<p class="small muted mb-0">Vous pouvez écrire au support depuis la <a href="contact.html">page contact</a> ' +
        "en rappelant la référence " + T.escapeHtml(s.application.ref) + ".</p></div>";

    } else if (stage === "to-activate") {
      main = '<div class="card">' +
        '<div class="alert alert-green"><span class="alert-ico">🎉</span><p class="mb-0">' +
        "<strong>Bonne nouvelle : votre candidature est acceptée.</strong> Décision rendue le " +
        T.formatDate(s.application.resolvedAt || s.application.decisionAt, true) + ".</p></div>" +
        '<h2 style="font-size:1.25rem">Dernière étape : activer votre compte</h2>' +
        "<p class=\"muted\">L'activation couvre la vérification de votre identité, l'ouverture de votre " +
        "portefeuille de paiement et l'accès permanent au catalogue de missions.</p>" +
        '<div class="alert alert-amber"><span class="alert-ico">💳</span><p class="mb-0">' +
        "Montant : <strong>20,00 € TTC, dus une seule fois.</strong> Ni abonnement, ni reconduction, " +
        "ni prélèvement ultérieur. Détail des prestations et droit de rétractation dans les " +
        '<a href="cgv.html">conditions de vente</a>.</p></div>' +
        '<a class="btn btn-lg btn-green" href="activation.html">Activer mon compte</a>' +
        '<p class="small muted mt-2 mb-0">Votre acceptation reste valable trente jours.</p></div>';
      side = '<div class="card"><h3 style="font-size:1rem">Après l\'activation</h3>' +
        '<ul class="small muted" style="padding-left:1.1em;margin-bottom:0">' +
        "<li>Accès immédiat aux lots de missions</li><li>150 crédits de bienvenue</li>" +
        "<li>Retraits possibles dès 2 500 crédits</li></ul></div>";

    } else {
      var done = s.tasks.log.length;
      var earned = s.wallet.history.reduce(function (a, h) { return a + (h.credits > 0 ? h.credits : 0); }, 0);
      main =
        '<div class="kpi-row">' +
          '<div class="kpi"><small>Solde</small><b>' + s.wallet.credits.toLocaleString("fr-FR") + " cr</b>" +
            '<span class="small muted">' + T.creditsToEuros(s.wallet.credits) + "</span></div>" +
          '<div class="kpi"><small>Missions validées</small><b>' + done + "</b>" +
            '<span class="small muted">depuis l\'activation</span></div>' +
          '<div class="kpi"><small>Taux de qualité</small><b>' + (done ? "98 %" : "—") + "</b>" +
            '<span class="small muted">100 dernières unités</span></div>' +
        "</div>" +
        '<div class="card"><h2 style="font-size:1.15rem">Dernières missions</h2>' +
        (done
          ? '<table class="table"><thead><tr><th>Mission</th><th>Date</th><th class="num">Crédits</th></tr></thead><tbody>' +
            s.tasks.log.slice(0, 6).map(function (l) {
              return "<tr><td>" + T.escapeHtml(l.title) + "</td><td>" + T.formatDate(l.date, true) +
                     '</td><td class="num">+' + l.credits + "</td></tr>";
            }).join("") + "</tbody></table>"
          : '<p class="muted">Aucune mission traitée pour le moment. Le catalogue vous attend.</p>') +
        '<a class="btn btn-primary mt-2" href="taches.html">Voir les missions disponibles</a></div>';
      side =
        '<div class="card"><h3 style="font-size:1rem">Compte activé</h3>' +
        '<p class="small muted">Activation réglée le ' + T.formatDate(s.activation.paidAt) +
        " — référence " + T.escapeHtml(s.activation.ref || "—") + ".</p>" +
        '<p class="small muted mb-0">Total gagné : <strong>' + earned.toLocaleString("fr-FR") +
        " crédits</strong> (" + T.creditsToEuros(earned) + ").</p></div>" +
        '<div class="card mt-2"><h3 style="font-size:1rem">Retraits</h3>' +
        '<p class="small muted">Seuil : 2 500 crédits. Virement SEPA sous 2 à 5 jours ouvrés.</p>' +
        '<a class="btn btn-ghost btn-block btn-sm" href="portefeuille.html">Ouvrir le portefeuille</a></div>';
    }

    root.innerHTML = '<div class="app-grid"><div>' + main + '</div><aside>' + side +
      '<div class="card mt-2"><h3 style="font-size:1rem">Suivi de votre dossier</h3>' + timeline(stage) +
      "</div></aside></div>";

    var retry = document.getElementById("retry");
    if (retry) {
      retry.addEventListener("click", function () {
        T.Account.resetApplication();
        window.location.href = "inscription.html";
      });
    }
  }

  render();
})();
