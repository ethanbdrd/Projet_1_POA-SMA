from reconfort.structures import File
from reconfort.carte_mentale import DEPLACEMENTS
from reconfort.carte_mentale import LIBRE, INCONNU

def cases_voisines(case):
    cases = []
    for p1, p2 in DEPLACEMENTS.values():
        cases.append((case[0]+p1,case[1]+p2))
    return cases

def _reconstruire(predecesseur, case):
    case_courante = case
    cases = [case]
    while predecesseur[case_courante] is not None:
        cases.append(predecesseur[case_courante])
        case_courante = predecesseur[case_courante]
    cases.reverse()
    return cases

def plus_court_chemin(depart, arrivees, est_traversable):
    arrivees = set(arrivees)
    if depart in arrivees:
        return [depart]

    predecesseur = {depart: None}
    file = File()
    file.enfiler(depart)

    while not file.est_vide():
        courant = file.defiler()
        for voisin in cases_voisines(courant):
            if voisin in predecesseur.keys():
                continue
            if not est_traversable(voisin):
                continue
            predecesseur[voisin] = courant
            if voisin in arrivees:
                return _reconstruire(predecesseur, voisin)
            file.enfiler(voisin)

    return None

def predicat_optimiste(carte):
    def est_traversable(case):
        if not carte.dans_la_grille(case):
            return False
        if carte.type_de(case) == LIBRE or carte.type_de(case) == INCONNU:
            return True
        return False
    return est_traversable

def direction_entre(case1, case2):
    ecart = (case2[0] - case1[0], case2[1] - case1[1])
    if ecart not in DEPLACEMENTS.values():
        raise Exception("Les cases n'ont pas un pas d'écart")
    for direction, case in DEPLACEMENTS.items():
        if ecart == case:
            return direction
    return None


