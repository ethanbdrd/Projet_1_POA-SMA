import unittest
from pathlib import Path

from reconfort.simulateur import *


class TestSimulateur(unittest.TestCase):
    def setUp(self) :
        carte = {
            "dimensions": {"hauteur": 5, "largeur": 7},
            "grille": [
                "#######",
                "#R.A..#",
                "#..#.P#",
                "#D....#",
                "#######",
            ],
            "depart_robot": [1, 1],
            "armoire": {"position": [1, 3]},
            "dictionnaire": {"position": [3, 1]},
            "residents": [{"id": "R1", "nom": "Camille", "position": [2, 5]}],
        }
        emotions = ["joie", "confiance", "peur", "surprise", "tristesse", "degout", "colere", "anticipation"]
        intensites = ["faible", "moyenne", "forte"]
        casiers = []
        for ligne in range(3) :
            for colonne in range(8) :
                casiers.append({"ligne": ligne, "colonne": colonne, "emotion": emotions[colonne],
                                "intensite": intensites[ligne], "objet": None})
        casiers[8]["objet"] = "photo"
        casiers[12]["objet"] = "couverture"
        armoire = {"emotions": emotions, "intensites": intensites, "casier_depart": [1, 0], "casiers": casiers}
        self.sim = Simulateur(carte, armoire)

    def test_perception_depart(self) :
        self.assertEqual(self.sim.percevoir(), {"N": "mur", "S": "libre", "E": "libre", "O": "mur"})

    def test_perception_armoire_dictionnaire_resident(self) :
        self.sim.appliquer("AVANCER", "E")
        self.assertEqual(self.sim.percevoir()["E"], "armoire")
        self.sim.position = (2, 1)
        self.assertEqual(self.sim.percevoir()["S"], "dictionnaire")
        self.sim.position = (1, 5)
        self.assertEqual(self.sim.percevoir()["S"], "resident")

    def test_avancer(self) :
        self.sim.appliquer("AVANCER", "E")
        self.assertEqual(self.sim.position, (1, 2))

    def test_avancer_illegal(self) :
        with self.assertRaises(Exception) :
            self.sim.appliquer("AVANCER", "O")
        self.assertEqual(self.sim.position, (1, 1))
        self.sim.appliquer("AVANCER", "E")
        with self.assertRaises(Exception) :
            self.sim.appliquer("AVANCER", "E")

    def test_action_inconnue(self) :
        with self.assertRaises(Exception) :
            self.sim.appliquer("VOLER")

    def test_consulter(self) :
        with self.assertRaises(Exception) :
            self.sim.appliquer("CONSULTER")
        self.sim.appliquer("AVANCER", "S")
        self.sim.appliquer("CONSULTER")

    def test_contenu_casier(self) :
        self.assertIsNone(self.sim.contenu_casier())
        self.sim.appliquer("AVANCER", "E")
        self.assertEqual(self.sim.contenu_casier(), "photo")

    def test_chercher_loin(self) :
        with self.assertRaises(Exception) :
            self.sim.appliquer("CHERCHER", "E")

    def test_chercher_bouclage_colonnes(self) :
        self.sim.appliquer("AVANCER", "E")
        self.sim.appliquer("CHERCHER", "O")
        self.assertEqual(self.sim.casier, (1, 7))
        self.sim.appliquer("CHERCHER", "E")
        self.assertEqual(self.sim.casier, (1, 0))

    def test_chercher_lignes_ne_bouclent_pas(self) :
        self.sim.appliquer("AVANCER", "E")
        self.sim.appliquer("CHERCHER", "N")
        with self.assertRaises(Exception) :
            self.sim.appliquer("CHERCHER", "N")
        self.sim.appliquer("CHERCHER", "S")
        self.sim.appliquer("CHERCHER", "S")
        with self.assertRaises(Exception) :
            self.sim.appliquer("CHERCHER", "S")

    def test_prendre(self) :
        self.sim.appliquer("AVANCER", "E")
        for i in range(4) :
            self.sim.appliquer("CHERCHER", "E")
        self.assertEqual(self.sim.contenu_casier(), "couverture")
        self.sim.appliquer("PRENDRE", "couverture")
        self.assertEqual(self.sim.objetPorte, "couverture")
        with self.assertRaises(Exception) :
            self.sim.appliquer("PRENDRE", "couverture")

    def test_prendre_illegal(self) :
        self.sim.appliquer("AVANCER", "E")
        with self.assertRaises(Exception) :
            self.sim.appliquer("PRENDRE", "couverture")
        self.sim.appliquer("CHERCHER", "E")
        with self.assertRaises(Exception) :
            self.sim.appliquer("PRENDRE", "plaid")

    def test_donner(self) :
        self.sim.appliquer("AVANCER", "E")
        for i in range(4) :
            self.sim.appliquer("CHERCHER", "E")
        self.sim.appliquer("PRENDRE", "couverture")
        with self.assertRaises(Exception) :
            self.sim.appliquer("DONNER", "couverture", "R1")
        for direction in ("S", "S", "E", "E", "N") :
            self.sim.appliquer("AVANCER", direction)
        with self.assertRaises(Exception) :
            self.sim.appliquer("DONNER", "couverture", "R9")
        self.sim.appliquer("DONNER", "couverture", "R1")
        self.assertIsNone(self.sim.objetPorte)

    def test_dessiner(self) :
        lignes = self.sim.dessiner().split("\n")
        self.assertEqual(lignes[1], "#R.A..#")
        self.sim.appliquer("AVANCER", "E")
        lignes = self.sim.dessiner().split("\n")
        self.assertEqual(lignes[1], "#.RA..#")

    def test_infos_initiales(self) :
        infos = self.sim.infos_initiales()
        self.assertNotIn("grille", infos)
        for etiquette in infos["etiquettes"] :
            self.assertNotIn("objet", etiquette)
        infos["residents"].clear()
        self.assertEqual(len(self.sim.infos_initiales()["residents"]), 1)

    def test_etancheite(self) :
        autorises = ["simulateur.py", "validation.py", "reconfort_io.py"]
        for fichier in Path("reconfort").glob("*.py") :
            if fichier.name not in autorises :
                texte = fichier.read_text(encoding="utf-8")
                self.assertNotIn('"grille"', texte, fichier.name)
                self.assertNotIn('"objet"', texte, fichier.name)


if __name__ == "__main__" :
    unittest.main()