/* ==========================================================================
   Tacheo — couche applicative
   Démonstration 100 % front-end : l'état du membre est conservé dans le
   localStorage du navigateur. Aucune donnée n'est transmise à un serveur.
   Pour une mise en production, remplacer les fonctions de Store.* par des
   appels à une API (voir README.md).
   ========================================================================== */
(function () {
  "use strict";

  var STORAGE_KEY = "tacheo.v1";

  /* Paramètres métier — centralisés pour rester modifiables au même endroit. */
  var CONFIG = {
    // Frais d'activation unique, dû une seule fois après acceptation du dossier.
    activationFee: 20,
    currency: "EUR",
    // Délai simulé d'examen du dossier. En production : décision humaine.
    reviewDelayMs: 25 * 1000,
    // Note minimale au test d'aptitude (sur 5) pour être accepté.
    passMark: 3,
    // 100 crédits = 1 €
    creditsPerEuro: 100,
    // Seuil minimal de retrait, en crédits.
    payoutThreshold: 2500,
    welcomeCredits: 150
  };

  /* ---------------------------------------------------------------- Store */

  var Store = {
    read: function () {
      try {
        var raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : null;
      } catch (e) {
        return null;
      }
    },
    write: function (state) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      } catch (e) {
        /* quota ou navigation privée : on ignore silencieusement */
      }
      return state;
    },
    clear: function () {
      try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
    },
    blank: function () {
      return {
        user: null,
        session: false,
        application: { status: "none" },
        activation: { paid: false },
        wallet: { credits: 0, history: [] },
        tasks: { done: {}, log: [] }
      };
    }
  };

  /* ------------------------------------------------------------- Utilitaires */

  function uid(prefix) {
    var n = Math.floor(Math.random() * 9e5) + 1e5;
    return (prefix || "TC") + "-" + new Date().getFullYear() + "-" + n;
  }

  function euros(value) {
    return value.toLocaleString("fr-FR", { style: "currency", currency: "EUR" });
  }

  function creditsToEuros(credits) {
    return euros(credits / CONFIG.creditsPerEuro);
  }

  function formatDate(iso, withTime) {
    if (!iso) return "—";
    var d = new Date(iso);
    var opts = { day: "2-digit", month: "long", year: "numeric" };
    if (withTime) { opts.hour = "2-digit"; opts.minute = "2-digit"; }
    return d.toLocaleDateString("fr-FR", opts);
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  /* Hachage volontairement basique : la démo ne stocke pas de mot de passe en
     clair, mais ceci ne remplace pas un hachage serveur (bcrypt/argon2). */
  function weakHash(str) {
    var h = 5381, i = 0;
    for (; i < str.length; i++) h = ((h << 5) + h + str.charCodeAt(i)) | 0;
    return "h" + Math.abs(h).toString(36);
  }

  /* ---------------------------------------------------------------- Compte */

  var Account = {
    state: function () {
      var s = Store.read();
      if (!s) s = Store.write(Store.blank());
      return Account.refresh(s);
    },

    save: function (state) { return Store.write(state); },

    isLogged: function () {
      var s = Account.state();
      return !!(s.user && s.session);
    },

    /* Fait avancer la machine à états : une candidature « en examen » dont le
       délai est écoulé devient acceptée ou refusée selon la note obtenue. */
    refresh: function (s) {
      var app = s.application;
      if (app && app.status === "review" && app.decisionAt && Date.now() >= new Date(app.decisionAt).getTime()) {
        app.status = app.score >= CONFIG.passMark ? "accepted" : "rejected";
        app.resolvedAt = new Date().toISOString();
        Store.write(s);
      }
      return s;
    },

    register: function (data) {
      var s = Store.read() || Store.blank();
      s.user = {
        id: uid("MB"),
        prenom: data.prenom,
        nom: data.nom,
        email: String(data.email || "").toLowerCase().trim(),
        pays: data.pays || "France",
        telephone: data.telephone || "",
        pass: weakHash(data.password || ""),
        createdAt: new Date().toISOString()
      };
      s.session = true;
      return Store.write(s);
    },

    login: function (email, password) {
      var s = Account.state();
      if (!s.user) return { ok: false, error: "Aucun compte n'est enregistré sur cet appareil." };
      if (s.user.email !== String(email).toLowerCase().trim()) {
        return { ok: false, error: "Adresse e-mail inconnue." };
      }
      if (s.user.pass !== weakHash(password)) {
        return { ok: false, error: "Mot de passe incorrect." };
      }
      s.session = true;
      Store.write(s);
      return { ok: true };
    },

    logout: function () {
      var s = Account.state();
      s.session = false;
      Store.write(s);
    },

    submitApplication: function (answers, score) {
      var s = Account.state();
      var now = new Date();
      s.application = {
        status: "review",
        ref: uid("CAND"),
        score: score,
        answers: answers,
        submittedAt: now.toISOString(),
        decisionAt: new Date(now.getTime() + CONFIG.reviewDelayMs).toISOString()
      };
      return Store.write(s);
    },

    resetApplication: function () {
      var s = Account.state();
      s.application = { status: "none" };
      return Store.write(s);
    },

    activate: function (method) {
      var s = Account.state();
      s.activation = {
        paid: true,
        method: method || "card",
        amount: CONFIG.activationFee,
        ref: uid("ACT"),
        paidAt: new Date().toISOString()
      };
      if (!s.wallet.history.length) {
        s.wallet.credits += CONFIG.welcomeCredits;
        s.wallet.history.unshift({
          date: new Date().toISOString(),
          label: "Crédits de bienvenue",
          credits: CONFIG.welcomeCredits
        });
      }
      return Store.write(s);
    },

    creditTask: function (task, credits) {
      var s = Account.state();
      s.wallet.credits += credits;
      s.wallet.history.unshift({
        date: new Date().toISOString(),
        label: "Mission validée — " + task.title,
        credits: credits
      });
      s.tasks.done[task.id] = (s.tasks.done[task.id] || 0) + 1;
      s.tasks.log.unshift({ id: task.id, title: task.title, date: new Date().toISOString(), credits: credits });
      s.tasks.log = s.tasks.log.slice(0, 40);
      return Store.write(s);
    },

    requestPayout: function (credits, method) {
      var s = Account.state();
      if (credits > s.wallet.credits) return { ok: false, error: "Solde insuffisant." };
      s.wallet.credits -= credits;
      s.wallet.history.unshift({
        date: new Date().toISOString(),
        label: "Demande de retrait (" + method + ")",
        credits: -credits
      });
      Store.write(s);
      return { ok: true };
    },

    /* Étape logique courante du parcours membre. */
    stage: function () {
      var s = Account.state();
      if (!s.user) return "guest";
      if (s.application.status === "none") return "to-apply";
      if (s.application.status === "review") return "review";
      if (s.application.status === "rejected") return "rejected";
      if (!s.activation.paid) return "to-activate";
      return "active";
    }
  };

  /* -------------------------------------------------------------- Interface */

  function toast(message, kind) {
    var zone = qs(".toast-zone");
    if (!zone) {
      zone = document.createElement("div");
      zone.className = "toast-zone";
      document.body.appendChild(zone);
    }
    var el = document.createElement("div");
    el.className = "toast" + (kind ? " toast-" + kind : "");
    el.setAttribute("role", "status");
    el.textContent = message;
    zone.appendChild(el);
    setTimeout(function () {
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 250);
    }, 3600);
  }

  /* Menu mobile */
  function initNav() {
    var header = qs(".site-header");
    var toggle = qs(".nav-toggle");
    if (!header || !toggle) return;
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* Le bandeau de navigation s'adapte à l'état de connexion. */
  function initAuthNav() {
    var logged = Account.isLogged();
    qsa("[data-when]").forEach(function (el) {
      var want = el.getAttribute("data-when");
      var show = (want === "logged") ? logged : !logged;
      el.classList.toggle("hide", !show);
    });
    qsa("[data-action='logout']").forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        Account.logout();
        window.location.href = "connexion.html";
      });
    });
    var name = qs("[data-user-name]");
    if (name) {
      var s = Account.state();
      if (s.user) name.textContent = s.user.prenom;
    }
  }

  /* Accordéons FAQ */
  function initFaq() {
    qsa(".faq-q").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var open = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", open ? "false" : "true");
      });
    });
  }

  /* Mise en évidence visuelle des cases cochées */
  function initChoices() {
    qsa(".choice input").forEach(function (input) {
      var sync = function () {
        var group = input.name
          ? qsa('input[name="' + input.name + '"]')
          : [input];
        group.forEach(function (i) {
          var box = i.closest(".choice");
          if (box) box.classList.toggle("is-picked", i.checked);
        });
      };
      input.addEventListener("change", sync);
      sync();
    });
  }

  /* Compteurs animés du bandeau de chiffres */
  function initCounters() {
    var els = qsa("[data-count]");
    if (!els.length || !("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        io.unobserve(el);
        var target = parseFloat(el.getAttribute("data-count"));
        var suffix = el.getAttribute("data-suffix") || "";
        var decimals = (el.getAttribute("data-decimals") | 0);
        var start = performance.now(), dur = 1100;
        function tick(now) {
          var p = Math.min(1, (now - start) / dur);
          var eased = 1 - Math.pow(1 - p, 3);
          var v = target * eased;
          el.textContent = v.toLocaleString("fr-FR", {
            minimumFractionDigits: decimals, maximumFractionDigits: decimals
          }) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    }, { threshold: .4 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* Protection des pages de l'espace membre.
     data-guard="member" | "accepted" | "active" */
  function initGuard() {
    var guard = document.body.getAttribute("data-guard");
    if (!guard) return;
    var stage = Account.stage();

    if (stage === "guest") {
      window.location.replace("connexion.html?next=" + encodeURIComponent(location.pathname.split("/").pop()));
      return;
    }
    if (guard === "member") return;

    if (guard === "accepted") {
      // Page d'activation : réservée aux candidatures acceptées.
      if (stage === "to-apply" || stage === "review" || stage === "rejected") {
        window.location.replace("compte.html");
      }
      return;
    }
    if (guard === "active" && stage !== "active") {
      window.location.replace(stage === "to-activate" ? "activation.html" : "compte.html");
    }
  }

  /* Année courante dans le pied de page */
  function initYear() {
    qsa("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initGuard();
    initNav();
    initAuthNav();
    initFaq();
    initChoices();
    initCounters();
    initYear();
  });

  /* Exposition publique */
  window.Tacheo = {
    CONFIG: CONFIG,
    Store: Store,
    Account: Account,
    toast: toast,
    euros: euros,
    creditsToEuros: creditsToEuros,
    formatDate: formatDate,
    escapeHtml: escapeHtml,
    uid: uid,
    qs: qs,
    qsa: qsa
  };
})();
