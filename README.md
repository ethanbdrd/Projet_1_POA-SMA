# Robot de réconfort — EL KAMEL Mohamed Amine & BAUDRAND Ethan

Projet de semestre, master informatique. Un robot à perception locale
consulte un dictionnaire, fouille une armoire et rapporte un objet à un
résident.

Langage : Python — Version : 3.9 ou plus

## Lancer

```
python agent.py <carte.json> <scenario.json> <dossier_donnees> <trace_sortie.json>
```

Exemple :

```
python agent.py cartes/appartement_01.json cartes/scenario_01.json donnees sortie.json
```

Dépendances : aucune, seulement la bibliothèque standard de Python.

Si un fichier est absent ou invalide, l'agent affiche un message d'erreur
sur la sortie d'erreur, renvoie un code non nul et n'écrit aucune trace.

## Tester

```
python -m unittest discover tests
```

Les tests couvrent chaque module (validation, simulateur, structures,
carte mentale, planification, dictionnaire, armoire, robot) ainsi que des
tests de bout en bout : sur nos propres cartes, ils lancent un scénario
complet, vérifient le résultat de chaque demande, puis rejouent la trace
pas à pas sur un simulateur neuf pour prouver qu'elle est valide.

## Organisation du code

| Fichier                      | Rôle                                                                                                                        |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `agent.py`                   | point d'entrée : charge et valide les fichiers, crée le simulateur et le robot, exécute les demandes, écrit la trace        |
| `reconfort/reconfort_io.py`  | fourni : lecture des fichiers JSON, normalisation des messages, écriture de la trace                                        |
| `reconfort/validation.py`    | toutes les vérifications de la section 5.6, avant la simulation                                                             |
| `reconfort/simulateur.py`    | la réalité : seul module qui lit la grille et le contenu des casiers ; applique les actions et refuse les actions illégales |
| `reconfort/robot.py`         | l'agent : boucle de décision d'une demande (dictionnaire, émotion, armoire, résident), journalisation de chaque pas         |
| `reconfort/carte_mentale.py` | ce que le robot sait de l'appartement, mis à jour à chaque perception                                                       |
| `reconfort/planification.py` | plus court chemin (parcours en largeur) sur la carte mentale                                                                |
| `reconfort/structures.py`    | structures utilitaires : file (pour le parcours en largeur) et cycle (colonnes de l'armoire qui bouclent)                   |
| `reconfort/dictionnaire.py`  | lecture de l'émotion d'un message (index des mots construit une seule fois)                                                 |
| `reconfort/armoire.py`       | ordre de fouille des casiers (replis), trajet du sélecteur, mémoire des casiers déjà vus                                    |
| `tests/`                     | tests unitaires de chaque module, tests de bout en bout et outil partagé de rejeu de trace (`outils_rejeu.py`)              |
| `cartes/`, `donnees/`        | jeux fournis (`appartement_01` à `05`) et nos propres jeux de test (voir ci-dessous)                                        |

### Nos jeux de test

| Fichiers                                                  | Ce qu'ils testent                                                                                         |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `appartement_06` + `scenario_06`                          | grand labyrinthe (15 × 21), 4 résidents, 9 demandes dont une sans émotion reconnue                        |
| `appartement_07` + `scenario_07`                          | résident muré : le robot conclut qu'il est inaccessible avant de prendre un objet                         |
| `appartement_01` + `scenario_08` + `armoire_colonne_vide` | armoire avec des colonnes vides : les 4 niveaux de repli (`aucun`, `intensite`, `voisine_1`, `voisine_2`) |

## Choix de conception

- **Étanchéité:** Le robot ne reçoit que les informations autorisées
  (`infos_initiales`, une copie sans la grille ni les objets). Il découvre
  les murs par ses perceptions et le contenu des casiers en se plaçant
  devant l'armoire. Un test vérifie qu'aucun autre module ne lit `grille`
  ou `objet`.
- **Planification optimiste:** Une case inconnue est supposée libre. Le
  robot recalcule le plus court chemin à chaque pas : dès qu'un mur est
  découvert sur sa route, il prend un détour. Si aucun chemin n'existe même
  en supposant les cases inconnues libres, la cible est prouvée
  inaccessible.
- **Mémoire entre les demandes:** La carte mentale et la mémoire de
  l'armoire sont conservées d'une demande à l'autre : les demandes
  suivantes coûtent moins de pas.
- **Ordre de vérification:** Le robot vérifie que le résident est
  accessible avant d'aller à l'armoire, pour ne jamais garder un objet en
  main qu'il ne pourrait pas donner.
- **Motifs d'échec:** En plus de « emotion indeterminee », « armoire vide »
  et « resident inaccessible », nous utilisons « dictionnaire inaccessible »
  et « armoire inaccessible » quand ces éléments ne peuvent pas être
  atteints.

## État

**Ce qui marche:** Validation complète des fichiers d'entrée ; simulation
de toutes les actions ; déplacement avec découverte des murs et
replanification ; lecture de l'émotion ; fouille de l'armoire avec les
replis ; livraison ; écriture d'une trace qui se rejoue sans erreur sur nos
trois jeux de test.

## Vidéo

_À compléter_ : `demo.mp4` (ou le lien), également déclarée dans
`rendu.json`.
