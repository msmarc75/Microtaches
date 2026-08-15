/* Formulaire de contact : contrôles de saisie et accusé de réception simulé. */
(function () {
  "use strict";

  var T = window.Tacheo;
  var form = document.getElementById("contact-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    var fields = ["cnom", "cmail", "csujet", "cmsg"].map(function (id) { return document.getElementById(id); });
    var ok = true;

    fields.forEach(function (field) {
      var holder = field.closest(".field");
      var old = holder.querySelector(".error-text");
      if (old) old.remove();
      field.classList.remove("input-error");

      var value = field.value.trim();
      var tooShort = field.minLength > 0 && value.length < field.minLength;
      var badMail = field.type === "email" && value && !/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(value);

      if (!value || tooShort || badMail) {
        ok = false;
        field.classList.add("input-error");
        var p = document.createElement("p");
        p.className = "error-text";
        p.textContent = badMail ? "Adresse e-mail invalide."
          : tooShort ? "Merci de détailler votre demande (20 caractères minimum)."
          : "Ce champ est obligatoire.";
        holder.appendChild(p);
      }
    });

    if (!ok) return;

    form.innerHTML = '<div class="alert alert-green"><span class="alert-ico">✓</span>' +
      "<p class=\"mb-0\"><strong>Message enregistré.</strong> Le support revient vers vous sous un jour " +
      "ouvré à l'adresse indiquée. (Démonstration : aucun message n'est réellement envoyé.)</p></div>";
    T.toast("Message enregistré.", "ok");
  });
})();
