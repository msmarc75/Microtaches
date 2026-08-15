#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur statique du site Tacheo.

Assemble les pages HTML à partir d'un gabarit commun (en-tête, navigation,
pied de page) et du contenu propre à chaque page. Le résultat est écrit à la
racine du dépôt pour être servi tel quel par GitHub Pages.

Usage :  python3 build.py
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

SITE = "Tacheo"
BASE_URL = "https://msmarc75.github.io/Microtaches"
TAGLINE = "Les petites tâches, faites en grand."

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='8' fill='%235b3df5'/%3E"
    "%3Ctext x='16' y='22' font-family='Arial,sans-serif' font-size='17' "
    "font-weight='bold' fill='white' text-anchor='middle'%3ET%3C/text%3E%3C/svg%3E"
)

NAV_ITEMS = [
    ("index.html#methode", "Comment ça marche", "methode"),
    ("missions.html", "Types de missions", "missions"),
    ("index.html#avantages", "Avantages", "avantages"),
    ("faq.html", "FAQ", "faq"),
]


def header(active):
    links = []
    for href, label, key in NAV_ITEMS:
        cls = ' class="is-active"' if key == active else ""
        links.append('<a href="%s"%s>%s</a>' % (href, cls, label))
    return """<a class="skip-link" href="#main">Aller au contenu</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html">
      <span class="brand-mark" aria-hidden="true">T</span>
      <span>Tacheo</span>
    </a>
    <button class="nav-toggle" type="button" aria-label="Ouvrir le menu" aria-expanded="false"><span></span></button>
    <nav class="nav-links" aria-label="Navigation principale">
      %s
    </nav>
    <div class="nav-right">
      <a class="btn btn-quiet hide" data-when="guest" href="connexion.html">Connexion</a>
      <a class="btn btn-primary hide" data-when="guest" href="inscription.html">Déposer ma candidature</a>
      <a class="btn btn-ghost hide" data-when="logged" href="compte.html">Mon espace</a>
      <a class="btn btn-quiet hide" data-when="logged" href="#" data-action="logout">Déconnexion</a>
    </div>
  </div>
</header>""" % ("\n      ".join(links))


FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html">
          <span class="brand-mark" aria-hidden="true">T</span><span>Tacheo</span>
        </a>
        <p class="small mt-2">Plateforme de micro-tâches rémunérées en français. Des missions courtes,
        des consignes claires, des paiements suivis.</p>
      </div>
      <div>
        <h4>Plateforme</h4>
        <ul class="footer-list">
          <li><a href="index.html#methode">Comment ça marche</a></li>
          <li><a href="missions.html">Types de missions</a></li>
          <li><a href="index.html#avantages">Avantages</a></li>
          <li><a href="faq.html">Questions fréquentes</a></li>
        </ul>
      </div>
      <div>
        <h4>Compte</h4>
        <ul class="footer-list">
          <li><a href="inscription.html">Déposer une candidature</a></li>
          <li><a href="connexion.html">Se connecter</a></li>
          <li><a href="compte.html">Mon espace</a></li>
          <li><a href="contact.html">Nous écrire</a></li>
        </ul>
      </div>
      <div>
        <h4>Informations légales</h4>
        <ul class="footer-list">
          <li><a href="cgu.html">Conditions d'utilisation</a></li>
          <li><a href="cgv.html">Conditions de vente</a></li>
          <li><a href="confidentialite.html">Confidentialité</a></li>
          <li><a href="mentions-legales.html">Mentions légales</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Tacheo — Tous droits réservés.</span>
      <span>Projet de démonstration, sans lien avec microtaches.com. Aucun paiement réel n'est encaissé.</span>
    </div>
  </div>
</footer>"""


def layout(filename, title, description, body, active="", guard=None, scripts=(), body_class=""):
    """Assemble une page complète et l'écrit sur le disque."""
    attrs = []
    if guard:
        attrs.append('data-guard="%s"' % guard)
    if body_class:
        attrs.append('class="%s"' % body_class)
    body_attr = (" " + " ".join(attrs)) if attrs else ""

    extra = "\n".join('<script src="assets/js/%s"></script>' % s for s in scripts)

    html = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="theme-color" content="#5b3df5">
<link rel="canonical" href="%(base)s/%(file)s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%(site)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(base)s/%(file)s">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="%(favicon)s">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
<!-- Police chargée sans bloquer le rendu : en cas d'indisponibilité, la pile
     système déclarée dans la feuille de styles prend le relais. -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap"
      media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap"></noscript>
</head>
<body%(bodyattr)s>
%(header)s
<main id="main">
%(body)s
</main>
%(footer)s
<script src="assets/js/app.js"></script>
%(extra)s
</body>
</html>
""" % {
        "title": title,
        "desc": description,
        "base": BASE_URL,
        "file": filename,
        "site": SITE,
        "favicon": FAVICON,
        "bodyattr": body_attr,
        "header": header(active),
        "body": body,
        "footer": FOOTER,
        "extra": extra,
    }

    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as fh:
        fh.write(html)
    return filename


# ===========================================================================
#  Fragments réutilisables
# ===========================================================================

def cta_band(title, text, button_label="Déposer ma candidature", button_href="inscription.html"):
    return """<section>
  <div class="wrap">
    <div class="cta-band">
      <h2>%s</h2>
      <p>%s</p>
      <div class="btn-row" style="justify-content:center;margin-top:22px">
        <a class="btn btn-lg btn-green" href="%s">%s</a>
        <a class="btn btn-lg btn-ghost" href="faq.html">Lire la FAQ</a>
      </div>
    </div>
  </div>
</section>""" % (title, text, button_href, button_label)


def faq_block(items):
    out = []
    for i, (q, a) in enumerate(items):
        out.append("""<div class="faq-item">
  <button class="faq-q" type="button" aria-expanded="%s">%s</button>
  <div class="faq-a"><p>%s</p></div>
</div>""" % ("true" if i == 0 else "false", q, a))
    return "\n".join(out)


def app_tabs(active):
    tabs = [
        ("compte.html", "Tableau de bord", "compte"),
        ("taches.html", "Missions disponibles", "taches"),
        ("portefeuille.html", "Portefeuille", "portefeuille"),
    ]
    out = []
    for href, label, key in tabs:
        cls = ' class="is-active"' if key == active else ""
        out.append('<a href="%s"%s>%s</a>' % (href, cls, label))
    return '<nav class="app-tabs" aria-label="Espace membre">%s</nav>' % "".join(out)


# ===========================================================================
#  Page d'accueil
#  IMPORTANT : aucune mention des frais d'activation sur cette page.
# ===========================================================================

MISSION_TYPES = [
    ("🖼️", "Classification d'images", "Trier et étiqueter des visuels qui servent à entraîner des modèles de reconnaissance."),
    ("🧾", "Saisie de données", "Reporter des informations depuis des documents numérisés vers des formulaires structurés."),
    ("🎧", "Transcription audio", "Retranscrire des extraits sonores courts, en français, avec une ponctuation soignée."),
    ("🔎", "Vérification d'informations", "Comparer deux sources et confirmer, ou non, qu'elles décrivent la même réalité."),
    ("📱", "Test d'applications", "Dérouler un scénario dans une application en préversion et remonter les anomalies."),
    ("🛡️", "Modération de contenus", "Appliquer une charte éditoriale à des avis et commentaires publiés en ligne."),
    ("📊", "Sondages courts", "Répondre à des questionnaires d'instituts d'études, en quelques minutes."),
    ("🌐", "Recherche web", "Retrouver une information factuelle sur une source officielle et la reporter."),
]

ADVANTAGES = [
    ("⏱️", "Des missions courtes", "La plupart des lots se traitent en trois à quinze minutes. Vous vous arrêtez quand vous voulez, sans engagement de volume."),
    ("📖", "Des consignes explicites", "Chaque mission s'ouvre sur un cadre de travail détaillé. Vous savez ce qui est attendu avant de commencer, pas après."),
    ("🇫🇷", "Une plateforme en français", "Interface, consignes et support entièrement francophones. Pas de traduction approximative sur des règles qui comptent."),
    ("🔐", "Vos données protégées", "Traitement conforme au RGPD, hébergement dans l'Union européenne, aucune revente de vos informations personnelles."),
    ("📈", "Une progression lisible", "Un taux de qualité, un historique de missions, des niveaux : votre travail est mesuré sur des critères connus d'avance."),
    ("💶", "Des retraits suivis", "Virement SEPA ou portefeuille électronique, avec un récapitulatif détaillé de chaque opération dans votre espace."),
]

USE_CASES = [
    ("🎓", "Étudiants", "Quelques créneaux entre deux cours, sans contrainte d'horaire ni de lieu."),
    ("🏠", "Parents au foyer", "Des sessions courtes qui s'intercalent dans une journée déjà bien remplie."),
    ("💼", "Indépendants", "Un complément d'activité pour lisser les périodes creuses entre deux missions."),
    ("🌍", "Expatriés", "Une activité qui suit le fuseau horaire de celui qui la pratique, pas l'inverse."),
]

TESTIMONIALS = [
    ("Camille R.", "Rennes", "Je fais deux ou trois lots le soir, surtout de la classification d'images. Les consignes sont claires et je sais à quoi m'attendre avant de me lancer."),
    ("Yassine B.", "Bruxelles", "Ce qui m'a décidé, c'est l'historique détaillé : je vois exactement ce qui a été validé, ce qui a été rejeté et pourquoi."),
    ("Nathalie D.", "Toulouse", "La transcription demande de la concentration, mais les extraits sont courts. C'est parfait entre deux rendez-vous."),
]

HOME_FAQ = [
    ("Qui peut déposer une candidature ?",
     "Toute personne majeure disposant d'une connexion internet et d'un compte bancaire ou d'un portefeuille électronique à son nom. Aucun diplôme n'est exigé."),
    ("Combien de temps prend l'examen du dossier ?",
     "Les candidatures sont étudiées sous 24 à 48 heures ouvrées. Vous recevez la décision par e-mail et dans votre espace membre."),
    ("Le dépôt de candidature est-il gratuit ?",
     "Oui, déposer une candidature ne coûte rien et ne vous engage à rien. Le formulaire prend une dizaine de minutes."),
    ("Combien de temps faut-il consacrer à la plateforme ?",
     "Aucun minimum n'est imposé. Certains membres traitent un lot par semaine, d'autres plusieurs par jour. Vous choisissez vos missions et votre rythme."),
    ("Comment suis-je rémunéré ?",
     "Chaque mission validée crédite votre portefeuille en crédits Tacheo, convertibles en euros. Les retraits se font par virement SEPA ou portefeuille électronique, à partir de 2 500 crédits."),
    ("Puis-je travailler depuis l'étranger ?",
     "Oui, la plateforme est accessible depuis la France, la Belgique, la Suisse, le Luxembourg, le Canada francophone et une partie de l'Afrique francophone."),
]


def build_home():
    types_html = "\n".join(
        """<article class="card card-hover">
  <div class="card-ico">%s</div>
  <h3>%s</h3>
  <p class="small muted">%s</p>
