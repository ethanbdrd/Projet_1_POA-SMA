# Répartition du travail — projet 1

Binôme : BAUDRAND Ethan & EL KAMEL Mohamed Amine

Les numéros de section renvoient à `docs/ENONCE.md`.

## Architecture

### Arborescence du dépôt

```
Projet1/                   racine du dépôt = racine de l'archive rendue
├── agent.py               point d'entrée
├── rendu.json             commande de lancement (section 2)
├── README.md
├── repartition_travail.md
├── demo.py                démo fournie, à supprimer quand agent.py marchera
├── reconfort/             le code du robot, un module par responsabilité
├── tests/                 tests automatisés (section 8)
├── cartes/                cartes et scénarios fournis, puis les nôtres
├── donnees/               dictionnaire et armoire
├── rapport/               rapport de 3 pages (section 11)
└── docs/                  énoncé et documents du prof (ne pas modifier)
```

### Le point d'entrée : `agent.py`

Il est lancé avec quatre arguments, dans cet ordre :

```
python agent.py <carte.json> <scenario.json> <dossier_donnees> <trace.json>
```

1. le chemin de la carte ;
2. le chemin du scénario ;
3. le dossier de données, qui contient `dictionnaire.json` et les armoires.
   Le fichier d'armoire à charger est `<dossier>/<scenario["armoire"]>.json` :
   ne jamais écrire `armoire_standard` en dur ;
4. le chemin de la trace à écrire.

