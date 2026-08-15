/* ==========================================================================
   Tacheo — catalogue de missions
   Chaque mission décrit son type d'interaction et les éléments à traiter.
   En production, ce fichier serait remplacé par un appel API renvoyant les
   lots de tâches disponibles pour le membre connecté.
   ========================================================================== */
window.TACHEO_TASKS = [
  {
    id: "img-01",
    title: "Classification d'images pour l'IA",
    category: "Intelligence artificielle",
    icon: "🖼️",
    credits: 42,
    minutes: 4,
    level: "Débutant",
    summary: "Attribuer la bonne catégorie à une série de visuels destinés à entraîner un modèle de reconnaissance.",
    brief: [
      "Regardez le visuel affiché au centre de l'écran.",
      "Choisissez la catégorie qui décrit le mieux l'objet principal.",
      "En cas de doute réel, choisissez « Autre » plutôt que de deviner."
    ],
    type: "classify",
    items: [
      { visual: "🚲", options: ["Véhicule", "Animal", "Aliment", "Autre"] },
      { visual: "🍜", options: ["Véhicule", "Animal", "Aliment", "Autre"] },
      { visual: "🦜", options: ["Véhicule", "Animal", "Aliment", "Autre"] },
      { visual: "🚌", options: ["Véhicule", "Animal", "Aliment", "Autre"] },
      { visual: "🪴", options: ["Véhicule", "Animal", "Aliment", "Autre"] },
      { visual: "🧀", options: ["Véhicule", "Animal", "Aliment", "Autre"] }
    ]
  },
  {
    id: "saisie-01",
    title: "Saisie de tickets de caisse",
    category: "Saisie de données",
    icon: "🧾",
    credits: 68,
    minutes: 7,
    level: "Débutant",
    summary: "Reporter les informations clés de tickets numérisés dans un formulaire structuré.",
    brief: [
      "Recopiez fidèlement les champs demandés, sans corriger l'orthographe du commerçant.",
      "Les montants s'écrivent avec une virgule décimale (ex. 12,40).",
      "Un champ illisible se saisit avec le caractère « ? »."
    ],
    type: "entry",
    items: [
      {
        sample: { Commerçant: "Boulangerie Le Fournil", Date: "14/03/2026", Total: "8,60 €" },
        fields: [
          { name: "commercant", label: "Nom du commerçant", expect: "Boulangerie Le Fournil" },
          { name: "date", label: "Date du ticket", expect: "14/03/2026" },
          { name: "total", label: "Montant total", expect: "8,60" }
        ]
      },
      {
        sample: { Commerçant: "Pharmacie des Lilas", Date: "02/04/2026", Total: "23,15 €" },
        fields: [
          { name: "commercant", label: "Nom du commerçant", expect: "Pharmacie des Lilas" },
          { name: "date", label: "Date du ticket", expect: "02/04/2026" },
          { name: "total", label: "Montant total", expect: "23,15" }
        ]
      },
      {
        sample: { Commerçant: "Garage Ternois SARL", Date: "27/04/2026", Total: "146,00 €" },
        fields: [
          { name: "commercant", label: "Nom du commerçant", expect: "Garage Ternois SARL" },
          { name: "date", label: "Date du ticket", expect: "27/04/2026" },
          { name: "total", label: "Montant total", expect: "146,00" }
        ]
      }
    ]
  },
  {
    id: "verif-01",
    title: "Vérification de fiches entreprises",
    category: "Vérification",
    icon: "🔎",
    credits: 55,
    minutes: 6,
    level: "Intermédiaire",
    summary: "Comparer deux fiches issues de bases différentes et signaler si elles désignent le même établissement.",
    brief: [
      "Deux fiches vous sont présentées côte à côte.",
      "Indiquez si elles correspondent au même établissement.",
      "Une différence de forme juridique seule ne suffit pas à conclure au non-appariement."
    ],
    type: "verify",
    items: [
      {
        a: "Menuiserie Dubreuil — 14 rue des Peupliers, 59000 Lille",
        b: "MENUISERIE DUBREUIL SARL — 14 r. des Peupliers, Lille 59000"
      },
      {
        a: "Cabinet Vasseur & Associés — 3 place Bellecour, 69002 Lyon",
        b: "Cabinet Vasseur Immobilier — 3 place Bellecour, 69002 Lyon"
      },
      {
        a: "Le Comptoir Vert — 88 avenue Jean Jaurès, 31000 Toulouse",
        b: "Le Comptoir Vert — 88 av. Jean Jaurès, 31000 Toulouse"
      },
      {
        a: "Atelier Sicard — 12 quai de la Fosse, 44000 Nantes",
        b: "Atelier Sicard — 12 quai de la Fosse, 44100 Nantes"
      }
    ]
  },
  {
    id: "modo-01",
    title: "Modération de commentaires",
    category: "Modération",
    icon: "🛡️",
    credits: 60,
    minutes: 5,
    level: "Intermédiaire",
    summary: "Appliquer la charte d'un site d'avis clients à des commentaires publiés par des internautes.",
    brief: [
      "Publier : avis pertinent, même négatif.",
      "Masquer : insulte, propos discriminatoire, coordonnées personnelles.",
      "À revoir : contenu ambigu qui nécessite un second regard."
    ],
    type: "choice",
    options: ["Publier", "Masquer", "À revoir"],
    items: [
      { text: "Livraison en retard de trois jours, mais le service client a été réactif. Produit conforme." },
      { text: "Appelez-moi au 06 12 34 56 78, je revends le même article moins cher." },
      { text: "Franchement déçu par la qualité du tissu pour ce prix-là." },
      { text: "Le vendeur ne répond jamais, c'est une honte, arnaqueurs !" },
      { text: "Commande reçue, tout est parfait. Je recommande." }
    ]
  },
  {
    id: "sondage-01",
    title: "Sondage — habitudes d'achat en ligne",
    category: "Sondages",
    icon: "📊",
    credits: 30,
    minutes: 3,
    level: "Débutant",
    summary: "Répondre à un court questionnaire pour un institut d'études marketing.",
    brief: [
      "Il n'y a pas de bonne ou de mauvaise réponse.",
      "Répondez selon vos habitudes réelles.",
      "Vos réponses sont agrégées de façon anonyme."
    ],
    type: "survey",
    items: [
      { question: "À quelle fréquence achetez-vous en ligne ?", options: ["Plusieurs fois par semaine", "Une fois par semaine", "Une à deux fois par mois", "Plus rarement"] },
      { question: "Quel appareil utilisez-vous le plus pour acheter ?", options: ["Smartphone", "Ordinateur", "Tablette"] },
      { question: "Qu'est-ce qui déclenche le plus votre achat ?", options: ["Le prix", "Les avis clients", "Le délai de livraison", "La marque"] },
      { question: "Consultez-vous les avis avant d'acheter ?", options: ["Systématiquement", "Souvent", "Parfois", "Jamais"] }
    ]
  },
  {
    id: "transcript-01",
    title: "Transcription audio courte",
    category: "Transcription",
    icon: "🎧",
    credits: 85,
    minutes: 9,
    level: "Intermédiaire",
    summary: "Retranscrire des messages vocaux de moins de vingt secondes laissés sur un répondeur professionnel.",
    brief: [
      "Écoutez l'extrait puis retranscrivez-le mot à mot.",
      "La ponctuation est attendue, les hésitations ne le sont pas.",
      "Un mot inaudible se note [inaudible]."
    ],
    type: "transcribe",
    items: [
      { audio: "Bonjour, je vous appelle au sujet du devis envoyé mardi dernier. Pouvez-vous me rappeler avant vendredi ? Merci." },
      { audio: "Bonsoir, c'est madame Renard. Je souhaite décaler mon rendez-vous de jeudi à la semaine prochaine." },
      { audio: "Oui bonjour, je confirme la livraison à l'adresse du chantier, quatorze rue de la Gare." }
    ]
  },
  {
    id: "app-01",
    title: "Test d'application mobile",
    category: "Test produit",
    icon: "📱",
    credits: 120,
    minutes: 14,
    level: "Confirmé",
    summary: "Parcourir un scénario d'utilisation dans une application en préversion et remonter les anomalies.",
    brief: [
      "Suivez le scénario étape par étape.",
      "Signalez toute anomalie, même mineure.",
      "Précisez le modèle d'appareil et la version du système."
    ],
    type: "choice",
    options: ["Fonctionne", "Anomalie mineure", "Bloquant"],
    items: [
      { text: "Étape 1 — Création d'un compte avec une adresse e-mail." },
      { text: "Étape 2 — Réception et saisie du code de confirmation." },
      { text: "Étape 3 — Ajout d'un article au panier depuis la recherche." },
      { text: "Étape 4 — Paiement en mode test et affichage du reçu." }
    ]
  },
  {
    id: "web-01",
    title: "Recherche d'informations publiques",
    category: "Recherche web",
    icon: "🌐",
    credits: 75,
    minutes: 8,
    level: "Intermédiaire",
    summary: "Retrouver une information factuelle sur le site officiel d'une organisation et la reporter.",
    brief: [
      "Utilisez uniquement des sources officielles.",
      "Reportez l'information exactement telle qu'elle apparaît.",
      "Indiquez « non trouvé » plutôt qu'une approximation."
    ],
    type: "entry",
    items: [
      {
        sample: { Organisation: "Mairie de Sarlat-la-Canéda", Recherche: "Horaires d'ouverture le samedi" },
        fields: [
          { name: "reponse", label: "Information trouvée", expect: "" },
          { name: "source", label: "Adresse de la page source", expect: "" }
        ]
      },
      {
        sample: { Organisation: "Bibliothèque municipale de Rennes", Recherche: "Tarif de l'abonnement annuel adulte" },
        fields: [
          { name: "reponse", label: "Information trouvée", expect: "" },
          { name: "source", label: "Adresse de la page source", expect: "" }
        ]
      }
    ]
  },
  {
    id: "audio-01",
    title: "Étiquetage de sons courts",
    category: "Intelligence artificielle",
    icon: "🔊",
    credits: 38,
    minutes: 4,
    level: "Débutant",
    summary: "Associer une étiquette à des extraits sonores servant à entraîner un classifieur audio.",
    brief: [
      "Un extrait, une étiquette.",
      "Si plusieurs sons se superposent, retenez le plus fort.",
      "Les extraits durent moins de cinq secondes."
    ],
    type: "choice",
    options: ["Voix humaine", "Musique", "Bruit urbain", "Nature"],
    items: [
      { text: "Extrait n° 1 — enregistrement 4 s, niveau moyen." },
      { text: "Extrait n° 2 — enregistrement 3 s, niveau élevé." },
      { text: "Extrait n° 3 — enregistrement 5 s, niveau faible." },
      { text: "Extrait n° 4 — enregistrement 2 s, niveau moyen." },
      { text: "Extrait n° 5 — enregistrement 4 s, niveau élevé." }
    ]
  },
  {
    id: "produit-01",
    title: "Comparaison de fiches produit",
    category: "Vérification",
    icon: "⚖️",
    credits: 50,
    minutes: 5,
    level: "Débutant",
    summary: "Repérer les écarts entre la fiche d'un fabricant et celle d'un revendeur.",
    brief: [
      "Comparez les caractéristiques annoncées.",
      "Signalez tout écart de contenance, de référence ou de composition.",
      "Une différence de prix n'est pas un écart à signaler."
    ],
    type: "verify",
    items: [
      { a: "Fabricant — Sirop de menthe, bouteille 70 cl, sans colorant", b: "Revendeur — Sirop de menthe, bouteille 70 cl, sans colorant" },
      { a: "Fabricant — Casque audio X20, autonomie 30 h", b: "Revendeur — Casque audio X20, autonomie 20 h" },
      { a: "Fabricant — Lessive liquide 2 L, 40 lavages", b: "Revendeur — Lessive liquide 2 L, 40 lavages" }
    ]
  }
];
