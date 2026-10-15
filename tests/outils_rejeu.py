"""Outils partages par les tests de bout en bout : simuler un scenario et rejouer sa trace."""

from pathlib import Path

from agent import charger_et_valider
from reconfort import reconfort_io as rio
from reconfort.robot import Robot
from reconfort.simulateur import Simulateur


def simuler(nom_carte, nom_scenario):
    """Lance tout le scenario comme agent.py, sans ecrire de fichier, et renvoie (carte, armoire, trace)."""
    carte, scenario, dictionnaire, armoire = charger_et_valider(
        Path("cartes") / (nom_carte + ".json"),
        Path("cartes") / (nom_scenario + ".json"),
        Path("donnees"))
    simulateur = Simulateur(carte, armoire)
    trace = rio.Trace(carte["nom"], scenario["nom"], ["BAUDRAND Ethan", "EL KAMEL Mohamed Amine"])
    robot = Robot(simulateur.infos_initiales(), simulateur, trace, dictionnaire)
    for demande in scenario["demandes"]:
        robot.executer_demande(demande["numero"], demande["resident"], demande["message"])
    return carte, armoire, trace


def rejouer(test, carte, armoire, trace):
    """Rejoue chaque pas de la trace sur un simulateur neuf et verifie qu'il correspond a la realite."""
    resident_de = {l["demande"]: l["resident"] for l in trace.livraisons}
    simulateur = Simulateur(carte, armoire)

    for pas in trace.pas:
        repere = "pas t=%d (%s)" % (pas["t"], pas["action"]) #si pas["t"]=600 et pas["action"]="CONSULTER" donc donne "pas t=868 (CONSULTER)"
        test.assertEqual(tuple(pas["position"]), simulateur.position, repere)
        test.assertEqual(tuple(pas["casier"]), simulateur.casier, repere)
        test.assertEqual(pas["perception"], simulateur.percevoir(), repere)
        test.assertEqual(pas["contenu_casier"], simulateur.contenu_casier(), repere)
        simulateur.appliquer(pas["action"], pas["argument"], resident_de.get(pas["demande"]))

    test.assertIsNone(simulateur.objetPorte)
