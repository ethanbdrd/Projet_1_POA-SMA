import unittest

from reconfort.armoire import *


class TestCandidats(unittest.TestCase):
    def setUp(self) :
        self.emotions = ["joie", "confiance", "peur", "surprise", "tristesse", "degout", "colere", "anticipation"]
        self.intensites = ["faible", "moyenne", "forte"]

    def casiers(self, emotion, intensite) :
        resultat = []
        for casier, repli in candidats(emotion, intensite, self.emotions, self.intensites) :
            resultat.append(casier)
        return resultat

    def test_quinze_candidats(self) :
        casiers = self.casiers("surprise", "forte")
        self.assertEqual(len(casiers), 15)
        self.assertEqual(len(set(casiers)), 15)

    def test_exemple_annexe_c5(self) : #Exemple dasn l'enonce avec demande de surprise / forte dont toute la colonne est vide.
        self.assertEqual(self.casiers("surprise", "forte")[:5], [(2, 3), (1, 3), (0, 3), (2, 4), (2, 2)])

    def test_premier_candidat_est_le_casier_exact(self) :
        self.assertEqual(self.casiers("tristesse", "moyenne")[0], (1, 4))

    def test_intensite_plus_faible_d_abord(self) :
        self.assertEqual(self.casiers("tristesse", "moyenne")[1:3], [(0, 4), (2, 4)])

    def test_horaire_avant_antihoraire(self) :
        self.assertEqual(self.casiers("tristesse", "moyenne")[3:5], [(1, 5), (1, 3)])

    def test_bouclage_de_la_roue(self) :
        colonnes = set()
        for ligne, colonne in self.casiers("joie", "faible") :
            colonnes.add(colonne)
        self.assertEqual(colonnes, {6, 7, 0, 1, 2})

    def test_replis(self) : #Ici on s'interesse aux emotions(colonnes)
        replis = dict(candidats("surprise", "forte", self.emotions, self.intensites))
        self.assertEqual(replis[(2, 3)], "aucun")
        self.assertEqual(replis[(1, 3)], "intensite")
        self.assertEqual(replis[(2, 4)], "voisine_1")
        self.assertEqual(replis[(0, 1)], "voisine_2")
        self.assertNotIn((0, 7), replis)


class TestTrajet(unittest.TestCase):
    def test_sur_place(self) :
        self.assertEqual(trajet((1, 4), (1, 4), 3, 8), [])

    def test_simple(self) :
        self.assertEqual(trajet((1, 0), (1, 3), 3, 8), ["E", "E", "E"])
        self.assertEqual(trajet((1, 0), (2, 0), 3, 8), ["S"])
        self.assertEqual(trajet((2, 3), (0, 3), 3, 8), ["N", "N"])

    def test_lignes_puis_colonnes(self) : #les déplacements verticaux sont faits avant les horizontaux
        self.assertEqual(trajet((1, 0), (2, 2), 3, 8), ["S", "E", "E"])

    def test_par_le_bouclage(self) :
        self.assertEqual(trajet((1, 0), (1, 7), 3, 8), ["O"])
        self.assertEqual(trajet((1, 6), (1, 1), 3, 8), ["E", "E", "E"])

    def test_egalite(self) :
        self.assertEqual(trajet((1, 0), (1, 4), 3, 8), ["E", "E", "E", "E"])

    def test_hors_armoire(self) :
        with self.assertRaises(ValueError) :
            trajet((1, 0), (3, 0), 3, 8)

    def test_depart_hors_armoire(self) :
        with self.assertRaises(ValueError) :
            trajet((3, 0), (1, 0), 3, 8)
        with self.assertRaises(ValueError) :
            trajet((1, 8), (1, 0), 3, 8)


class TestMemoireArmoire(unittest.TestCase):
    def setUp(self) :
        self.memoire = MemoireArmoire((1, 0))

    def test_init(self) :
        self.assertEqual(self.memoire.casier, (1, 0))
        self.assertFalse(self.memoire.est_connu((1, 0)))

    def test_noter_un_objet(self) :
        self.memoire.noter((1, 4), "couverture")
        self.assertTrue(self.memoire.est_connu((1, 4)))
        self.assertEqual(self.memoire.contenu((1, 4)), "couverture")

    def test_noter_un_casier_vide(self) :
        self.memoire.noter((1, 3), None)
        self.assertTrue(self.memoire.est_connu((1, 3)))
        self.assertIsNone(self.memoire.contenu((1, 3)))

    def test_casier_jamais_vu(self) :
        self.assertFalse(self.memoire.est_connu((2, 7)))
        self.assertIsNone(self.memoire.contenu((2, 7)))


if __name__ == "__main__" :
    unittest.main()
