from reconfort.structures import Cycle

DISTANCE_MAX = 2
REPLIS_VOISINES = {1: "voisine_1", 2: "voisine_2"}


def candidats(emotion, intensite, emotions, intensites):
    """Les 15 casiers a distance <= 2, tries : [((ligne, colonne), repli), ...]."""
    roue = Cycle(emotions)
    indice_intensite = intensites.index(intensite)
    liste = []
    for colonne in range(len(emotions)) :
        distance, sens = roue.pas(emotion, emotions[colonne])
        if distance <= DISTANCE_MAX :
            for ligne in range(len(intensites)) :
                ecart = abs(ligne - indice_intensite)
                ordre_sens = 0 if sens == "H" else 1
                if distance > 0 :
                    repli = REPLIS_VOISINES[distance]
                elif ecart > 0 :
                    repli = "intensite"
                else :
                    repli = "aucun"
                cle = (distance, ecart, ligne, ordre_sens)
                liste.append((cle, (ligne, colonne), repli))
    liste.sort()
    resultat = []
    for cle, casier, repli in liste :
        resultat.append((casier, repli))
    return resultat


def trajet(casier, cible, nb_lignes, nb_colonnes):
    """Les directions CHERCHER pour aller de casier a cible."""
    if not (0 <= cible[0] < nb_lignes and 0 <= cible[1] < nb_colonnes) :
        raise Exception("Casier hors de l'armoire : " + str(cible))
    directions = []

    ecart_lignes = cible[0] - casier[0]
    if ecart_lignes > 0 :
        directions += ["S"] * ecart_lignes
    else :
        directions += ["N"] * (-ecart_lignes)

    vers_est = (cible[1] - casier[1]) % nb_colonnes
    vers_ouest = nb_colonnes - vers_est
    if vers_est == 0 :
        pass
    elif vers_est <= vers_ouest :
        directions += ["E"] * vers_est
    else :
        directions += ["O"] * vers_ouest
    return directions


class MemoireArmoire:
    """Ce que le robot a deja vu dans l'armoire."""

    def __init__(self, casier_depart):
        self.casier = casier_depart
        self.contenus = {}

    def noter(self, casier, objet):
        """Enregistre le contenu constate d'un casier."""
        self.contenus[casier] = objet

    def est_connu(self, casier):
        return casier in self.contenus

    def contenu(self, casier):
        """L'objet du casier, None s'il est vide ou jamais vu."""
        return self.contenus.get(casier)
