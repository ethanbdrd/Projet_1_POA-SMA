import unittest

from tests.outils_rejeu import rejouer, simuler


class TestBoutEnBout(unittest.TestCase):

    def lancer(self, nom_carte, nom_scenario):
        carte, armoire, trace = simuler(nom_carte, nom_scenario)
        rejouer(self, carte, armoire, trace)
        return trace

    def echecs(self, trace):
        return {l["demande"]: l["motif_echec"] for l in trace.livraisons if not l["succes"]}

    def test_grand_labyrinthe(self):
        trace = self.lancer("appartement_06", "scenario_06")
        self.assertEqual(len(trace.livraisons), 9)
        self.assertEqual(self.echecs(trace), {7: "emotion indeterminee"})

    def test_resident_mure(self):
        trace = self.lancer("appartement_07", "scenario_07")
        self.assertEqual(self.echecs(trace), {3: "resident inaccessible", 5: "resident inaccessible"})

        actions_r2 = [p["action"] for p in trace.pas if p["demande"] in (3, 5)]
        self.assertNotIn("PRENDRE", actions_r2)

        pas_utilises = {l["demande"]: l["pas_utilises"] for l in trace.livraisons}
        self.assertLess(pas_utilises[5], pas_utilises[3])

    def test_replis(self):
        trace = self.lancer("appartement_01", "scenario_08")
        self.assertEqual(self.echecs(trace), {})

        replis = [l["repli"] for l in trace.livraisons]
        self.assertEqual(replis, ["aucun", "intensite", "voisine_1", "voisine_2"])

        objets = [l["objet"] for l in trace.livraisons]
        self.assertEqual(objets, ["photo de famille", "photo de famille", "bouton d appel", "casque audio"])


if __name__ == "__main__":
    unittest.main()