`agent.py` reste très court : il lit les arguments, charge et valide les
fichiers, construit le simulateur et le robot, lance la simulation, écrit la
trace et renvoie le code de retour (0 si tout va bien, non nul en cas
d'erreur de données). Toute la logique vit dans `reconfort/`.

### Les modules de `reconfort/` 

- `reconfort_io.py` (fourni) : lecture des fichiers JSON (ne vérifie que
  `format` et `version`), `normaliser` pour découper un message en mots,
  classe `Trace` pour écrire la sortie.
- `validation.py` : toutes les vérifications de la section 5.6, avant la
  simulation. A le droit de lire `grille` pour vérifier les symboles.
- `simulateur.py` : la réalité. Perception, contenu du casier courant,
  légalité et application des actions. **Seul module à utiliser `grille` et
  `objet`.**
- `structures.py` : la file (parcours en largeur) et le cycle à 8 éléments
  (roue des émotions, colonnes de l'armoire).
- `carte_mentale.py` : **mémoire** du robot sur l'appartement (cases
  inconnues, libres, obstacles).
- `planification.py` : **décision**, parcours en largeur sur la carte
  mentale.
- `dictionnaire.py` : **décision**, message → (émotion, intensité), ou
  émotion indéterminée (section 6.1).
- `armoire.py` : **mémoire** et **décision** côté armoire. Liste ordonnée
  des 15 casiers candidats (section 6.2), trajet du sélecteur, casiers déjà
  vus.
- `robot.py` : l'agent. Cycle percevoir → mémoriser → décider → agir, et
  enchaînement d'une demande (dictionnaire → armoire → résident).
- `affichage.py` : dessin de la grille dans le terminal, pour le débogage et
  la vidéo. Ne fait pas partie de l'agent.

### Qui parle à qui

```
agent.py ──► reconfort_io (lecture) ──► validation
   │
   ├──► simulateur        la réalité : grille, objets des casiers
   │       ▲        │
   │     action   perception (4 cases voisines, contenu du casier)
   │       │        ▼
   └──► robot             l'agent : ne connaît que ses perceptions
           ├── carte_mentale + planification
           ├── dictionnaire
           ├── armoire
           └──► Trace     un pas par action, une livraison par demande
```

Deux règles à respecter partout :

- le robot ne reçoit **jamais** le dictionnaire `carte` complet ni le champ
  `objet`. Il reçoit seulement ses connaissances de départ (dimensions, sa
  position, positions de l'armoire, du dictionnaire et des résidents,
  étiquettes des casiers) puis, à chaque tour, sa perception ;
- aucune variable globale : au projet 2, plusieurs robots partageront le
  même simulateur.

## Qui fait quoi ?  

Les étapes 1 à 4 sont indépendantes : on les mène en parallèle.

### Étape 0 — Organisation du dépôt

- Responsables : Ethan & Amine
- Quoi : arborescence du dépôt (sa racine sera la racine de l'archive
  rendue), `.gitignore`, `rendu.json` avec nos deux noms, début du README.
- Point de contrôle : un commit chacun, `.gitignore`, arborescence

### Étape 1 — Validation des fichiers (section 5.6)

- Responsable : Amine
- Relecteur : Ethan
- Fichier : `reconfort/validation.py`
- Quoi : vérifier, **avant** de lancer la simulation, tout ce que liste la
  section 5.6. `reconfort_io.py` ne vérifie que `format` et `version` ; le
  reste est à nous :
  - champs obligatoires présents et du bon type ;
  - grille rectangulaire et cohérente avec `dimensions` ;
  - positions dans la grille et sur le bon symbole (`R`, `A`, `D`, `P`) ;
  - identifiants de résidents uniques ;
  - scénario prévu pour cette carte, demandes adressées à des résidents
    existants ;
  - casiers dans les bornes, sans doublon, étiquettes cohérentes avec leur
    position ; `casier_depart` dans l'armoire ;
  - émotions et intensités connues, aucun mot dans deux entrées du
    dictionnaire.
- Attention : en cas d'erreur, message clair sur stderr, code de retour
  ≠ 0 et **aucun** fichier de trace écrit. Le jeu de test caché contient
  22 fichiers cassés.
- Point de contrôle : un fichier cassé par catégorie dans `tests/` ;
  code de retour ≠ 0, message sur stderr, aucune trace écrite

### Étape 2 — Simulateur : seul module qui lit `grille` et `objet`

- Responsable : Amine
- Relecteur : Ethan
- Fichier : `reconfort/simulateur.py`
- Quoi : le simulateur représente la réalité. À partir de la vraie grille
  et du vrai contenu de l'armoire, il :
  - donne au robot sa perception : le type des 4 cases voisines (`mur`,
    `libre`, `armoire`, `dictionnaire`, `resident`) ;
  - donne le contenu du casier courant quand le robot est à côté de
    l'armoire ;
  - vérifie qu'une action est légale et l'applique (section 3.4).
- Attention : le robot n'a pas le droit de lire `grille` ni `objet`
  (sections 3.2 et 3.3). C'est vérifié à la correction, et l'enfreindre
  annule les points fonctionnels. Le robot ne reçoit jamais le dictionnaire
  `carte` complet, seulement ce qu'il a le droit de savoir au départ
  (dimensions, sa position, positions de l'armoire, du dictionnaire et des
  résidents).
- Point de contrôle : aucun autre module n'accède à `grille` ni à `objet`

### Étape 3 — Structures : file, cycle (roue et colonnes de l'armoire)

- Responsable : Ethan
- Relecteur : Amine
- Fichier : `reconfort/structures.py`
- Quoi :
  - la file du parcours en largeur, sur `collections.deque` (annexe B.4) ;
  - une structure cyclique à 8 éléments pour la roue des émotions et les
    colonnes de l'armoire : voisin dans le sens horaire et antihoraire,
    distance sur le cycle (de 0 à 4).
- Point de contrôle : test du bouclage entre les colonnes 7 et 0, et de la
  distance joie ↔ tristesse = 4

### Étape 4 — Carte mentale et parcours en largeur

- Responsable : Ethan
- Relecteur : Amine
- Fichiers : `reconfort/carte_mentale.py`, `reconfort/planification.py`
- Quoi :
  - la carte mentale du robot : chaque case est inconnue, libre ou
    obstacle, et elle est mise à jour à chaque perception. Au départ, seuls
    l'armoire, le dictionnaire et les résidents sont connus (obstacles) ;
  - le parcours en largeur : plus court chemin vers n'importe quelle case
    voisine d'une cible, en supposant libres les cases inconnues
    (annexe B.5). S'il ne trouve aucun chemin, c'est la preuve que la cible
    est inaccessible (annexe B.6).
- Attention : bibliothèques de plus court chemin interdites (`networkx`,
  etc., section 7).
- Point de contrôle : annexe B.3, chemin de 7 pas, et un test où un mur
  découvert en route change le trajet

### Étape 5 — Boucle de l'agent (percevoir → mémoriser → décider → agir)

- Responsables : Ethan & Amine
- Fichiers : `reconfort/robot.py`, `agent.py`
- Quoi : le cycle du robot, à chaque tour :
  - percevoir : demander au simulateur les 4 cases voisines ;
  - mémoriser : mettre à jour la carte mentale ;
  - décider : replanifier et choisir la prochaine action ;
  - agir : exécuter l'action via le simulateur et l'écrire dans la trace.

  Ces quatre parties doivent être séparées et lisibles dans le code
  (section 7, 3 points au barème). Premier objectif : aller jusqu'au
  dictionnaire et faire `CONSULTER`.
- Point de contrôle : la trace montre le contournement d'un mur découvert
  en route

### Étapes 6 à 10 — à répartir après l'étape 5

- Étape 6 : lire l'émotion d'un message dans le dictionnaire (section 6.1)
- Étape 7 : choisir et fouiller le casier dans l'armoire (section 6.2,
  annexe C)
- Étape 8 : livrer le résident et gérer les échecs, dont le résident
  inaccessible (section 6.3)
- Étape 9 : affichage dans le terminal et vidéo de démonstration
  (section 2 bis)
- Étape 10 : nos propres cartes de test, README, `rendu.json`, rapport
  (section 11)

Le responsable écrit le code et ses tests. Le relecteur lit **tout** le code
avant la fusion : à la soutenance, chacun doit pouvoir expliquer n'importe
quelle portion, y compris celle écrite par l'autre.

#
