import unittest

from reconfort.structures import *

class TestFile(unittest.TestCase):
    def setUp(self) :
        self.file = File()

    def test_init(self) :
        self.assertTrue(self.file.est_vide())

    def test_defiler_vide_exception(self) :
        with self.assertRaises(Exception) :
            self.file.defiler()

    def test_enfiler_defiler_len(self) :
        self.assertTrue(self.file.est_vide())
        self.file.enfiler("1")
        self.assertEqual(self.file.taille, len(self.file))
        self.file.enfiler("2")
        self.assertFalse(self.file.est_vide())
        self.assertEqual(self.file.taille, len(self.file))
        self.assertEqual(self.file.defiler(), "1")
        self.assertEqual(self.file.taille, len(self.file))
        self.assertEqual(self.file.defiler(), "2")
        self.assertEqual(self.file.taille, self.file.__len__())
        self.assertTrue(self.file.est_vide())


class TestCycle(unittest.TestCase):
    def setUp(self) :
        self.Cycle = Cycle(["joie", "confiance", "peur", "surprise", "tristesse", "degout", "colere", "anticipation"])

    def test_init(self) :
        with self.assertRaises(Exception) :
            self.CycleVide = Cycle("2")
        with self.assertRaises(Exception) :
            self.CycleDoublon = Cycle([1,2,3,2])

        self.assertEqual(self.Cycle.tailleRoue,8)

    def test_indice(self):
        with self.assertRaises(Exception) :
            self.Cycle.indice("???")
        self.assertEqual(self.Cycle.indice("joie"),0)

    def test_element(self):
        self.assertEqual(self.Cycle.element(0),"joie")

    def test_suivant(self):
        self.assertEqual(self.Cycle.suivant("anticipation"),"joie")

    def test_precedant(self):
        self.assertEqual(self.Cycle.precedent("joie"),"anticipation")

    def test_distance(self):
        self.assertEqual(self.Cycle.distance("joie", "surprise"),3)
        self.assertEqual(self.Cycle.distance("joie", "degout"),3)

    def test_distance_egale(self):
        self.assertEqual(self.Cycle.pas("joie", "tristesse"),(4,"H"))

    def test_distance_nulle(self):
        self.assertEqual(self.Cycle.pas("joie", "joie"),(0,"H"))

    def test_pas(self):
        self.assertEqual(self.Cycle.pas("joie", "colere"),(2,"A"))

    def test_sens(self):
        self.assertEqual(self.Cycle.sens("joie", "surprise"),"H")
        self.assertEqual(self.Cycle.sens("joie", "degout"),"A")

if __name__ == "__main__" :
    unittest.main()