</article>""" % t for t in MISSION_TYPES
    )

    adv_html = "\n".join(
        """<article class="card card-hover">
  <div class="card-ico %s">%s</div>
  <h3>%s</h3>
  <p class="small muted">%s</p>
</article>""" % (["", "ico-green", "ico-amber"][i % 3], a[0], a[1], a[2])
        for i, a in enumerate(ADVANTAGES)
    )

    cases_html = "\n".join(
        """<article class="card card-hover">
  <div class="card-ico ico-green">%s</div>
  <h3>%s</h3>
  <p class="small muted">%s</p>
</article>""" % c for c in USE_CASES
    )

    testi_html = "\n".join(
        """<article class="card quote">
  <div class="stars" aria-label="5 étoiles sur 5">★★★★★</div>
  <p>« %s »</p>
  <div class="quote-author">
    <span class="avatar" aria-hidden="true">%s</span>
    <span><strong>%s</strong><br><span class="tiny muted">%s</span></span>
  </div>
</article>""" % (t[2], t[0][0] + t[0].split(" ")[-1][0], t[0], t[1])
        for t in TESTIMONIALS
    )

    steps = [
        ("Déposez votre candidature", "Un formulaire en quatre étapes : vos coordonnées, votre profil, un court test de compréhension des consignes. Comptez dix minutes."),
        ("Attendez la décision", "Notre équipe examine chaque dossier sous 24 à 48 heures ouvrées. Vous êtes prévenu par e-mail dès qu'elle est rendue."),
        ("Ouvrez votre espace membre", "Une fois le dossier accepté, votre espace vous donne accès aux lots de missions correspondant à votre profil."),
        ("Traitez et encaissez", "Chaque lot validé crédite votre portefeuille. Le retrait se demande en deux clics, dès le seuil atteint."),
    ]
    steps_html = "\n".join(
        """<article class="step">
  <div class="step-num">%d</div>
  <h3>%s</h3>
  <p>%s</p>
</article>""" % (i + 1, s[0], s[1]) for i, s in enumerate(steps)
    )

    body = """<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow"><span class="dot"></span> Candidatures ouvertes — 41 pays</span>
      <h1>Les petites tâches.<br>Faites en grand.</h1>
      <p class="lead">Tacheo réunit des missions courtes confiées par des entreprises : saisie, transcription,
      vérification, classification pour l'intelligence artificielle. Vous les traitez depuis chez vous,
      au rythme que vous choisissez.</p>
      <div class="btn-row mt-3">
        <a class="btn btn-lg btn-primary" href="inscription.html">Déposer ma candidature</a>
        <a class="btn btn-lg btn-ghost" href="missions.html">Voir les types de missions</a>
      </div>
      <ul class="hero-points">
        <li><span class="check">✓</span> Candidature gratuite</li>
        <li><span class="check">✓</span> Sans diplôme ni expérience</li>
        <li><span class="check">✓</span> Réponse sous 24 à 48 h</li>
        <li><span class="check">✓</span> Retraits SEPA</li>
      </ul>
    </div>
    <div>
      <div class="hero-card">
        <div class="hero-card-head">
          <strong>Lots disponibles aujourd'hui</strong>
          <span class="badge badge-green">En direct</span>
        </div>
        <div class="mini-task">
          <span class="mini-ico">🖼️</span>
          <span><strong>Classification d'images</strong><span class="tiny">6 visuels · 4 min</span></span>
          <span class="mini-pay">+42 cr</span>
        </div>
        <div class="mini-task">
          <span class="mini-ico">🎧</span>
          <span><strong>Transcription audio</strong><span class="tiny">3 extraits · 9 min</span></span>
          <span class="mini-pay">+85 cr</span>
        </div>
        <div class="mini-task">
          <span class="mini-ico">🧾</span>
          <span><strong>Saisie de tickets</strong><span class="tiny">3 documents · 7 min</span></span>
          <span class="mini-pay">+68 cr</span>
        </div>
        <div class="float-badge">
          <strong>2 418</strong>
          lots traités cette semaine
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section-tight section-soft">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><b data-count="128400">0</b><span>membres inscrits</span></div>
      <div class="stat"><b data-count="2.3" data-decimals="1" data-suffix=" M">0</b><span>missions validées</span></div>
      <div class="stat"><b data-count="41">0</b><span>pays couverts</span></div>
      <div class="stat"><b data-count="4.6" data-decimals="1" data-suffix="/5">0</b><span>note moyenne des membres</span></div>
    </div>
  </div>
</section>

<section id="methode">
  <div class="wrap">
    <div class="section-head">
      <h2>Comment ça marche</h2>
      <p class="lead">Quatre étapes, aucune zone d'ombre. Vous savez à chaque instant où en est votre dossier.</p>
    </div>
    <div class="grid grid-4 steps">
      %s
    </div>
  </div>
</section>

<section class="section-soft" id="missions">
  <div class="wrap">
    <div class="section-head">
      <h2>Ce que vous ferez concrètement</h2>
      <p class="lead">Huit familles de missions, toutes réalisables depuis un ordinateur ou un téléphone.</p>
    </div>
    <div class="grid grid-4">
      %s
    </div>
    <p class="center mt-3"><a class="btn btn-ghost" href="missions.html">Voir le détail des missions</a></p>
  </div>
</section>

<section id="avantages">
  <div class="wrap">
    <div class="section-head">
      <h2>Pourquoi Tacheo</h2>
      <p class="lead">Une plateforme pensée pour que le travail fourni soit reconnu et mesuré sur des critères connus d'avance.</p>
    </div>
    <div class="grid grid-3">
      %s
    </div>
  </div>
</section>

<section class="section-soft">
  <div class="wrap">
    <div class="section-head">
      <h2>Pour qui</h2>
      <p class="lead">Le point commun de nos membres : du temps disponible par tranches courtes.</p>
    </div>
    <div class="grid grid-4">
      %s
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <h2>Ce qu'en disent les membres</h2>
      <p class="lead">Trois retours parmi les avis déposés dans l'espace membre au cours du dernier trimestre.</p>
    </div>
    <div class="grid grid-3">
      %s
    </div>
  </div>
