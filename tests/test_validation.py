import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from reconfort import reconfort_io as rio
from reconfort.validation import *


class TestValidation(unittest.TestCase):
    def setUp(self) :
        self.carte = rio.charger_carte("cartes/appartement_01.json")
        self.scenario = rio.charger_scenario("cartes/scenario_01.json")
        self.dictionnaire = rio.charger_dictionnaire("donnees/dictionnaire.json")
        self.armoire = rio.charger_armoire("donnees/armoire_standard.json")

    def test_fichiers_valides(self) :
        valider_carte(self.carte)
        valider_scenario(self.scenario, self.carte)
        valider_dictionnaire(self.dictionnaire)
        valider_armoire(self.armoire, self.dictionnaire)

    def test_version(self) :
        self.carte["version"] = True
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)
        self.carte["version"] = 2
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_champ_absent(self) :
        del self.carte["residents"]
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_mauvais_type(self) :
        self.carte["dimensions"]["hauteur"] = "9"
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_grille_non_rectangulaire(self) :
        self.carte["grille"][1] += "."
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_dimensions_incoherentes(self) :
        self.carte["dimensions"]["largeur"] = 14
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_symbole_inconnu(self) :
        self.carte["grille"][1] = "#X" + self.carte["grille"][1][2:]
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_bord_troue(self) :
        self.carte["grille"][1] = "." + self.carte["grille"][1][1:]
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_position_hors_grille(self) :
        self.carte["depart_robot"] = [20, 1]
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_depart_pas_sur_R(self) :
        self.carte["depart_robot"] = [1, 1]
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_armoire_mal_placee(self) :
        self.carte["armoire"]["position"] = [1, 1]
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_dictionnaire_mal_place(self) :
        self.carte["dictionnaire"]["position"] = [1, 1]
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_resident_sur_un_mur(self) :
        self.carte["residents"][0]["position"] = [0, 0]
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_residents_meme_id(self) :
        self.carte["residents"][1]["id"] = self.carte["residents"][0]["id"]
        with self.assertRaises(ErreurValidation) :
            valider_carte(self.carte)

    def test_scenario_autre_carte(self) :
        self.scenario["carte"] = "appartement_99"
        with self.assertRaises(ErreurValidation) :
            valider_scenario(self.scenario, self.carte)

    def test_resident_inconnu(self) :
        self.scenario["demandes"][0]["resident"] = "R99"
        with self.assertRaises(ErreurValidation) :
            valider_scenario(self.scenario, self.carte)

    def test_numero_en_double(self) :
        self.scenario["demandes"][1]["numero"] = self.scenario["demandes"][0]["numero"]
        with self.assertRaises(ErreurValidation) :
            valider_scenario(self.scenario, self.carte)

    def test_emotion_inconnue(self) :
        self.dictionnaire["entrees"][0]["emotion"] = "nostalgie"
        with self.assertRaises(ErreurValidation) :
            valider_dictionnaire(self.dictionnaire)

    def test_intensite_inconnue(self) :
        self.dictionnaire["entrees"][0]["intensite"] = "extreme"
        with self.assertRaises(ErreurValidation) :
            valider_dictionnaire(self.dictionnaire)

    def test_mot_dans_deux_entrees(self) :
        self.dictionnaire["entrees"][1]["formes"].append(self.dictionnaire["entrees"][0]["formes"][0])
        with self.assertRaises(ErreurValidation) :
            valider_dictionnaire(self.dictionnaire)

    def test_mot_repete_dans_une_entree(self) :
        formes = self.dictionnaire["entrees"][0]["formes"]
        formes.append(formes[0])
        with self.assertRaises(ErreurValidation) :
            valider_dictionnaire(self.dictionnaire)

    def test_forme_pas_une_chaine(self) :
        self.dictionnaire["entrees"][0]["formes"].append(42)
        with self.assertRaises(ErreurValidation) :
            valider_dictionnaire(self.dictionnaire)

    def test_casier_hors_armoire(self) :
        self.armoire["casiers"][0]["ligne"] = 3
        with self.assertRaises(ErreurValidation) :
            valider_armoire(self.armoire, self.dictionnaire)

    def test_casier_en_double(self) :
        self.armoire["casiers"].append(dict(self.armoire["casiers"][0]))
        with self.assertRaises(ErreurValidation) :
            valider_armoire(self.armoire, self.dictionnaire)

    def test_casier_manquant(self) :
        self.armoire["casiers"].pop()
        with self.assertRaises(ErreurValidation) :
            valider_armoire(self.armoire, self.dictionnaire)

    def test_etiquette_incoherente(self) :
        self.armoire["casiers"][0]["emotion"] = "colere"
        with self.assertRaises(ErreurValidation) :
            valider_armoire(self.armoire, self.dictionnaire)

    def test_casier_depart_hors_armoire(self) :
        self.armoire["casier_depart"] = [1, 8]
        with self.assertRaises(ErreurValidation) :
            valider_armoire(self.armoire, self.dictionnaire)


class TestAgent(unittest.TestCase):
    def lancer(self, chemin_carte) :
        dossier = Path(tempfile.mkdtemp())
        trace = dossier / "trace.json"
        resultat = subprocess.run(
            [sys.executable, "agent.py", str(chemin_carte), "cartes/scenario_01.json", "donnees", str(trace)],
            capture_output=True, text=True, encoding="utf-8")
        return resultat, trace

    def test_fichiers_valides(self) :
        resultat, trace = self.lancer("cartes/appartement_01.json")
        self.assertEqual(resultat.returncode, 0, resultat.stderr)

    def test_fichier_absent(self) :
        resultat, trace = self.lancer("cartes/inexistant.json")
        self.assertNotEqual(resultat.returncode, 0)
        self.assertNotEqual(resultat.stderr.strip(), "")
        self.assertNotIn("Traceback", resultat.stderr)
        self.assertFalse(trace.exists())

    def test_carte_invalide(self) :
        carte = rio.charger_carte("cartes/appartement_01.json")
        carte["grille"][1] = "." + carte["grille"][1][1:]
        chemin = Path(tempfile.mkdtemp()) / "carte.json"
        chemin.write_text(json.dumps(carte), encoding="utf-8")
        resultat, trace = self.lancer(chemin)
        self.assertNotEqual(resultat.returncode, 0)
        self.assertIn("murs", resultat.stderr)
        self.assertNotIn("Traceback", resultat.stderr)
        self.assertFalse(trace.exists())


if __name__ == "__main__" :
    unittest.main()
