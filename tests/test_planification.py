import unittest

from reconfort.planification import *
from reconfort.carte_mentale import *
from reconfort.planification import _reconstruire


class TestPlanification(unittest.TestCase):

    def setUp(self):
        self.grille = [
            "######",
            "#R.#.#",
            "#.#..#",
            "#...##",
            "######",
        ]

    def test_cases_voisines(self):
        self.assertEqual(cases_voisines((1,1)), [(0,1),(2,1),(1,2),(1,0)])
        self.assertEqual(cases_voisines((0,0)), [(-1,0),(1,0),(0,1),(0,-1)])

    def test_direction_entre(self):
        self.assertEqual(direction_entre((1,1),(1,2)), "E")
        self.assertEqual(direction_entre((0,0),(-1,0)), "N")
        self.assertEqual(direction_entre((1,0),(2,0)), "S")
        self.assertEqual(direction_entre((0,1),(0,0)), "O")
        with self.assertRaises(Exception):
            direction_entre((1,1),(3,1))
        with self.assertRaises(Exception):
            direction_entre((0,0),(1,1))
    def test_reconstruire(self):
        predecesseur = {
            (1, 1): None,
            (2, 1): (1, 1),
            (3, 1): (2, 1),
            (3, 2): (3, 1),
            (3, 3): (3, 2),
            (2, 3): (3, 3),
            (2, 4): (2, 3),
            (1, 4): (2, 4),
        }
        self.assertEqual(_reconstruire(predecesseur, (1,4)), [(1,1),(2,1),(3,1),(3,2),(3,3),(2,3),(2,4),(1,4)])
        self.assertEqual(_reconstruire(predecesseur, (1,1)), [(1,1)])
        self.assertEqual(_reconstruire(predecesseur, (3,2)), [(1,1),(2,1),(3,1),(3,2)])

    def test_predicat_optimiste(self):
        est_traversable = predicat_optimiste(CarteMentale(5, 6, (1,1), (2,2), (3,4), []))
        self.assertTrue(est_traversable((1,2)))
        self.assertTrue(est_traversable((1,1)))
        self.assertFalse(est_traversable((0,0)))
        self.assertFalse(est_traversable((2,2)))
        self.assertFalse(est_traversable((3,4)))
        self.assertFalse(est_traversable((9,9)))

    def predicat(self, grille):
        def est_traversable(case):
            ligne, colonne = case
            if not (0 <= ligne < len(grille) and 0 <= colonne < len(grille[0])):
                return False
            return grille[ligne][colonne] != "#"

        return est_traversable

    def test_plus_court_chemin(self):
        est_traversable = self.predicat(self.grille)
        self.assertEqual(plus_court_chemin((1,1), {(1,4)}, est_traversable), [(1,1),(2,1),(3,1),(3,2),(3,3),(2,3),(2,4),(1,4)])
        self.assertEqual(plus_court_chemin((1,1),{(1,1)}, est_traversable), [(1,1)])
        self.assertEqual(plus_court_chemin((1,1),{(2,2)}, est_traversable), None)
        self.assertEqual(plus_court_chemin((1,1),set(), est_traversable), None)
        self.assertEqual(plus_court_chemin((1, 1), {(1, 4),(2,3)}, est_traversable),[(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3)])


    def test_replanification(self):
        carte_mentale = CarteMentale(5, 6, (1,1), (2,2), (3,4), [])
        est_traversable = predicat_optimiste(carte_mentale)
        self.assertEqual(plus_court_chemin((1,2),{(1,4)}, est_traversable), [(1,2),(1,3),(1,4)])
        carte_mentale.mettre_a_jour((1,2), {"N": "mur", "S": "armoire", "E": "mur", "O": "libre"})
        self.assertEqual(plus_court_chemin((1,2),{(1,4)}, est_traversable),[(1, 2), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (2, 4), (1, 4)])