</section>

<section class="section-soft">
  <div class="wrap wrap-sm">
    <div class="section-head">
      <h2>Questions fréquentes</h2>
      <p class="lead">Les six questions que l'on nous pose le plus souvent avant de candidater.</p>
    </div>
    %s
    <p class="center mt-3"><a class="btn btn-ghost" href="faq.html">Toutes les questions</a></p>
  </div>
</section>

%s
""" % (steps_html, types_html, adv_html, cases_html, testi_html, faq_block(HOME_FAQ),
       cta_band("Prêt à commencer ?",
                "Le dépôt de candidature prend une dizaine de minutes et ne vous engage à rien. "
                "Vous recevez la décision sous 24 à 48 heures ouvrées."))

    return layout(
        "index.html",
        "Tacheo — Micro-tâches rémunérées en français",
        "Tacheo réunit des missions courtes rémunérées : saisie de données, transcription, "
        "vérification, classification d'images. Candidature gratuite, réponse sous 24 à 48 h.",
        body, active="", scripts=(),
    )


# ===========================================================================
#  Page « types de missions »
# ===========================================================================

MISSION_DETAIL = [
    ("🖼️", "Classification d'images", "Intelligence artificielle", "3 à 6 min", "35 à 60 crédits",
     "Vous voyez un visuel, vous lui attribuez la catégorie qui lui correspond. Ces lots alimentent "
     "l'entraînement de modèles de reconnaissance visuelle : commerce, agriculture, sécurité routière.",
     ["Aucune compétence technique requise", "Consignes de deux à trois lignes par catégorie", "Contrôle qualité par recoupement de plusieurs membres"]),
    ("🧾", "Saisie de données", "Saisie", "5 à 12 min", "50 à 90 crédits",
     "Vous reportez dans un formulaire les informations lisibles sur un document numérisé : ticket, "
     "facture, bon de livraison, formulaire manuscrit.",
     ["Rigueur sur les chiffres et les dates", "Recopie fidèle, sans correction de la source", "Champs illisibles signalés, jamais devinés"]),
    ("🎧", "Transcription audio", "Transcription", "8 à 20 min", "80 à 160 crédits",
     "Vous retranscrivez des extraits sonores courts en français : messages vocaux professionnels, "
     "réponses à des enquêtes téléphoniques, annonces.",
     ["Bonne orthographe indispensable", "Extraits de moins de trente secondes", "Passages inaudibles notés [inaudible]"]),
    ("🔎", "Vérification d'informations", "Vérification", "4 à 10 min", "45 à 80 crédits",
     "Vous comparez deux fiches issues de bases différentes et déterminez si elles désignent bien la "
     "même entité : entreprise, produit, adresse.",
     ["Sens du détail", "Règles d'appariement fournies avec le lot", "Aucune recherche externe requise"]),
    ("📱", "Test d'applications", "Test produit", "10 à 25 min", "100 à 200 crédits",
     "Vous déroulez un scénario d'usage dans une application en préversion et vous remontez ce qui "
     "ne fonctionne pas comme annoncé.",
     ["Smartphone récent recommandé", "Scénario fourni étape par étape", "Capture d'écran demandée pour toute anomalie"]),
    ("🛡️", "Modération de contenus", "Modération", "4 à 8 min", "50 à 75 crédits",
     "Vous appliquez la charte d'un site d'avis clients à des commentaires publiés : publication, "
     "masquage ou signalement pour second regard.",
     ["Charte détaillée fournie", "Aucun contenu choquant dans les lots ouverts à tous", "Possibilité de passer un élément"]),
    ("📊", "Sondages courts", "Sondages", "2 à 6 min", "25 à 45 crédits",
     "Vous répondez à des questionnaires d'instituts d'études. Vos réponses sont agrégées de façon "
     "anonyme et ne sont jamais revendues nominativement.",
     ["Aucune bonne ou mauvaise réponse", "Quotas par profil : certains lots se ferment vite", "Durée annoncée avant de commencer"]),
    ("🌐", "Recherche web", "Recherche", "6 à 15 min", "60 à 110 crédits",
     "Vous retrouvez une information factuelle sur une source officielle — horaires, tarif, "
     "coordonnées — et vous la reportez avec le lien de la page consultée.",
     ["Sources officielles uniquement", "Lien de la source systématiquement demandé", "« Non trouvé » est une réponse acceptable"]),
]


def build_missions():
    cards = []
    for icon, title, cat, duration, pay, desc, points in MISSION_DETAIL:
        li = "".join('<li>%s</li>' % p for p in points)
        cards.append("""<article class="card">
  <div class="card-ico">%s</div>
  <span class="badge badge-violet">%s</span>
  <h3 class="mt-2">%s</h3>
  <p class="small muted">%s</p>
  <ul class="small muted" style="padding-left:1.1em">%s</ul>
  <div class="task-foot">
    <span class="pay">%s<small>par lot</small></span>
    <span class="badge">⏱️ %s</span>
  </div>
</article>""" % (icon, cat, title, desc, li, pay, duration))

    body = """<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow"><span class="dot"></span> Catalogue</span>
      <h1>Les missions proposées sur Tacheo</h1>
      <p class="lead">Huit familles de missions, avec pour chacune la durée moyenne d'un lot, la
      rémunération constatée et les exigences de qualité. Les lots réellement disponibles dépendent
      de votre profil et des commandes en cours.</p>
    </div>
    <div class="grid grid-2">
      %s
    </div>
  </div>
</section>

<section class="section-soft">
  <div class="wrap wrap-sm">
    <h2 class="center">Comment la rémunération est calculée</h2>
    <p class="lead center">Chaque lot affiche son montant en crédits avant que vous ne l'ouvriez.
    Aucun lot ne se déclenche sans que vous ayez vu ce qu'il rapporte.</p>
    <div class="card mt-3">
      <table class="table">
        <thead><tr><th>Unité</th><th class="num">Équivalence</th></tr></thead>
        <tbody>
          <tr><td>100 crédits</td><td class="num">1,00 €</td></tr>
          <tr><td>Seuil de retrait</td><td class="num">2 500 crédits (25,00 €)</td></tr>
          <tr><td>Délai de virement SEPA</td><td class="num">2 à 5 jours ouvrés</td></tr>
          <tr><td>Frais de retrait, zone SEPA</td><td class="num">Aucun</td></tr>
        </tbody>
      </table>
    </div>
    <p class="small muted mt-2">Les montants indiqués correspondent à la moyenne constatée sur le
    dernier trimestre. Ils varient selon la complexité du lot et le taux de qualité du membre.</p>
  </div>
</section>

