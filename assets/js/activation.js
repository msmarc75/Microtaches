/* Page d'activation : contrôle du formulaire de règlement puis enregistrement
   de l'activation. Le paiement est simulé — aucun appel à un prestataire n'est
   effectué. Pour brancher un vrai encaissement, remplacer processPayment().  */
(function () {
  "use strict";

  var T = window.Tacheo;
  var form = document.getElementById("pay-form");
  if (!form) return;

  var cardFields = document.getElementById("card-fields");
  var sepaFields = document.getElementById("sepa-fields");
  var errorBox = document.getElementById("pay-error");
  var button = document.getElementById("pay-btn");
  var num = document.getElementById("cardnum");
  var exp = document.getElementById("cardexp");

  /* Bascule carte / prélèvement SEPA */
  T.qsa('input[name="method"]').forEach(function (input) {
    input.addEventListener("change", function () {
      var card = input.value === "card";
      cardFields.classList.toggle("hide", !card);
      sepaFields.classList.toggle("hide", card);
      T.qsa("input", cardFields).forEach(function (i) { i.required = card; });
    });
  });

  /* Confort de saisie : groupes de quatre chiffres et format MM/AA */
  num.addEventListener("input", function () {
    var digits = num.value.replace(/\D/g, "").slice(0, 19);
    num.value = digits.replace(/(.{4})/g, "$1 ").trim();
  });
  exp.addEventListener("input", function () {
    var digits = exp.value.replace(/\D/g, "").slice(0, 4);
    exp.value = digits.length > 2 ? digits.slice(0, 2) + "/" + digits.slice(2) : digits;
  });

  function fail(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("hide");
    errorBox.scrollIntoView({ block: "center", behavior: "smooth" });
    return false;
  }

  function validate() {
    errorBox.classList.add("hide");
    if (!form.querySelector('input[name="cgv"]').checked) {
      return fail("Vous devez accepter les conditions générales de vente pour continuer.");
    }
    var method = form.querySelector('input[name="method"]:checked').value;

    if (method === "sepa") {
      var iban = document.getElementById("iban").value.replace(/\s/g, "");
      if (iban.length < 15) return fail("Merci de saisir un IBAN valide.");
      return true;
    }
    if (!document.getElementById("cardname").value.trim()) {
      return fail("Le nom du titulaire est obligatoire.");
    }
    var digits = num.value.replace(/\D/g, "");
    if (digits.length < 13) return fail("Le numéro de carte est incomplet.");
    if (!/^\d{2}\/\d{2}$/.test(exp.value)) return fail("La date d'expiration doit être au format MM/AA.");
    var mm = parseInt(exp.value.slice(0, 2), 10);
    if (mm < 1 || mm > 12) return fail("Le mois d'expiration est invalide.");
    var yy = parseInt(exp.value.slice(3), 10) + 2000;
    var now = new Date();
    if (yy < now.getFullYear() || (yy === now.getFullYear() && mm < now.getMonth() + 1)) {
      return fail("La carte est expirée.");
    }
    if (!/^\d{3,4}$/.test(document.getElementById("cardcvc").value)) {
      return fail("Le cryptogramme comporte trois ou quatre chiffres.");
    }
    return true;
  }

  /* Point d'accroche pour un vrai prestataire de paiement.
     Exemple : rediriger vers une session Stripe Checkout créée côté serveur,
     puis appeler T.Account.activate() au retour, après vérification du webhook. */
  function processPayment(method) {
    return new Promise(function (resolve) {
      setTimeout(function () { resolve({ ok: true, method: method }); }, 1400);
    });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!validate()) return;

    var method = form.querySelector('input[name="method"]:checked').value;
    button.disabled = true;
    button.textContent = "Traitement du paiement…";

    processPayment(method).then(function (result) {
      if (!result.ok) {
        button.disabled = false;
        button.textContent = "Payer 20,00 € et activer mon compte";
        fail("Le paiement a été refusé. Vérifiez vos informations ou changez de moyen de paiement.");
        return;
      }
      T.Account.activate(method);
      button.textContent = "Compte activé ✓";
      T.toast("Compte activé. 150 crédits de bienvenue ont été versés.", "ok");
      setTimeout(function () { window.location.href = "taches.html"; }, 900);
    });
  });
})();
