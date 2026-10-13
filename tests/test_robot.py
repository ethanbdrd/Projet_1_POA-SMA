import unittest

from reconfort import reconfort_io as rio
from reconfort.robot import Robot
from reconfort.simulateur import Simulateur

EMOTIONS = ["joie", "confiance", "peur", "surprise",
            "tristesse", "degout", "colere", "anticipation"]
INTENSITES = ["faible", "moyenne", "forte"]

GRILLE = [
    "#######",
    "#R.A..#",
    "#..#.P#",
    "#D....#",
    "#######",
]



def carte_de_test(grille=None):
    grille = grille or GRILLE
    return {
        "nom": "carte_de_test",
        "dimensions": {"hauteur": len(grille), "largeur": len(grille[0])},
        "grille": grille,
        "depart_robot": [1, 1],
        "armoire": {"position": [1, 3]},
        "dictionnaire": {"position": [3, 1]},
        "residents": [{"id": "R1", "nom": "Camille", "position": [2, 5]}],
    }


def armoire_de_test(garnis):
    casiers = []
    for ligne, intensite in enumerate(INTENSITES):
        for colonne, emotion in enumerate(EMOTIONS):
            casiers.append({
                "ligne": ligne,
                "colonne": colonne,
                "emotion": emotion,
                "intensite": intensite,
                "objet": garnis.get((ligne, colonne)),
            })
    return {
        "emotions": EMOTIONS,
        "intensites": INTENSITES,
        "casier_depart": [1, 0],
        "casiers": casiers,
    }


def dictionnaire_de_test():
    return {
        "emotions": EMOTIONS,
        "intensites": INTENSITES,
        "entrees": [
            {"formes": ["triste"], "emotion": "tristesse", "intensite": "moyenne"},
        ],
    }


class TestRobot(unittest.TestCase):

    def setUp(self):
        self.dictionnaire = dictionnaire_de_test()
        self.preparer()

    def preparer(self, garnis=None, grille=None):
        if garnis is None:
            garnis = {(1, 4): "couverture"}
        self.carte = carte_de_test(grille)
        self.armoire = armoire_de_test(garnis)
        self.simulateur = Simulateur(self.carte, self.armoire)
        self.trace = rio.Trace(self.carte["nom"], "scenario_de_test", ["Ethan", "Amine"])
        self.robot = Robot(self.simulateur.infos_initiales(), self.simulateur,
                           self.trace, self.dictionnaire)
        self.robot.demande = 1

    def fouille(self, garnis):
        self.preparer(garnis)
        self.robot.aller_a((1, 3))
        return self.robot.fouiller("tristesse", "moyenne")

    def test_perception(self):
        perception = self.robot.percevoir()
        self.assertEqual(perception, {"N": "mur", "S": "libre", "E": "libre", "O": "mur"})
        self.assertEqual(self.robot.carte.type_de((1, 2)), "libre")

    def test_agir_journalise_un_pas(self):
        self.robot.percevoir()
        self.robot.agir("ATTENDRE")

        pas = self.trace.pas[0]
        self.assertEqual(len(self.trace.pas), 1)
        self.assertEqual(pas["position"], [1, 1])
        self.assertEqual(pas["casier"], [1, 0])
        self.assertEqual(pas["action"], "ATTENDRE")
        self.assertIsNone(pas["contenu_casier"])
        self.assertEqual(pas["perception"], {"N": "mur", "S": "libre", "E": "libre", "O": "mur"})

    def test_aller_a(self):
        self.assertTrue(self.robot.aller_a((3, 1)))
        self.assertEqual(self.simulateur.position, (2, 1))

    def test_fouiller(self):
        self.assertEqual(self.fouille({(1, 4): "couverture"}),
                         ((1, 4), "couverture", "aucun"))
        self.assertEqual(self.fouille({(0, 4): "plaid", (2, 4): "chale"}),
                         ((0, 4), "plaid", "intensite"))
        self.assertEqual(self.fouille({(1, 5): "savon", (1, 3): "ballon"}),
                         ((1, 5), "savon", "voisine_1"))
        self.assertEqual(self.fouille({(1, 2): "balle", (1, 4): "couverture"}),
                         ((1, 4), "couverture", "aucun"))
        self.assertIsNone(self.fouille({}))

    def test_executer_demande(self):
        self.robot.executer_demande(1, "R1", "je suis triste ce soir")
        self.robot.executer_demande(2, "R1", "je suis triste ce soir")

        self.assertEqual(len(self.trace.livraisons), 2)
        for livraison in self.trace.livraisons:
            self.assertTrue(livraison["succes"], livraison["motif_echec"])
            self.assertEqual(livraison["emotion"], "tristesse")
            self.assertEqual(livraison["intensite"], "moyenne")
            self.assertEqual(livraison["casier_choisi"], [1, 4])
            self.assertEqual(livraison["repli"], "aucun")
            self.assertEqual(livraison["objet"], "couverture")
        self.assertIsNone(self.simulateur.objetPorte)

        actions = [pas["action"] for pas in self.trace.pas]
        self.assertEqual(actions.count("CONSULTER"), 2)
        self.assertEqual(actions.count("PRENDRE"), 2)
        self.assertEqual(actions.count("DONNER"), 2)
        self.assertIn("R1", self.robot.residents_atteints)

    def test_echecs(self):
        self.robot.executer_demande(1, "R1", "bonjour comment allez vous")
        self.assertEqual(self.trace.livraisons[0]["motif_echec"], "emotion indeterminee")

        self.preparer({})
        self.robot.executer_demande(1, "R1", "je suis triste")
        self.assertEqual(self.trace.livraisons[0]["motif_echec"], "armoire vide")

        for livraison in self.trace.livraisons:
            self.assertFalse(livraison["succes"])

    def test_executer_demande_resident_inaccessible(self):
        grille = [
            "#######",
            "#R.A.##",
            "#..##P#",
            "#D...##",
            "#######",
        ]
        self.preparer(grille=grille)
        self.robot.executer_demande(1, "R1", "je suis triste ce soir")
        self.robot.executer_demande(2, "R1", "je suis triste ce soir")

        self.assertEqual(self.trace.livraisons[0]["motif_echec"], "resident inaccessible")
        self.assertEqual(len(self.trace.livraisons), 2)
        actions = [pas["action"] for pas in self.trace.pas]
        self.assertEqual(actions.count("PRENDRE"), 0)


    def test_rejeu_de_la_trace(self):
        self.robot.executer_demande(1, "R1", "je suis triste ce soir")

        resident_de = {l["demande"]: l["resident"] for l in self.trace.livraisons}
        simulateur = Simulateur(self.carte, self.armoire)

        for pas in self.trace.pas:
            repere = "pas t=%d (%s)" % (pas["t"], pas["action"])
            self.assertEqual(tuple(pas["position"]), simulateur.position, repere)
            self.assertEqual(tuple(pas["casier"]), simulateur.casier, repere)
            self.assertEqual(pas["perception"], simulateur.percevoir(), repere)
            self.assertEqual(pas["contenu_casier"], simulateur.contenu_casier(), repere)
            simulateur.appliquer(pas["action"], pas["argument"],
                                 resident_de.get(pas["demande"]))

        self.assertIsNone(simulateur.objetPorte)


if __name__ == "__main__":
    unittest.main()