%s
""" % ("\n".join(cards),
       cta_band("Une famille de missions vous parle ?",
                "Déposez votre candidature : elle est gratuite et vous positionne sur les lots correspondant à votre profil."))

    return layout(
        "missions.html",
        "Types de missions — Tacheo",
        "Classification d'images, saisie de données, transcription, vérification, test "
        "d'applications, modération, sondages, recherche web : le détail des missions Tacheo.",
        body, active="missions",
    )


# ===========================================================================
#  FAQ complète
# ===========================================================================

FAQ_SECTIONS = [
    ("Candidature et ouverture de compte", [
        ("Qui peut candidater sur Tacheo ?",
         "Toute personne majeure disposant d'une connexion internet et d'un moyen d'encaissement à son nom. Aucun diplôme n'est requis et aucune expérience préalable n'est demandée."),
        ("Combien de temps prend le formulaire de candidature ?",
         "Environ dix minutes. Il comporte quatre étapes : coordonnées, profil et disponibilités, court test de compréhension des consignes, puis récapitulatif."),
        ("Le dépôt de candidature est-il payant ?",
         "Non. Déposer une candidature est gratuit et ne vous engage à rien."),
        ("Sous quel délai obtient-on une réponse ?",
         "Sous 24 à 48 heures ouvrées. La décision apparaît dans votre espace membre et vous est notifiée par e-mail."),
        ("Ma candidature a été refusée, puis-je recommencer ?",
         "Oui. Un nouveau dossier peut être déposé après un délai de sept jours, en tenant compte des remarques figurant dans la décision."),
        ("Puis-je avoir plusieurs comptes ?",
         "Non. Un seul compte par personne physique. Les comptes multiples sont fermés et les crédits associés annulés."),
    ]),
    ("Après l'acceptation de votre dossier", [
        ("Que se passe-t-il une fois le dossier accepté ?",
         "Votre espace membre s'ouvre sur l'étape d'activation du compte. Cette étape se règle une seule fois, puis les lots de missions correspondant à votre profil deviennent accessibles."),
        ("En quoi consiste l'activation du compte ?",
         "L'activation couvre la vérification d'identité, l'ouverture du portefeuille de paiement et l'accès permanent au catalogue de missions. Elle est facturée 20,00 € TTC, une seule fois, sans abonnement ni prélèvement ultérieur. Le montant, le détail des prestations et le droit de rétractation sont rappelés sur la page de paiement et dans les conditions de vente avant tout règlement."),
        ("L'activation est-elle renouvelée chaque mois ?",
         "Non. Il s'agit d'un paiement unique. Aucun prélèvement récurrent n'est mis en place et aucune carte n'est conservée pour un débit ultérieur."),
        ("Puis-je être remboursé de l'activation ?",
         "Oui, dans les conditions prévues à l'article 6 des conditions de vente : quatorze jours à compter du paiement, dès lors que vous n'avez pas demandé l'exécution immédiate du service."),
        ("Combien de temps l'accès reste-t-il ouvert ?",
         "Sans limitation de durée, tant que le compte reste actif et conforme aux conditions d'utilisation."),
    ]),
    ("Missions et qualité", [
        ("Comment les lots me sont-ils attribués ?",
         "Selon votre profil déclaré, votre historique de qualité et les quotas fixés par le donneur d'ordre. Vous restez libre d'ouvrir ou d'ignorer un lot."),
        ("Existe-t-il un volume minimal à traiter ?",
         "Non. Aucun quota n'est imposé. Un compte sans activité pendant douze mois consécutifs est toutefois mis en sommeil."),
        ("Pourquoi une mission peut-elle être rejetée ?",
         "Principalement pour non-respect des consignes, réponses incohérentes avec le recoupement des autres membres, ou traitement manifestement trop rapide pour être sérieux."),
        ("Que se passe-t-il si je conteste un rejet ?",
         "Chaque rejet peut être contesté depuis l'historique de votre espace, sous sept jours. Un second examen est réalisé par un autre évaluateur."),
        ("Comment est calculé mon taux de qualité ?",
         "Sur les cent dernières unités traitées, rapport entre unités validées et unités soumises. Sous 80 %, l'accès à certaines familles de missions est temporairement restreint."),
    ]),
    ("Crédits, retraits et fiscalité", [
        ("Que valent les crédits Tacheo ?",
         "100 crédits équivalent à 1,00 €. La conversion est fixe et affichée dans votre portefeuille."),
        ("À partir de quel montant puis-je retirer ?",
         "À partir de 2 500 crédits, soit 25,00 €."),
        ("Quels sont les moyens de retrait ?",
         "Virement SEPA en euros, portefeuille électronique, ou conversion en cartes cadeaux depuis la boutique."),
        ("Y a-t-il des frais de retrait ?",
         "Aucun frais en zone SEPA. Hors zone SEPA, des frais fixes s'appliquent et sont affichés avant la validation de la demande."),
        ("Dois-je déclarer ces revenus ?",
         "Oui. Les sommes perçues sont des revenus imposables dans votre pays de résidence. Tacheo transmet aux administrations concernées les informations exigées par la directive DAC7 et met un récapitulatif annuel à votre disposition."),
    ]),
    ("Compte, données et sécurité", [
        ("Quelles données sont collectées ?",
         "Vos coordonnées, les informations de profil que vous renseignez, votre historique de missions et les données strictement nécessaires au paiement. Le détail figure dans la politique de confidentialité."),
        ("Mes données sont-elles revendues ?",
         "Non. Elles ne sont transmises qu'aux prestataires techniques nécessaires au fonctionnement du service, sous contrat, et aux administrations lorsque la loi l'exige."),
        ("Comment supprimer mon compte ?",
         "Depuis votre espace membre ou par courriel à contact@tacheo.example. La suppression est effective sous trente jours, hors données à conservation légale obligatoire."),
        ("Que faire en cas d'activité suspecte sur mon compte ?",
         "Changez immédiatement votre mot de passe et écrivez au support. Le compte peut être gelé le temps de la vérification."),
    ]),
]


def build_faq():
    sections = []
    for title, items in FAQ_SECTIONS:
        sections.append("""<div class="mt-3">
  <h2>%s</h2>
  %s
</div>""" % (title, faq_block(items)))

    body = """<section>
  <div class="wrap wrap-sm">
    <div class="section-head">
      <span class="eyebrow"><span class="dot"></span> Centre d'aide</span>
      <h1>Questions fréquentes</h1>
      <p class="lead">Tout ce qu'il faut savoir avant de candidater, et une fois le dossier accepté.</p>
    </div>
    %s
    <div class="alert alert-violet mt-3">
      <span class="alert-ico">✉️</span>
      <p>Vous ne trouvez pas votre réponse ? Écrivez-nous depuis la <a href="contact.html">page contact</a>,
      le support répond sous un jour ouvré.</p>
    </div>
  </div>
</section>

%s
""" % ("\n".join(sections),
       cta_band("Une dernière question ? Elle trouvera sa réponse en chemin.",
                "Le dépôt de candidature est gratuit et sans engagement."))

    return layout(
        "faq.html",
        "Questions fréquentes — Tacheo",
        "Candidature, missions, qualité, crédits, retraits, données personnelles : "
        "les réponses aux questions les plus posées sur Tacheo.",
        body, active="faq",
    )


# ===========================================================================
#  Candidature (création de compte + formulaire en 4 étapes)
# ===========================================================================

QUIZ = [
    ("Une consigne précise que les montants doivent être saisis avec une virgule décimale. "
     "Le document affiche « 12.40 ». Que saisissez-vous ?",
     ["12,40", "12.40", "12,4 €", "Je passe l'élément"], 0),
    ("Un champ obligatoire est illisible sur le document à saisir. Que faites-vous ?",
     ["Je le remplis au plus proche", "Je signale le champ comme illisible selon la consigne",
      "Je laisse vide sans rien indiquer", "J'abandonne le lot"], 1),
    ("Une consigne indique « ne pas corriger l'orthographe de la source ». Le nom du commerçant "
     "comporte une faute évidente. Que faites-vous ?",
     ["Je corrige, c'est plus propre", "Je recopie tel quel", "Je mets tout en majuscules", "Je signale au support"], 1),
    ("Sur un lot de 100 images, vous êtes certain de 90 classements et hésitez sur 10. "
     "Quelle est la bonne conduite ?",
     ["Je devine les 10 pour finir plus vite", "Je traite les 90 et j'utilise l'option prévue pour les cas douteux",
      "Je rends le lot vide", "Je recommence le lot depuis le début"], 1),
    ("Un donneur d'ordre vous demande par message vos identifiants de connexion. Que faites-vous ?",
     ["Je les transmets, c'est un client", "Je refuse et je le signale au support",
      "Je crée un second compte pour lui", "Je transmets seulement le mot de passe"], 1),
]


def build_inscription():
    quiz_html = []
    for i, (question, options, _correct) in enumerate(QUIZ):
        opts = "\n".join(
            """<label class="choice"><input type="radio" name="q%d" value="%d" required>
  <span>%s</span></label>""" % (i, j, o) for j, o in enumerate(options)
        )
        quiz_html.append("""<fieldset>
  <legend class="small">Question %d sur %d</legend>
  <p class="field-label" style="margin-bottom:10px">%s</p>
  %s
