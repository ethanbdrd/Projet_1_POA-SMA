def cote_a_cote(gauche, droite, ecart=3) :
    lignes_gauche = gauche.splitlines()
    lignes_droite = droite.splitlines()
    largeur = max((len(l) for l in lignes_gauche), default=0)
    largeur += ecart
    hauteur = max(len(lignes_gauche), len(lignes_droite))
    lignes_gauche += [""] * (hauteur - len(lignes_gauche))
    lignes_droite += [""] * (hauteur - len(lignes_droite))
    lignes = []
    for i in range(hauteur):
        lignes.append(lignes_gauche[i].ljust(largeur) + lignes_droite[i])
    return "\n".join(lignes)

def image(simulateur, robot) :
    liste = []
    if robot.trace.pas:
        dernier = robot.trace.pas[-1]
        action = dernier["action"]
    else:
        action = "depart"
    liste.append("pas %d | demande %s | %s | porte %s | casier %s" % (len(robot.trace.pas), robot.demande,action,robot.objet_porte,simulateur.casier))
    liste.append(cote_a_cote("reel" + "\n" + simulateur.dessiner(), "mémoire du robot" + "\n"+ robot.carte.dessiner(simulateur.position)))
    liste.append("? inconnu   . libre   # mur   A armoire   D dictionnaire   P resident   R robot")
    return "\n".join(liste)