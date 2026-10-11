#!/usr/bin/env python3
"""Robot de reconfort.

Usage :
    python agent.py <carte.json> <scenario.json> <dossier_donnees> <trace.json>
"""

import sys
from pathlib import Path

from reconfort import reconfort_io as rio
from reconfort.robot import Robot
from reconfort.simulateur import Simulateur
from reconfort.validation import (
    ErreurValidation,
    valider_armoire,
    valider_carte,
    valider_dictionnaire,
    valider_scenario,
)


def charger_et_valider(cheminCarte, cheminScenario, dossierDonnees) :
    carte = rio.charger_carte(cheminCarte)
    valider_carte(carte)

    scenario = rio.charger_scenario(cheminScenario)
    valider_scenario(scenario, carte)

    dictionnaire = rio.charger_dictionnaire(dossierDonnees / "dictionnaire.json")
    valider_dictionnaire(dictionnaire)

    armoire = rio.charger_armoire(dossierDonnees / (scenario["armoire"] + ".json"))
    valider_armoire(armoire, dictionnaire)

    return carte, scenario, dictionnaire, armoire


def main(argv) :
    if len(argv) != 5 :
        print(__doc__.strip(), file=sys.stderr)
        return 2

    cheminCarte = Path(argv[1])
    cheminScenario = Path(argv[2])
    dossierDonnees = Path(argv[3])
    cheminSortie = Path(argv[4])

    try :
        carte, scenario, dictionnaire, armoire = charger_et_valider(cheminCarte, cheminScenario, dossierDonnees)
    except (rio.ErreurFichier, ErreurValidation) as erreur :
        print("erreur : " + str(erreur), file=sys.stderr)
        return 1
    sim = Simulateur(carte, armoire)
    trace = rio.Trace(carte["nom"], scenario["nom"], ["BAUDRAND Ethan", "EL KAMEL Mohamed Amine"])
    robot = Robot(sim.infos_initiales(), sim, trace, dictionnaire)
    for demande in scenario["demandes"]:
        robot.executer_demande(demande["numero"], demande["resident"], demande["message"])
    trace.ecrire(cheminSortie)
    return 0



if __name__ == "__main__" :
    raise SystemExit(main(sys.argv))