</fieldset>""" % (i + 1, len(QUIZ), question, opts))

    body = """<section class="app-shell">
  <div class="wrap wrap-sm">
    <div class="center" style="margin-bottom:28px">
      <span class="eyebrow"><span class="dot"></span> Étape 1 du parcours</span>
      <h1>Déposer ma candidature</h1>
      <p class="lead">Quatre étapes, une dizaine de minutes. Le dépôt est gratuit et sans engagement ;
      la décision vous parvient sous 24 à 48 heures ouvrées.</p>
    </div>

    <div class="card">
      <div class="stepper" id="stepper">
        <div class="stepper-item is-current"><div class="stepper-bar"></div><small>Coordonnées</small></div>
        <div class="stepper-item"><div class="stepper-bar"></div><small>Profil</small></div>
        <div class="stepper-item"><div class="stepper-bar"></div><small>Test de consignes</small></div>
        <div class="stepper-item"><div class="stepper-bar"></div><small>Récapitulatif</small></div>
      </div>

      <form id="apply-form" novalidate>

        <!-- Étape 1 : coordonnées -->
        <div class="form-step is-active" data-step="0">
          <h2 style="font-size:1.3rem">Vos coordonnées</h2>
          <p class="small muted">Elles doivent correspondre à votre pièce d'identité : la vérification
          en dépendra plus tard.</p>
          <div class="field-row">
            <div class="field">
              <label for="prenom">Prénom</label>
              <input type="text" id="prenom" name="prenom" autocomplete="given-name" required>
            </div>
            <div class="field">
              <label for="nom">Nom</label>
              <input type="text" id="nom" name="nom" autocomplete="family-name" required>
            </div>
          </div>
          <div class="field">
            <label for="email">Adresse e-mail</label>
            <input type="email" id="email" name="email" autocomplete="email" required>
            <p class="hint">La décision sur votre dossier sera envoyée à cette adresse.</p>
          </div>
          <div class="field-row">
            <div class="field">
              <label for="pays">Pays de résidence</label>
              <select id="pays" name="pays" required>
                <option value="">Choisir…</option>
                <option>France</option><option>Belgique</option><option>Suisse</option>
                <option>Luxembourg</option><option>Canada</option><option>Sénégal</option>
                <option>Côte d'Ivoire</option><option>Cameroun</option><option>Maroc</option>
                <option>Madagascar</option><option>Autre</option>
              </select>
            </div>
            <div class="field">
              <label for="naissance">Date de naissance</label>
              <input type="date" id="naissance" name="naissance" required>
              <p class="hint">Vous devez être majeur.</p>
            </div>
          </div>
          <div class="field-row">
            <div class="field">
              <label for="password">Mot de passe</label>
              <input type="password" id="password" name="password" autocomplete="new-password" required minlength="8">
              <p class="hint">Huit caractères minimum.</p>
            </div>
            <div class="field">
              <label for="password2">Confirmation</label>
              <input type="password" id="password2" name="password2" autocomplete="new-password" required>
            </div>
          </div>
          <div class="form-actions">
            <span></span>
            <button type="button" class="btn btn-primary" data-next>Continuer</button>
          </div>
        </div>

        <!-- Étape 2 : profil -->
        <div class="form-step" data-step="1">
          <h2 style="font-size:1.3rem">Votre profil</h2>
          <p class="small muted">Ces éléments servent à vous proposer les lots qui vous correspondent.</p>

          <div class="field">
            <span class="field-label">Situation actuelle</span>
            <div class="choice-grid">
              <label class="choice"><input type="radio" name="situation" value="Étudiant" required><span>Étudiant</span></label>
              <label class="choice"><input type="radio" name="situation" value="Salarié"><span>Salarié</span></label>
              <label class="choice"><input type="radio" name="situation" value="Indépendant"><span>Indépendant</span></label>
              <label class="choice"><input type="radio" name="situation" value="Sans emploi"><span>En recherche d'emploi</span></label>
              <label class="choice"><input type="radio" name="situation" value="Parent au foyer"><span>Parent au foyer</span></label>
              <label class="choice"><input type="radio" name="situation" value="Retraité"><span>Retraité</span></label>
            </div>
          </div>

          <div class="field">
            <label for="dispo">Disponibilité hebdomadaire</label>
            <select id="dispo" name="dispo" required>
              <option value="">Choisir…</option>
              <option>Moins de 5 heures</option>
              <option>5 à 10 heures</option>
              <option>10 à 20 heures</option>
              <option>Plus de 20 heures</option>
            </select>
          </div>

          <div class="field">
            <span class="field-label">Équipement dont vous disposez</span>
            <div class="choice-grid">
              <label class="choice"><input type="checkbox" name="equip" value="Ordinateur"><span>Ordinateur</span></label>
              <label class="choice"><input type="checkbox" name="equip" value="Smartphone"><span>Smartphone</span></label>
              <label class="choice"><input type="checkbox" name="equip" value="Casque audio"><span>Casque audio</span></label>
              <label class="choice"><input type="checkbox" name="equip" value="Connexion fibre"><span>Connexion stable</span></label>
            </div>
          </div>

          <div class="field">
            <span class="field-label">Familles de missions qui vous intéressent</span>
            <div class="choice-grid">
              <label class="choice"><input type="checkbox" name="interets" value="Saisie de données"><span>Saisie de données</span></label>
              <label class="choice"><input type="checkbox" name="interets" value="Transcription"><span>Transcription audio</span></label>
              <label class="choice"><input type="checkbox" name="interets" value="Classification"><span>Classification d'images</span></label>
              <label class="choice"><input type="checkbox" name="interets" value="Vérification"><span>Vérification</span></label>
              <label class="choice"><input type="checkbox" name="interets" value="Modération"><span>Modération</span></label>
              <label class="choice"><input type="checkbox" name="interets" value="Test d'applications"><span>Test d'applications</span></label>
            </div>
          </div>

          <div class="field">
            <label for="motivation">En quelques lignes, pourquoi souhaitez-vous rejoindre Tacheo ?</label>
            <textarea id="motivation" name="motivation" required minlength="40"
              placeholder="Votre disponibilité, ce qui vous attire dans ces missions, votre expérience éventuelle…"></textarea>
            <p class="hint">40 caractères minimum. Ce champ est lu lors de l'examen du dossier.</p>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-ghost" data-prev>Retour</button>
            <button type="button" class="btn btn-primary" data-next>Continuer</button>
          </div>
        </div>

        <!-- Étape 3 : test de consignes -->
        <div class="form-step" data-step="2">
          <h2 style="font-size:1.3rem">Test de compréhension des consignes</h2>
          <div class="alert alert-violet">
            <span class="alert-ico">💡</span>
            <p>Cinq situations concrètes. Ce test évalue votre lecture des consignes, pas vos
            connaissances. Il n'y a pas de limite de temps.</p>
          </div>
          %s
          <div class="form-actions">
            <button type="button" class="btn btn-ghost" data-prev>Retour</button>
            <button type="button" class="btn btn-primary" data-next>Continuer</button>
          </div>
        </div>

        <!-- Étape 4 : récapitulatif -->
        <div class="form-step" data-step="3">
          <h2 style="font-size:1.3rem">Récapitulatif</h2>
          <p class="small muted">Vérifiez vos informations avant l'envoi. Elles ne seront plus
          modifiables pendant l'examen du dossier.</p>
          <div class="card" style="background:var(--bg-soft);box-shadow:none" id="recap"></div>

          <div class="field mt-3">
            <label class="choice"><input type="checkbox" name="cgu" required>
              <span>Je certifie l'exactitude des informations fournies et j'accepte les
              <a href="cgu.html" target="_blank" rel="noopener">conditions d'utilisation</a> ainsi que la
              <a href="confidentialite.html" target="_blank" rel="noopener">politique de confidentialité</a>.</span>
            </label>
            <label class="choice"><input type="checkbox" name="majeur" required>
              <span>Je déclare être majeur et candidater pour mon propre compte.</span>
            </label>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-ghost" data-prev>Retour</button>
            <button type="submit" class="btn btn-lg btn-primary">Envoyer ma candidature</button>
          </div>
        </div>

      </form>
    </div>

    <p class="small muted center mt-3">Vous avez déjà un compte ?
      <a href="connexion.html">Connectez-vous</a>.</p>
  </div>
</section>
""" % "\n".join(quiz_html)

    return layout(
        "inscription.html",
        "Déposer ma candidature — Tacheo",
        "Formulaire de candidature Tacheo en quatre étapes : coordonnées, profil, "
        "test de compréhension des consignes et récapitulatif. Gratuit et sans engagement.",
        body, scripts=("candidature.js",),
    )


# ===========================================================================
#  Connexion
# ===========================================================================

def build_connexion():
    body = """<section class="app-shell">
  <div class="wrap wrap-xs">
    <div class="center" style="margin-bottom:24px">
      <h1 style="font-size:1.9rem">Connexion</h1>
      <p class="muted">Accédez à votre espace membre et au suivi de votre dossier.</p>
    </div>
    <div class="card">
      <form id="login-form" novalidate>
        <div class="field">
          <label for="email">Adresse e-mail</label>
          <input type="email" id="email" name="email" autocomplete="email" required>
        </div>
        <div class="field">
          <label for="password">Mot de passe</label>
          <input type="password" id="password" name="password" autocomplete="current-password" required>
        </div>
        <div id="login-error" class="error-text hide"></div>
        <button class="btn btn-primary btn-block btn-lg mt-2" type="submit">Se connecter</button>
      </form>
      <p class="small muted center mt-3 mb-0">Pas encore de compte ?
        <a href="inscription.html">Déposer une candidature</a></p>
    </div>
    <div class="alert mt-3">
      <span class="alert-ico">ℹ️</span>
      <p class="small mb-0">Démonstration : le compte créé lors de la candidature est enregistré
      localement dans ce navigateur. Aucune donnée n'est transmise à un serveur.</p>
    </div>
  </div>
