import unittest

from reconfort.carte_mentale import *

class TestCarteMentale (unittest.TestCase):

    def setUp(self):
        self.carte_mentale = CarteMentale(4,6,(1,1),(1,2),(1,4), [(2,4)])


    def test_dessiner(self):
        attendu = "\n".join([
            "######",
            "#RA?D#",
            "#???P#",
            "######",
        ])
        self.assertEqual(self.carte_mentale.dessiner((1,1)), attendu)

    def test_dans_la_grille(self):
        self.assertTrue(self.carte_mentale.dans_la_grille((1,1)))
        self.assertFalse(self.carte_mentale.dans_la_grille((2,9)))
        self.assertFalse(self.carte_mentale.dans_la_grille((3,-2)))
        self.assertFalse(self.carte_mentale.dans_la_grille((-1, 1)))

    def test_type_de(self):
        self.assertEqual(self.carte_mentale.type_de((1,2)), ARMOIRE)
        self.assertEqual(self.carte_mentale.type_de((1,4)), DICTIONNAIRE)
        self.assertEqual(self.carte_mentale.type_de((2,4)), RESIDENT)
        self.assertEqual(self.carte_mentale.type_de((0,0)), MUR)
        self.assertEqual(self.carte_mentale.type_de((1,1)), LIBRE)
        with self.assertRaises(Exception):
            self.carte_mentale.type_de((1,7))

    def test_voisines(self):
        self.assertEqual(self.carte_mentale.voisines((1,1)), [(0,1),(2,1),(1,2),(1,0)])
        self.assertEqual(self.carte_mentale.voisines((3,5)), [(2,5),(3,4)])

    def test_mettre_a_jour(self):
        self.carte_mentale.mettre_a_jour((1,1),{"N": "mur", "S": "armoire", "E": "libre", "O": "mur"})
        self.assertEqual(self.carte_mentale.type_de((0,1)), MUR)
        self.assertEqual(self.carte_mentale.type_de((1,1)), LIBRE)
        self.assertEqual(self.carte_mentale.type_de((2,1)), ARMOIRE)
        self.assertEqual(self.carte_mentale.type_de((1,0)), MUR)
        self.assertEqual(self.carte_mentale.type_de((1,2)), LIBRE)
        self.assertEqual(self.carte_mentale.type_de((1,3)), INCONNU)

    def test_mettre_a_jour_les_quatre_directions(self):
        carte = CarteMentale(5, 7, (2,2), (1,5), (3,5), [(2,5)])
        carte.mettre_a_jour((2,2), {"N": "mur", "S": "libre", "E": "libre", "O": "mur"})
        self.assertEqual(carte.type_de((1,2)), MUR)
        self.assertEqual(carte.type_de((3,2)), LIBRE)
        self.assertEqual(carte.type_de((2,3)), LIBRE)
        self.assertEqual(carte.type_de((2,1)), MUR)
        self.assertEqual(carte.type_de((2,2)), LIBRE)
        self.assertEqual(carte.type_de((2,4)), INCONNU)

    def test_case_vue_reste_vue(self):
        carte = CarteMentale(5, 7, (2,2), (1,5), (3,5), [(2,5)])
        carte.mettre_a_jour((2,2), {"N": "mur", "S": "libre", "E": "libre", "O": "mur"})
        carte.mettre_a_jour((2,3), {"N": "mur", "S": "mur", "E": "libre", "O": "libre"})
        self.assertEqual(carte.type_de((1,2)), MUR)
        self.assertEqual(carte.type_de((2,1)), MUR)
        self.assertEqual(carte.type_de((2,2)), LIBRE)

    def test_est_connue(self):
        self.assertTrue(self.carte_mentale.est_connue((1,1)))
        self.assertFalse(self.carte_mentale.est_connue((2,1)))
        with self.assertRaises(Exception):
            self.carte_mentale.est_connue((3,7))
        with self.assertRaises(Exception):
            self.carte_mentale.est_connue((1,-2))

    def test_case_d_acces(self):
        self.assertEqual(self.carte_mentale.case_d_acces((1,1)),[(2,1)])
        self.assertEqual(self.carte_mentale.case_d_acces((3,5)),[])
        self.assertEqual(self.carte_mentale.case_d_acces((2,2)),[(2,3),(2,1)])

