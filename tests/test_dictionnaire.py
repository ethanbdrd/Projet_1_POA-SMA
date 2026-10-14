import unittest

from reconfort.dictionnaire import *
import reconfort.dictionnaire as module_dictionnaire

class TestDictionnaire(unittest.TestCase):
    def setUp(self) :
        self.dictionnaire = {
            "entrees": [
                {"formes": ["seul", "seule"], "emotion": "tristesse", "intensite": "moyenne"},
                {"formes": ["inquiet", "inquiete"], "emotion": "peur", "intensite": "faible"},
                {"formes": ["terrifie", "terrifiee"], "emotion": "peur", "intensite": "forte"},
                {"formes": ["heureux", "heureuse"], "emotion": "joie", "intensite": "moyenne"},
            ]
        }

    def test_construire_index(self) :
        index = construire_index(self.dictionnaire)
        self.assertEqual(index["seule"], ("tristesse", "moyenne"))
        self.assertEqual(index["inquiet"], ("peur", "faible"))
        self.assertEqual(len(index), 8)

    def test_index_construit_une_seule_fois(self) :
        lire_emotion("seule", self.dictionnaire)
        self.assertIs(module_dictionnaire._dernier_dictionnaire, self.dictionnaire)
        premier = index_de(self.dictionnaire)
        self.assertIs(index_de(self.dictionnaire), premier)
        autre = {"entrees": [{"formes": ["calme"], "emotion": "joie", "intensite": "faible"}]}
        self.assertIsNot(index_de(autre), premier)
        self.assertEqual(lire_emotion("tres calme", autre), ("joie", "faible"))

    def test_mot_reconnu(self) :
        self.assertEqual(lire_emotion("Je me sens seule ce soir.", self.dictionnaire), ("tristesse", "moyenne"))

    def test_majuscules_et_accents(self) :
        self.assertEqual(lire_emotion("Je suis TERRIFIÉE !", self.dictionnaire), ("peur", "forte"))

    def test_ponctuation_collee(self) : #Un mot est connu meme si il est colle a un virgule
        self.assertEqual(lire_emotion("inquiet, vraiment...", self.dictionnaire), ("peur", "faible"))

    def test_premier_mot_reconnu_gagne(self) : #Toujours prendre le premier mot rencontree mm si il y 2
        message = "Je suis heureux mais un peu inquiet."
        self.assertEqual(lire_emotion(message, self.dictionnaire), ("joie", "moyenne"))
        message = "Je suis inquiet mais heureux."
        self.assertEqual(lire_emotion(message, self.dictionnaire), ("peur", "faible"))

    def test_aucun_mot_reconnu(self) : #Meme si il trouve aucune emotion il retourne None
        self.assertIsNone(lire_emotion("Il fait beau aujourd'hui.", self.dictionnaire))

    def test_message_vide(self) : # Un message vide renvoie None aussi
        self.assertIsNone(lire_emotion("", self.dictionnaire))

    def test_mot_partiel_non_reconnu(self) : # Le mot n'est pas reconnu s'il contient seulement une partie d'un mot du dictionnaire
        self.assertIsNone(lire_emotion("seulement", self.dictionnaire))


if __name__ == "__main__" :
    unittest.main()