</section>
"""
    return layout(
        "connexion.html", "Connexion — Tacheo",
        "Connectez-vous à votre espace membre Tacheo pour suivre votre dossier et accéder à vos missions.",
        body, scripts=("connexion.js",),
    )


# ===========================================================================
#  Espace membre — tableau de bord
# ===========================================================================

def build_compte():
    body = """<section class="app-shell">
  <div class="wrap">
    <div class="app-head">
      <h1>Bonjour <span data-user-name>—</span></h1>
      <span id="stage-badge" class="badge">Chargement…</span>
    </div>
    %s
    <div id="dashboard"></div>
  </div>
</section>
""" % app_tabs("compte")

    return layout(
        "compte.html", "Mon espace — Tacheo",
        "Suivi de votre dossier de candidature et accès à vos missions Tacheo.",
        body, guard="member", scripts=("compte.js",),
    )


# ===========================================================================
#  Activation du compte (frais unique) — accessible après acceptation
# ===========================================================================

def build_activation():
    body = """<section class="app-shell">
  <div class="wrap">
    <div class="app-head">
      <h1>Activation de votre compte</h1>
      <span class="badge badge-green">Candidature acceptée</span>
    </div>

    <div class="alert alert-green">
      <span class="alert-ico">🎉</span>
      <p><strong>Votre dossier a été retenu.</strong> Il reste une étape avant l'ouverture de votre
      accès aux missions : l'activation du compte, qui se règle une seule fois.</p>
    </div>

    <div class="pay-grid">
      <div class="card">
        <h2 style="font-size:1.25rem">Ce que couvre l'activation</h2>
        <ul class="small">
          <li><strong>Vérification d'identité (KYC)</strong> — contrôle de votre pièce d'identité et de
          votre justificatif de domicile, obligatoire avant tout versement.</li>
          <li><strong>Ouverture du portefeuille de paiement</strong> — création de votre compte de
          règlement et enregistrement de vos coordonnées bancaires.</li>
          <li><strong>Accès permanent au catalogue</strong> — l'ensemble des familles de missions
          correspondant à votre profil, sans limitation de durée.</li>
          <li><strong>Support et contestation</strong> — accès au support francophone et à la
          procédure de second examen en cas de rejet de mission.</li>
        </ul>

        <div class="alert alert-amber mt-3">
          <span class="alert-ico">⚠️</span>
          <p class="mb-0"><strong>Paiement unique de 20,00 € TTC.</strong> Il n'y a ni abonnement, ni
          reconduction, ni prélèvement ultérieur. Vos données de carte ne sont pas conservées.
          Le droit de rétractation de quatorze jours s'applique dans les conditions prévues à
          l'<a href="cgv.html">article 6 des conditions de vente</a>.</p>
        </div>

        <h2 style="font-size:1.25rem" class="mt-3">Règlement</h2>
        <form id="pay-form" novalidate>
          <div class="field">
            <span class="field-label">Moyen de paiement</span>
            <div class="choice-grid">
              <label class="choice is-picked"><input type="radio" name="method" value="card" checked><span>Carte bancaire</span></label>
              <label class="choice"><input type="radio" name="method" value="sepa"><span>Prélèvement SEPA unique</span></label>
            </div>
          </div>

          <div id="card-fields">
            <div class="field">
              <label for="cardname">Nom du titulaire</label>
              <input type="text" id="cardname" name="cardname" autocomplete="cc-name" required>
            </div>
            <div class="field">
              <label for="cardnum">Numéro de carte</label>
              <input type="text" id="cardnum" name="cardnum" inputmode="numeric" autocomplete="cc-number"
                     placeholder="4242 4242 4242 4242" maxlength="23" required>
              <p class="hint">Démonstration : utilisez le numéro de test 4242 4242 4242 4242.</p>
            </div>
            <div class="field-row">
              <div class="field">
                <label for="cardexp">Expiration</label>
                <input type="text" id="cardexp" name="cardexp" placeholder="MM/AA" maxlength="5" autocomplete="cc-exp" required>
              </div>
              <div class="field">
                <label for="cardcvc">Cryptogramme</label>
                <input type="text" id="cardcvc" name="cardcvc" placeholder="123" maxlength="4" inputmode="numeric" required>
              </div>
            </div>
          </div>

          <div id="sepa-fields" class="hide">
            <div class="field">
              <label for="iban">IBAN</label>
              <input type="text" id="iban" name="iban" placeholder="FR76 3000 1007 9412 3456 7890 185">
            </div>
          </div>

          <div class="field">
            <label class="choice"><input type="checkbox" name="cgv" required>
              <span>J'ai lu et j'accepte les <a href="cgv.html" target="_blank" rel="noopener">conditions
              générales de vente</a> et je reconnais avoir été informé du montant de 20,00 € TTC,
              dû une seule fois.</span>
            </label>
          </div>

          <div id="pay-error" class="error-text hide"></div>
          <button class="btn btn-lg btn-green btn-block" type="submit" id="pay-btn">
            Payer 20,00 € et activer mon compte
          </button>
          <p class="tiny muted center mt-2">
            Paiement simulé à des fins de démonstration : aucune somme n'est réellement débitée.
          </p>
        </form>
      </div>

      <aside>
        <div class="price-box">
          <h3 style="font-size:1.05rem">Récapitulatif</h3>
          <div class="price-line"><span>Activation du compte membre</span><span>16,67 €</span></div>
          <div class="price-line"><span>TVA 20 %</span><span>3,33 €</span></div>
          <div class="price-line"><span>Abonnement</span><span class="muted">Aucun</span></div>
          <div class="price-total"><span>Total dû aujourd'hui</span><b>20,00 €</b></div>
          <p class="tiny muted mt-2 mb-0">Paiement unique. Aucun montant ne sera prélevé
          ultérieurement sur ce moyen de paiement.</p>
        </div>

        <div class="card mt-2">
          <h3 style="font-size:1rem">Après le paiement</h3>
          <ul class="small muted" style="padding-left:1.1em;margin-bottom:0">
            <li>Accès immédiat au catalogue de missions</li>
            <li>150 crédits de bienvenue versés sur votre portefeuille</li>
            <li>Reçu disponible dans votre espace membre</li>
          </ul>
        </div>

        <div class="card mt-2">
          <h3 style="font-size:1rem">Vous préférez réfléchir ?</h3>
          <p class="small muted">Votre acceptation reste valable trente jours. Vous pouvez revenir
          plus tard : votre dossier ne sera pas réexaminé.</p>
          <a class="btn btn-ghost btn-block btn-sm" href="compte.html">Revenir au tableau de bord</a>
        </div>
      </aside>
    </div>
  </div>
</section>
"""
    return layout(
        "activation.html", "Activation du compte — Tacheo",
        "Activation unique du compte membre Tacheo après acceptation de la candidature.",
        body, guard="accepted", scripts=("activation.js",),
    )


# ===========================================================================
#  Catalogue de missions (espace membre)
# ===========================================================================

def build_taches():
    body = """<section class="app-shell">
  <div class="wrap">
    <div class="app-head">
      <h1>Missions disponibles</h1>
      <span class="badge badge-green">Compte actif</span>
    </div>
    %s
    <div class="filters" id="filters"></div>
    <div class="grid grid-3" id="task-grid"></div>
    <p class="small muted mt-3">Les lots sont attribués selon votre profil et votre taux de qualité.
    Un lot ouvert doit être terminé pour être rémunéré.</p>
  </div>
</section>
""" % app_tabs("taches")

    return layout(
        "taches.html", "Missions disponibles — Tacheo",
        "Catalogue des lots de missions disponibles sur votre compte Tacheo.",
        body, guard="active", scripts=("data.js", "taches.js"),
    )


def build_tache():
    body = """<section class="app-shell">
  <div class="wrap wrap-sm">
    <p class="small"><a href="taches.html">← Retour aux missions</a></p>
    <div id="task-view"></div>
  </div>
