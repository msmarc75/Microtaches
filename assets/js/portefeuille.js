/* Portefeuille : solde, historique des opérations et demande de retrait. */
(function () {
  "use strict";

  var T = window.Tacheo;
  var historyBox = document.getElementById("history");
  if (!historyBox) return;

  var form = document.getElementById("payout-form");
  var errorBox = document.getElementById("payout-error");

  function render() {
    var s = T.Account.state();
    var earned = s.wallet.history.reduce(function (a, h) { return a + (h.credits > 0 ? h.credits : 0); }, 0);

    document.getElementById("kpi-credits").textContent = s.wallet.credits.toLocaleString("fr-FR") + " cr";
    document.getElementById("kpi-euros").textContent = T.creditsToEuros(s.wallet.credits);
    document.getElementById("kpi-total").textContent = earned.toLocaleString("fr-FR") + " cr";
    document.getElementById("kpi-tasks").textContent = s.tasks.log.length;

    if (!s.wallet.history.length) {
      historyBox.innerHTML = '<p class="muted mb-0">Aucune opération pour le moment. ' +
        'Traitez un <a href="taches.html">premier lot</a> pour créditer votre portefeuille.</p>';
      return;
    }

    historyBox.innerHTML = '<table class="table"><thead><tr><th>Date</th><th>Opération</th>' +
      '<th class="num">Crédits</th></tr></thead><tbody>' +
      s.wallet.history.map(function (h) {
        var sign = h.credits > 0 ? "+" : "";
        var color = h.credits > 0 ? "var(--green)" : "var(--red)";
        return "<tr><td>" + T.formatDate(h.date, true) + "</td><td>" + T.escapeHtml(h.label) +
          '</td><td class="num" style="color:' + color + ';font-weight:700">' +
          sign + h.credits.toLocaleString("fr-FR") + "</td></tr>";
      }).join("") + "</tbody></table>";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    errorBox.classList.add("hide");

    var amount = parseInt(document.getElementById("amount").value, 10);
    var method = document.getElementById("method").value;
    var s = T.Account.state();

    if (!amount || amount < T.CONFIG.payoutThreshold) {
      errorBox.textContent = "Le montant minimal de retrait est de " +
        T.CONFIG.payoutThreshold.toLocaleString("fr-FR") + " crédits.";
      errorBox.classList.remove("hide");
      return;
    }
    if (amount > s.wallet.credits) {
      errorBox.textContent = "Votre solde ne permet pas ce retrait (disponible : " +
        s.wallet.credits.toLocaleString("fr-FR") + " crédits).";
      errorBox.classList.remove("hide");
      return;
    }

    var result = T.Account.requestPayout(amount, method);
    if (!result.ok) {
      errorBox.textContent = result.error;
      errorBox.classList.remove("hide");
      return;
    }
    form.reset();
    render();
    T.toast("Demande de retrait enregistrée. Versement sous 2 à 5 jours ouvrés.", "ok");
  });

  render();
})();
