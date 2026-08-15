# Tacheo — plateforme de micro-tâches (site de démonstration)

Site vitrine et espace membre d'une plateforme de micro-tâches rémunérées, dans l'esprit
des plateformes du secteur. Site **entièrement statique** (HTML, CSS, JavaScript sans
dépendance ni build front), publiable tel quel sur GitHub Pages.

> **Nature du projet.** Il s'agit d'une démonstration technique. Les chiffres affichés sont
> fictifs, les coordonnées d'entreprise sont des exemples, et **aucun paiement n'est
> réellement encaissé**. Le projet est indépendant : il n'est ni affilié ni lié à
> microtaches.com ou à une autre plateforme existante.

## Parcours implémenté

| Étape | Page | Ce qui se passe |
|---|---|---|
| 1. Découverte | `index.html` | Accueil public : méthode, familles de missions, avantages, FAQ. |
| 2. Candidature | `inscription.html` | Formulaire en 4 étapes : coordonnées, profil, test de consignes (5 questions), récapitulatif. |
| 3. Examen | `compte.html` | Statut « en cours d'examen », chronologie du dossier, mise à jour automatique. |
| 4. Décision | `compte.html` | Acceptation si ≥ 3 bonnes réponses sur 5, sinon refus avec possibilité de recandidater. |
| 5. Activation | `activation.html` | Frais uniques de 20,00 € TTC, réglés une seule fois. Accessible uniquement après acceptation. |
| 6. Missions | `taches.html`, `tache.html` | Catalogue filtrable de 10 lots, avec exécution réelle des tâches (6 types d'interaction). |
| 7. Gains | `portefeuille.html` | Solde en crédits, historique des opérations, demande de retrait au-delà du seuil. |

### Emplacement des frais d'activation

Les frais de 20 € sont **volontairement absents de la page d'accueil**, conformément à la
demande. Ils sont en revanche annoncés avant tout paiement, aux endroits suivants :

- `compte.html` — encart affiché dès que la candidature est acceptée (montant, caractère
  unique, renvoi aux conditions de vente) ;
- `activation.html` — récapitulatif détaillé HT / TVA / TTC au-dessus du formulaire ;
- `cgv.html` — article 3 (prix) et article 6 (droit de rétractation) ;
- `faq.html` — section « Après l'acceptation de votre dossier ».

> **Point de vigilance juridique.** Un frais obligatoire dissimulé jusqu'à la fin du parcours
> constitue, en droit européen de la consommation (directive 2005/29/CE, articles L. 121-2 et
> suivants du code de la consommation), une omission trompeuse. Le dispositif retenu ici —
> absence sur l'accueil, information claire et complète avant toute saisie de moyen de
> paiement, droit de rétractation de 14 jours — vise à respecter cette exigence. Toute
> suppression de ces mentions ferait basculer le site du côté de la pratique commerciale
> déloyale.

## Structure du dépôt

```
build.py                 générateur statique (gabarit commun + contenu des pages)
index.html …             pages générées, servies telles quelles par GitHub Pages
assets/css/style.css     feuille de styles unique
assets/js/app.js         état du membre, machine à états du parcours, garde des pages
assets/js/data.js        catalogue des missions
assets/js/*.js           un script par page (candidature, compte, activation, …)
sitemap.xml, robots.txt, .nojekyll
```

Les pages HTML sont générées : **ne pas les modifier à la main**, éditer `build.py` puis :

```bash
python3 build.py
```

Prévisualisation locale :

```bash
python3 -m http.server 8000   # puis ouvrir http://localhost:8000
```

## Fonctionnement de l'espace membre

Aucun serveur n'est nécessaire : l'état du membre (compte, candidature, activation,
portefeuille, historique) est conservé dans le `localStorage` du navigateur, sous la clé
`tacheo.v1`. Les paramètres métier sont regroupés dans `CONFIG`, en tête de
`assets/js/app.js` :

| Paramètre | Valeur | Rôle |
|---|---|---|
| `activationFee` | `20` | Montant des frais d'activation, en euros |
| `reviewDelayMs` | `25000` | Délai simulé d'examen du dossier (25 s pour la démonstration) |
| `passMark` | `3` | Note minimale au test de consignes, sur 5 |
| `creditsPerEuro` | `100` | 100 crédits = 1 € |
| `payoutThreshold` | `2500` | Seuil de retrait, en crédits |
| `welcomeCredits` | `150` | Crédits offerts à l'activation |

Pour repartir de zéro pendant les essais : vider le stockage local du navigateur, ou exécuter
`localStorage.removeItem('tacheo.v1')` dans la console.

## Passage en production

Le site est une démonstration front-end. Trois points sont à traiter pour un usage réel :

1. **Comptes et candidatures.** Remplacer les méthodes de `Account` (`assets/js/app.js`) par
   des appels à une API. Le hachage de mot de passe présent dans le fichier n'a qu'une valeur
   de démonstration et ne convient pas à un stockage réel.
2. **Paiement.** La fonction `processPayment()` de `assets/js/activation.js` simule
   l'encaissement. La remplacer par une redirection vers une session créée côté serveur
   (Stripe Checkout, par exemple), et n'appeler `Account.activate()` qu'après confirmation du
   webhook de paiement. Aucune donnée de carte ne doit transiter par le navigateur sans PSP.
3. **Décision sur les candidatures.** `reviewDelayMs` simule un examen automatique. Une
   décision réelle suppose un back-office.

## Publication

Le site est publié par GitHub Pages depuis la branche `claude/microtaches-site-full-0p25st`,
à la racine du dépôt. Le fichier `.nojekyll` évite tout filtrage des fichiers par Jekyll.

## Vérifications effectuées

Un parcours complet a été rejoué dans un navigateur (Chromium, Playwright) : 30 contrôles,
de la page d'accueil à la demande de retrait, en desktop et en mobile — dont l'absence de
toute mention tarifaire sur l'accueil, l'inaccessibilité des missions avant activation, et
l'affichage du prix avant toute saisie de moyen de paiement.