</section>
"""
    return layout(
        "tache.html", "Mission en cours — Tacheo",
        "Exécution d'un lot de missions Tacheo.",
        body, guard="active", scripts=("data.js", "tache.js"),
    )


def build_portefeuille():
    body = """<section class="app-shell">
  <div class="wrap">
    <div class="app-head"><h1>Portefeuille</h1></div>
    %s
    <div class="app-grid">
      <div>
        <div class="kpi-row">
          <div class="kpi"><small>Solde disponible</small><b id="kpi-credits">—</b><span class="small muted" id="kpi-euros">—</span></div>
          <div class="kpi"><small>Total gagné</small><b id="kpi-total">—</b><span class="small muted">depuis l'inscription</span></div>
          <div class="kpi"><small>Missions validées</small><b id="kpi-tasks">—</b><span class="small muted">lots terminés</span></div>
        </div>
        <div class="card">
          <h2 style="font-size:1.15rem">Historique des opérations</h2>
          <div id="history"></div>
        </div>
      </div>
      <aside>
        <div class="card">
          <h3 style="font-size:1.05rem">Demander un retrait</h3>
          <p class="small muted">Seuil minimal : 2 500 crédits (25,00 €). Aucun frais en zone SEPA.</p>
          <form id="payout-form" novalidate>
            <div class="field">
              <label for="amount">Montant en crédits</label>
              <input type="number" id="amount" name="amount" min="2500" step="100" placeholder="2500">
            </div>
            <div class="field">
              <label for="method">Moyen de versement</label>
              <select id="method" name="method">
                <option>Virement SEPA</option>
                <option>Portefeuille électronique</option>
                <option>Carte cadeau</option>
              </select>
            </div>
            <div id="payout-error" class="error-text hide"></div>
            <button class="btn btn-primary btn-block" type="submit">Demander le retrait</button>
          </form>
        </div>
        <div class="card mt-2">
          <h3 style="font-size:1rem">Bon à savoir</h3>
          <ul class="small muted" style="padding-left:1.1em;margin-bottom:0">
            <li>100 crédits = 1,00 €</li>
            <li>Virement SEPA sous 2 à 5 jours ouvrés</li>
            <li>Récapitulatif annuel disponible pour votre déclaration</li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</section>
""" % app_tabs("portefeuille")

    return layout(
        "portefeuille.html", "Portefeuille — Tacheo",
        "Solde, historique des gains et demandes de retrait sur votre compte Tacheo.",
        body, guard="active", scripts=("portefeuille.js",),
    )


# ===========================================================================
#  Contact
# ===========================================================================

def build_contact():
    body = """<section>
  <div class="wrap wrap-sm">
    <div class="section-head">
      <h1>Nous écrire</h1>
      <p class="lead">Le support répond sous un jour ouvré, du lundi au vendredi, de 9 h à 18 h (CET).</p>
    </div>
    <div class="card">
      <form id="contact-form" novalidate>
        <div class="field-row">
          <div class="field"><label for="cnom">Nom</label><input type="text" id="cnom" required></div>
          <div class="field"><label for="cmail">Adresse e-mail</label><input type="email" id="cmail" required></div>
        </div>
        <div class="field">
          <label for="csujet">Sujet</label>
          <select id="csujet" required>
            <option value="">Choisir…</option>
            <option>Question sur ma candidature</option>
            <option>Question sur une mission</option>
            <option>Question sur un paiement</option>
            <option>Données personnelles</option>
            <option>Autre</option>
          </select>
        </div>
        <div class="field">
          <label for="cmsg">Message</label>
          <textarea id="cmsg" required minlength="20"></textarea>
        </div>
        <button class="btn btn-primary btn-lg" type="submit">Envoyer le message</button>
        <p class="tiny muted mt-2 mb-0">Démonstration : le formulaire n'envoie aucun message.</p>
      </form>
    </div>
    <div class="grid grid-2 mt-3">
      <div class="card"><h3 style="font-size:1rem">Support membres</h3>
        <p class="small muted mb-0">contact@tacheo.example<br>Réponse sous 1 jour ouvré</p></div>
      <div class="card"><h3 style="font-size:1rem">Données personnelles</h3>
        <p class="small muted mb-0">dpo@tacheo.example<br>Réponse sous 30 jours</p></div>
    </div>
  </div>
</section>
"""
    return layout("contact.html", "Contact — Tacheo",
                  "Contacter le support Tacheo : candidature, missions, paiements, données personnelles.",
                  body, scripts=("contact.js",))


# ===========================================================================
#  Pages légales
# ===========================================================================

def legal_page(filename, title, heading, intro, sections):
    blocks = []
    for h, paragraphs in sections:
        blocks.append("<h2>%s</h2>" % h)
        for p in paragraphs:
            blocks.append(p if p.startswith("<") else "<p>%s</p>" % p)
    body = """<section>
  <div class="wrap wrap-sm prose">
    <h1>%s</h1>
    <p class="lead">%s</p>
    %s
    <p class="small muted mt-3">Dernière mise à jour : 15 août 2026.</p>
  </div>
