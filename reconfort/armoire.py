from reconfort.structures import Cycle

# Niveau de repli par rapport au casier idéal : même intensité, autre intensité ou émotion voisine
DISTANCE_MAX = 2
REPLIS_VOISINES = {1: "voisine_1", 2: "voisine_2"}


def candidats(emotion, intensite, emotions, intensites): #A partir de ce que ressent le résident, elle donne la liste des 15 casiers acceptables, rangés du meilleur au moins bon, pour que le robot sache dans quel ordre les fouiller.
    roue = Cycle(emotions)
    indice_intensite = intensites.index(intensite)
    liste = []
    for colonne in range(len(emotions)) :
        distance, sens = roue.pas(emotion, emotions[colonne]) #sens horaire ou antihoraire
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
                cle = (distance, ecart, ligne, ordre_sens) #distance, écart d'intensité, intensité la plus faible(la ligne), sens horaire
                liste.append((cle, (ligne, colonne), repli))
    liste.sort()
    resultat = []
    for cle, casier, repli in liste :
        resultat.append((casier, repli))
    return resultat


def trajet(casier, cible, nb_lignes, nb_colonnes): #Les directions CHERCHER pour aller de casier a cible par le chemin le plus court où un selecteur va passer d'un casier a un autre .
    if not (0 <= cible[0] < nb_lignes and 0 <= cible[1] < nb_colonnes) :#Cas casier n exite pas
        raise Exception("Casier hors de l'armoire : " + str(cible))
    directions = []

    ecart_lignes = cible[0] - casier[0]
    if ecart_lignes > 0 : #positif cible plsu bas , negatif cible plsu haut ou bien meme ligne
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


class MemoireArmoire: # C'est le carnet de notes pour que a chaque passage d'un caiser a un autre il s'en souviens ce qu'il y a dedans.
    def __init__(self, casier_depart):
        self.casier = casier_depart
        self.contenus = {}

    def noter(self, casier, objet): #Le robot note le contenu d'un casier vu
        self.contenus[casier] = objet

    def est_connu(self, casier): #True si il a deja regarder ce casier False sinon
        return casier in self.contenus

    def contenu(self, casier): #Le nom de l'objet ou None s'il est vide ou jamais vu
        return self.contenus.get(casier)
