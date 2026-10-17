# Usage : demo_visuelle.py <carte.json> <scenario.json> <dossier_donnees>

from pathlib import Path
from agent import charger_et_valider
from reconfort.affichage import image
from reconfort.robot import Robot
from reconfort import reconfort_io as rio

from reconfort.simulateur import Simulateur
from reconfort.reconfort_io import Trace
import time, sys

from reconfort.validation import ErreurValidation

VITESSE = 0.3

class RobotVisible(Robot) :
    def agir(self, action, argument=None, resident=None, commentaire=None):
        super().agir(action, argument, resident, commentaire)
        print("\033[H\033[2J", end="")
        print(image(self.simulateur, self))
        time.sleep(VITESSE)

def main(argv):
    if len(argv)!=4:
        print("Usage : demo_visuelle.py <carte.json> <scenario.json> <dossier_donnees>", file=sys.stderr)
        return 2

    chemin_carte = Path(argv[1])
    chemin_scenario = Path(argv[2])
    dossier_donnees = Path(argv[3])

    try:
        carte, scenario, dictionnaire, armoire  =charger_et_valider(chemin_carte, chemin_scenario, dossier_donnees)
    except (rio.ErreurFichier, ErreurValidation) as erreur :
        print("erreur : " + str(erreur), file=sys.stderr)
        return 1

    simulateur = Simulateur(carte, armoire)
    trace = Trace(carte["nom"], scenario["nom"], ["BAUDRAND Ethan", "EL KAMEL Mohamed Amine"])
    robot = RobotVisible(simulateur.infos_initiales(), simulateur ,trace, dictionnaire)

    print("\033[H\033[2J", end="")
    print(image(simulateur, robot))
    time.sleep(VITESSE)

    for demande in scenario["demandes"]:
        robot.executer_demande(demande["numero"], demande["resident"], demande["message"])

    print()
    for livraison in trace.livraisons:
        livraison_echec = ""
        if not livraison["succes"]:
            livraison_echec = str("avec pour motif "+livraison["motif_echec"]+" et la solution de repli a été : "+livraison["repli"])
        print("livraison n°",livraison["demande"],"pour le résident" ,livraison["resident"],"; Il a une ", livraison["emotion"], livraison["intensite"],"; Le robot lui a donné un(e)", livraison["objet"], "trouvé dans l'armoire en", livraison["casier_choisi"],"; Cette livraison est un", "succès" if livraison["succes"] else "echec",livraison_echec )


    dico_trace = trace.en_dictionnaire()
    resume = dico_trace["resume"]
    print()
    print(resume["demandes"],"demandes dont" ,resume["reussies"], "réussis et", resume["echecs"], "échouées en", resume["pas_total"], "pas au total.")

    return 0

if __name__ == "__main__" :
    raise SystemExit(main(sys.argv))