</section>
""" % (heading, intro, "\n".join(blocks))
    return layout(filename, title, intro[:155], body)


def build_legal():
    legal_page(
        "cgu.html", "Conditions d'utilisation — Tacheo", "Conditions générales d'utilisation",
        "Les présentes conditions régissent l'accès et l'usage de la plateforme Tacheo par ses membres.",
        [
            ("1. Objet", ["Tacheo met en relation des donneurs d'ordre et des membres réalisant des missions courtes en ligne, dites micro-tâches. Les présentes conditions définissent les droits et obligations de chacun."]),
            ("2. Accès à la plateforme", [
                "L'accès est ouvert à toute personne physique majeure, après dépôt d'une candidature et acceptation de celle-ci par Tacheo. Le dépôt d'une candidature est gratuit.",
                "L'ouverture effective de l'accès aux missions est subordonnée à l'activation du compte, dont les modalités et le prix figurent dans les <a href=\"cgv.html\">conditions générales de vente</a>.",
                "Un seul compte est autorisé par personne. Toute duplication entraîne la fermeture des comptes concernés."]),
            ("3. Statut du membre", [
                "Le membre agit en toute indépendance. Aucune des dispositions des présentes ne crée de lien de subordination, de contrat de travail ni de mandat entre Tacheo et le membre.",
                "Le membre est seul responsable de ses obligations déclaratives, sociales et fiscales dans son pays de résidence."]),
            ("4. Obligations du membre", [
                "<ul><li>fournir des informations exactes et les tenir à jour ;</li><li>réaliser les missions personnellement, sans automatisation ni sous-traitance ;</li><li>respecter les consignes propres à chaque lot ;</li><li>préserver la confidentialité des contenus traités ;</li><li>ne pas tenter de contourner les contrôles qualité.</li></ul>"]),
            ("5. Qualité et rejet de missions", [
                "Chaque mission fait l'objet d'un contrôle qualité, notamment par recoupement entre plusieurs membres. Une mission rejetée n'est pas rémunérée.",
                "Tout rejet peut être contesté sous sept jours depuis l'espace membre. Un second examen est alors réalisé par un autre évaluateur."]),
            ("6. Rémunération", [
                "Les missions validées créditent le portefeuille du membre en crédits Tacheo, à raison de 100 crédits pour 1,00 €. Le retrait est possible à partir de 2 500 crédits."]),
            ("7. Suspension et résiliation", [
                "Tacheo peut suspendre ou fermer un compte en cas de manquement grave aux présentes conditions, notamment fraude, comptes multiples ou automatisation. Les crédits acquis de manière frauduleuse sont annulés.",
                "Le membre peut fermer son compte à tout moment depuis son espace. Les crédits disponibles au-delà du seuil de retrait restent réclamables pendant quatre-vingt-dix jours."]),
            ("8. Responsabilité", [
                "Tacheo s'engage à mettre en œuvre les moyens nécessaires au bon fonctionnement de la plateforme, sans garantir une disponibilité ininterrompue ni un volume de missions déterminé."]),
            ("9. Droit applicable", [
                "Les présentes conditions sont soumises au droit français. En cas de litige, une solution amiable sera recherchée avant toute action contentieuse."]),
        ])

    legal_page(
        "cgv.html", "Conditions de vente — Tacheo", "Conditions générales de vente",
        "Les présentes conditions encadrent la seule prestation payante de la plateforme : l'activation du compte membre.",
        [
            ("1. Prestation concernée", [
                "La seule prestation facturée par Tacheo au membre est l'<strong>activation du compte</strong>. Le dépôt d'une candidature, la consultation du site et l'usage courant de la plateforme demeurent gratuits."]),
            ("2. Contenu de la prestation", [
                "<ul><li>vérification d'identité et contrôle des justificatifs (KYC) ;</li><li>ouverture du portefeuille de paiement et enregistrement des coordonnées bancaires ;</li><li>accès permanent au catalogue de missions correspondant au profil du membre ;</li><li>accès au support francophone et à la procédure de second examen.</li></ul>"]),
            ("3. Prix", [
                "Le prix de l'activation est de <strong>20,00 € TTC</strong> (16,67 € HT, TVA 20 % : 3,33 €).",
                "Ce montant est dû <strong>une seule fois</strong>. Il ne s'agit pas d'un abonnement : aucune reconduction, aucun prélèvement périodique et aucune conservation des données de carte en vue d'un débit ultérieur ne sont mis en œuvre.",
                "Le prix est porté à la connaissance du membre, avec le détail de la prestation, sur la page de paiement, avant toute saisie de moyen de paiement et avant toute validation de commande."]),
            ("4. Moment de la facturation", [
                "L'activation n'est proposée qu'après l'acceptation de la candidature. Un membre dont le dossier n'a pas été retenu ne se voit facturer aucune somme."]),
            ("5. Paiement", [
                "Le paiement s'effectue par carte bancaire ou par prélèvement SEPA unique, via un prestataire de services de paiement agréé. Un reçu est mis à disposition dans l'espace membre."]),
            ("6. Droit de rétractation", [
                "Conformément aux articles L. 221-18 et suivants du code de la consommation, le membre dispose de <strong>quatorze jours</strong> à compter du paiement pour se rétracter, sans motif ni pénalité.",
                "Lorsque le membre demande expressément l'exécution immédiate du service et que celui-ci est pleinement exécuté avant l'expiration du délai, le droit de rétractation ne peut plus être exercé, conformément à l'article L. 221-28 du même code. Cette information lui est rappelée au moment du paiement.",
                "La demande de rétractation s'exerce par courriel à contact@tacheo.example. Le remboursement intervient dans les quatorze jours suivant la réception de la demande, par le même moyen de paiement."]),
            ("7. Réclamations et médiation", [
                "Toute réclamation peut être adressée au support. À défaut de solution amiable, le membre consommateur peut recourir gratuitement à un médiateur de la consommation."]),
            ("8. Droit applicable", [
                "Les présentes conditions sont soumises au droit français, sans préjudice des dispositions protectrices applicables dans le pays de résidence du membre consommateur."]),
        ])

    legal_page(
        "confidentialite.html", "Politique de confidentialité — Tacheo", "Politique de confidentialité",
        "Comment Tacheo collecte, utilise et protège les données personnelles de ses membres et visiteurs.",
        [
            ("1. Responsable de traitement", ["Tacheo SAS, dont les coordonnées figurent dans les <a href=\"mentions-legales.html\">mentions légales</a>, est responsable des traitements décrits ci-après. Le délégué à la protection des données est joignable à dpo@tacheo.example."]),
            ("2. Données collectées", [
                "<ul><li><strong>Identité et contact</strong> : nom, prénom, date de naissance, adresse e-mail, pays de résidence ;</li><li><strong>Profil</strong> : situation, disponibilités, équipements, centres d'intérêt, réponses au test de consignes ;</li><li><strong>Activité</strong> : missions réalisées, taux de qualité, historique des crédits ;</li><li><strong>Paiement</strong> : coordonnées bancaires traitées par le prestataire de paiement, jamais stockées sur nos serveurs ;</li><li><strong>Technique</strong> : journaux de connexion et données de sécurité.</li></ul>"]),
            ("3. Finalités et bases légales", [
                "<ul><li>gestion de la candidature et du compte — exécution du contrat ;</li><li>attribution et contrôle des missions — exécution du contrat ;</li><li>versement des rémunérations et lutte contre la fraude — obligation légale et intérêt légitime ;</li><li>déclarations DAC7 — obligation légale ;</li><li>amélioration du service — intérêt légitime.</li></ul>"]),
            ("4. Durées de conservation", [
                "Les données de compte sont conservées pendant la durée de la relation, puis trois ans. Les pièces comptables et les justificatifs d'identité sont conservés selon les durées légales applicables."]),
            ("5. Destinataires", [
                "Les données ne sont ni vendues, ni louées. Elles sont accessibles aux équipes internes habilitées, aux prestataires techniques sous contrat (hébergement, paiement, support) et aux administrations lorsque la loi l'impose."]),
            ("6. Hébergement et transferts", [
                "Les données sont hébergées dans l'Union européenne. Tout transfert hors Union européenne est encadré par les clauses contractuelles types de la Commission européenne."]),
            ("7. Vos droits", [
                "Vous disposez des droits d'accès, de rectification, d'effacement, de limitation, d'opposition et de portabilité, ainsi que du droit de définir des directives post-mortem. Ces droits s'exercent auprès de dpo@tacheo.example. Vous pouvez introduire une réclamation auprès de la CNIL."]),
            ("8. Cookies", [
                "Le site n'utilise aucun cookie publicitaire ni traceur tiers. Seul le stockage local du navigateur est employé, pour conserver l'état de votre session."]),
        ])

    legal_page(
        "mentions-legales.html", "Mentions légales — Tacheo", "Mentions légales",
        "Informations relatives à l'éditeur et à l'hébergeur du site.",
        [
            ("Éditeur", ["<p>Tacheo SAS — société par actions simplifiée au capital de 10 000 €<br>Siège social : 12 rue de la Fontaine, 75011 Paris, France<br>RCS Paris — SIREN 000 000 000<br>Numéro de TVA intracommunautaire : FR00 000000000<br>Directeur de la publication : la présidence de Tacheo SAS<br>Contact : contact@tacheo.example</p>"]),
            ("Hébergement", ["<p>GitHub Pages — GitHub, Inc.<br>88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis</p>"]),
            ("Propriété intellectuelle", ["L'ensemble des contenus du site — textes, éléments graphiques, code — est protégé par le droit d'auteur. Toute reproduction sans autorisation est interdite."]),
            ("Nature du site", [
                "Ce site est un <strong>projet de démonstration technique</strong>. Les données affichées sont fictives, les coordonnées d'entreprise sont des exemples et aucun paiement n'est réellement encaissé.",
                "Ce projet est indépendant : il n'est ni affilié, ni lié, ni approuvé par le site microtaches.com ou toute autre plateforme existante."]),
            ("Signalement", ["Tout contenu litigieux peut être signalé à contact@tacheo.example."]),
        ])


def build_404():
    body = """<section>
  <div class="wrap wrap-sm center" style="padding:60px 0">
    <div class="card-ico" style="margin:0 auto 18px">🧭</div>
    <h1>Page introuvable</h1>
    <p class="lead">Cette adresse ne correspond à aucune page du site. Elle a peut-être été déplacée.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-primary" href="index.html">Retour à l'accueil</a>
      <a class="btn btn-ghost" href="faq.html">Consulter la FAQ</a>
    </div>
  </div>
</section>
"""
    return layout("404.html", "Page introuvable — Tacheo", "La page demandée n'existe pas.", body)


# ===========================================================================
#  Fichiers annexes
# ===========================================================================

PUBLIC_PAGES = ["index.html", "missions.html", "faq.html", "inscription.html",
                "connexion.html", "contact.html", "cgu.html", "cgv.html",
                "confidentialite.html", "mentions-legales.html"]


def build_extras():
    today = "2026-08-15"
    urls = "\n".join(
        "  <url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq>"
        "<priority>%s</priority></url>" % (BASE_URL, p, today, "1.0" if p == "index.html" else "0.7")
        for p in PUBLIC_PAGES
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + urls + "\n</urlset>\n")

    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nAllow: /\nDisallow: /compte.html\nDisallow: /taches.html\n"
                 "Disallow: /tache.html\nDisallow: /portefeuille.html\nDisallow: /activation.html\n\n"
                 "Sitemap: %s/sitemap.xml\n" % BASE_URL)

    # Empêche Jekyll de filtrer les fichiers servis par GitHub Pages.
    open(os.path.join(ROOT, ".nojekyll"), "w").close()


def main():
    pages = [
        build_home(), build_missions(), build_faq(), build_inscription(),
        build_connexion(), build_compte(), build_activation(), build_taches(),
        build_tache(), build_portefeuille(), build_contact(), build_404(),
    ]
    build_legal()
    build_extras()
    print("Pages générées : %d + 4 pages légales + annexes" % len(pages))


if __name__ == "__main__":
    main()
