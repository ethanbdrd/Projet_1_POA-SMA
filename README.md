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
carte mentale, planification, dictionnaire, armoire, robot), vérifient
qu'aucun module de l'agent ne lit `grille` ou `objet`, et lancent des
scénarios complets dont la trace est rejouée pas à pas sur un simulateur
neuf.

Nos propres jeux de test :

| Fichiers                                                  | Ce qu'ils testent                                                                                  |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `appartement_06` + `scenario_06`                          | grand labyrinthe (15 × 21), 4 résidents, 9 demandes dont une sans émotion reconnue                 |
| `appartement_07` + `scenario_07`                          | résident muré, demandé deux fois                                                                   |
| `appartement_01` + `scenario_08` + `armoire_colonne_vide` | armoire à colonnes vides : les 4 niveaux de repli (`aucun`, `intensite`, `voisine_1`, `voisine_2`) |

## Organisation du code

| Fichier                                      | Rôle                                                                                                                 |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `agent.py`                                   | point d'entrée : charge et valide les fichiers, crée le simulateur et le robot, exécute les demandes, écrit la trace |
| `reconfort/reconfort_io.py`                  | fourni : lecture des fichiers, normalisation des messages, écriture de la trace                                      |
| `reconfort/validation.py`                    | vérifications des fichiers d'entrée (section 5.6), avant toute simulation                                            |
| `reconfort/simulateur.py`                    | la réalité : seul module qui lit la grille et les objets ; applique les actions et refuse les actions illégales      |
| `reconfort/robot.py`                         | l'agent : boucle de décision d'une demande ; toute action passe par `agir`, qui la journalise                        |
| `reconfort/carte_mentale.py`                 | ce que le robot sait de l'appartement, mis à jour à chaque perception                                                |
| `reconfort/planification.py`                 | plus court chemin (parcours en largeur), hypothèse optimiste sur les cases inconnues                                 |
| `reconfort/structures.py`                    | file (parcours en largeur) et cycle (colonnes de l'armoire qui bouclent)                                             |
| `reconfort/dictionnaire.py`                  | lecture de l'émotion d'un message                                                                                    |
| `reconfort/armoire.py`                       | ordre de fouille des casiers (replis), trajet du sélecteur, mémoire des casiers vus                                  |
| `reconfort/affichage.py`, `demo_visuelle.py` | affichage du robot et de sa carte mentale dans le terminal (utilisé pour la vidéo)                                   |
| `tests/`                                     | tests unitaires, tests de bout en bout, outil de rejeu de trace (`outils_rejeu.py`)                                  |
| `cartes/`, `donnees/`                        | jeux fournis et nos propres jeux de test                                                                             |

## État

**Ce qui marche :**

Validation complète des fichiers d'entrée ; simulation
de toutes les actions ; déplacement avec découverte des murs et
replanification à chaque pas ; lecture de l'émotion ; fouille de l'armoire
avec les quatre niveaux de repli ; livraison. Les cinq jeux fournis sont
entièrement réussis (29 demandes sur 29). Sur nos trois jeux, 16 demandes
sur 19 réussissent ; les 3 échecs sont voulus (message sans émotion
reconnue, résident muré). Toutes les traces se rejouent sans erreur.

**Ce qui ne marche pas :**

- La négation est ignorée : « je ne suis pas triste » est lu comme de la
  tristesse, car la lecture s'arrête au premier mot reconnu.
- Le sélecteur de l'armoire repasse parfois devant des casiers qu'il sait
  déjà vides, car le trajet est calculé casier par casier.
- Le robot va voir chaque résident avant d'aller à l'armoire la première
  fois, pour ne jamais garder un objet qu'il ne pourrait pas donner : ce
  détour coûte environ 10 % de pas en plus sur les jeux fournis.
- Le robot n'a pas été essayé sur les jeux cachés de la correction.

Ces points sont analysés dans le rapport.

## Répartition du travail

- **EL KAMEL Mohamed Amine** : validation des fichiers, simulateur, lecture
  de l'émotion, fouille de l'armoire, jeux de test, tests de bout en bout
  et rejeu de trace, README.
- **BAUDRAND Ethan** : structures, carte mentale, plus court chemin,
  planification, robot, affichage, vidéo.

Chacun a écrit les tests de ses modules et a relu le code de l'autre avant
chaque fusion.

## Vidéo

`demo.mov`, à la racine du dépôt, également déclarée dans `rendu.json`.
