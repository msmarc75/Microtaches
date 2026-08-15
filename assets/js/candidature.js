/* Formulaire de candidature en quatre étapes : navigation, contrôles de
   saisie, notation du test de consignes et envoi du dossier. */
(function () {
  "use strict";

  var T = window.Tacheo;
  var form = document.getElementById("apply-form");
  if (!form) return;

  var steps = T.qsa(".form-step", form);
  var stepper = T.qsa(".stepper-item");
  var current = 0;

  /* Index de la bonne réponse pour chacune des cinq questions. */
  var ANSWERS = [0, 1, 1, 1, 1];

  function show(index) {
    current = Math.max(0, Math.min(steps.length - 1, index));
    steps.forEach(function (s, i) { s.classList.toggle("is-active", i === current); });
    stepper.forEach(function (item, i) {
      item.classList.toggle("is-done", i < current);
      item.classList.toggle("is-current", i === current);
    });
    if (current === steps.length - 1) buildRecap();
    window.scrollTo({ top: form.getBoundingClientRect().top + window.scrollY - 110, behavior: "smooth" });
  }

  function setError(field, message) {
    clearError(field);
    field.classList.add("input-error");
    var p = document.createElement("p");
    p.className = "error-text";
    p.textContent = message;
    (field.closest(".field") || field.parentNode).appendChild(p);
  }

  function clearError(field) {
    field.classList.remove("input-error");
    var holder = field.closest(".field") || field.parentNode;
    var old = holder.querySelector(".error-text");
    if (old) old.remove();
  }

  function validateStep(index) {
    var scope = steps[index];
    var ok = true;
    var firstBad = null;

    /* Champs texte, e-mail, date, mot de passe, listes et zones de texte */
    T.qsa("input[required], select[required], textarea[required]", scope).forEach(function (field) {
      if (field.type === "radio" || field.type === "checkbox") return;
      clearError(field);
      var value = field.value.trim();
      if (!value) {
        setError(field, "Ce champ est obligatoire.");
        ok = false; firstBad = firstBad || field;
        return;
      }
      if (field.type === "email" && !/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(value)) {
        setError(field, "Adresse e-mail invalide.");
        ok = false; firstBad = firstBad || field;
      }
      if (field.minLength > 0 && value.length < field.minLength) {
        setError(field, "Merci de détailler un peu plus (" + field.minLength + " caractères minimum).");
        ok = false; firstBad = firstBad || field;
      }
    });

    /* Groupes de boutons radio et cases à cocher obligatoires */
    var seen = {};
    T.qsa("input[type=radio][required], input[type=checkbox][required]", scope).forEach(function (input) {
      if (seen[input.name]) return;
      seen[input.name] = true;
      var group = T.qsa('input[name="' + input.name + '"]', scope);
      var checked = group.some(function (i) { return i.checked; });
      var holder = input.closest("fieldset") || input.closest(".field");
      if (holder) {
        var old = holder.querySelector(".error-text");
        if (old) old.remove();
      }
      if (!checked) {
        ok = false;
        firstBad = firstBad || input;
        if (holder) {
          var p = document.createElement("p");
          p.className = "error-text";
          p.textContent = "Merci de répondre à ce point.";
          holder.appendChild(p);
        }
      }
    });

    /* Contrôles propres à la première étape */
    if (index === 0) {
      var pass = document.getElementById("password");
      var pass2 = document.getElementById("password2");
      if (pass.value && pass.value.length < 8) {
        setError(pass, "Huit caractères minimum.");
        ok = false; firstBad = firstBad || pass;
      }
      if (pass.value && pass2.value && pass.value !== pass2.value) {
        setError(pass2, "Les deux mots de passe ne correspondent pas.");
        ok = false; firstBad = firstBad || pass2;
      }
      var birth = document.getElementById("naissance");
      if (birth.value) {
        var age = (Date.now() - new Date(birth.value).getTime()) / (365.25 * 24 * 3600 * 1000);
        if (age < 18) {
          setError(birth, "La plateforme est réservée aux personnes majeures.");
          ok = false; firstBad = firstBad || birth;
        }
      }
    }

    if (!ok && firstBad) {
      firstBad.focus({ preventScroll: true });
      firstBad.scrollIntoView({ block: "center", behavior: "smooth" });
    }
    return ok;
  }

  function checkedValues(name) {
    return T.qsa('input[name="' + name + '"]:checked').map(function (i) { return i.value; });
  }

  function buildRecap() {
    var get = function (id) { return (document.getElementById(id) || {}).value || "—"; };
    var picked = checkedValues("situation")[0] || "—";
    var interets = checkedValues("interets");
    var equip = checkedValues("equip");
    var rows = [
      ["Nom et prénom", T.escapeHtml(get("prenom") + " " + get("nom"))],
      ["Adresse e-mail", T.escapeHtml(get("email"))],
      ["Pays de résidence", T.escapeHtml(get("pays"))],
      ["Situation", T.escapeHtml(picked)],
      ["Disponibilité", T.escapeHtml(get("dispo"))],
      ["Équipement", T.escapeHtml(equip.join(", ") || "Non précisé")],
      ["Missions visées", T.escapeHtml(interets.join(", ") || "Non précisé")]
    ];
    document.getElementById("recap").innerHTML =
      '<table class="table">' + rows.map(function (r) {
        return "<tr><th>" + r[0] + "</th><td>" + r[1] + "</td></tr>";
      }).join("") + "</table>";
  }

  function score() {
    var total = 0;
    ANSWERS.forEach(function (good, i) {
      var picked = document.querySelector('input[name="q' + i + '"]:checked');
      if (picked && parseInt(picked.value, 10) === good) total++;
    });
    return total;
  }

  T.qsa("[data-next]", form).forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (validateStep(current)) show(current + 1);
    });
  });
  T.qsa("[data-prev]", form).forEach(function (btn) {
    btn.addEventListener("click", function () { show(current - 1); });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!validateStep(current)) return;

    var answers = {
      situation: checkedValues("situation")[0] || "",
      dispo: document.getElementById("dispo").value,
      equipement: checkedValues("equip"),
      interets: checkedValues("interets"),
      motivation: document.getElementById("motivation").value.trim(),
      naissance: document.getElementById("naissance").value
    };

    T.Account.register({
      prenom: document.getElementById("prenom").value.trim(),
      nom: document.getElementById("nom").value.trim(),
      email: document.getElementById("email").value.trim(),
      pays: document.getElementById("pays").value,
      password: document.getElementById("password").value
    });
    T.Account.submitApplication(answers, score());

    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = "Envoi en cours…";
    T.toast("Candidature envoyée. Vous allez être redirigé.", "ok");
    setTimeout(function () { window.location.href = "compte.html"; }, 900);
  });
})();
