/* Connexion à l'espace membre (démonstration : le compte est celui enregistré
   dans ce navigateur lors de la candidature). */
(function () {
  "use strict";

  var T = window.Tacheo;
  var form = document.getElementById("login-form");
  if (!form) return;
  var box = document.getElementById("login-error");

  /* Déjà connecté : inutile de repasser par le formulaire. */
  if (T.Account.isLogged()) {
    window.location.replace("compte.html");
    return;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    box.classList.add("hide");

    var email = document.getElementById("email").value.trim();
    var password = document.getElementById("password").value;
    if (!email || !password) {
      box.textContent = "Merci de renseigner votre e-mail et votre mot de passe.";
      box.classList.remove("hide");
      return;
    }

    var result = T.Account.login(email, password);
    if (!result.ok) {
      box.innerHTML = T.escapeHtml(result.error) +
        ' <a href="inscription.html">Déposer une candidature</a>';
      box.classList.remove("hide");
      return;
    }

    var next = new URLSearchParams(window.location.search).get("next");
    window.location.href = (next && /^[a-z0-9\-]+\.html$/i.test(next)) ? next : "compte.html";
  });
})();
