import copy

DEPLACEMENTS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}

TYPE_PAR_SYMBOLE = {
    "#": "mur",
    ".": "libre",
    "R": "libre",
    "A": "armoire",
    "D": "dictionnaire",
    "P": "resident",
}


class Simulateur :
    def __init__(self, carte, armoire) :
        self.__grille = carte["grille"]
        self.__objets = {}
        for casier in armoire["casiers"] :
            self.__objets[(casier["ligne"], casier["colonne"])] = casier["objet"]

        self.hauteur = len(self.__grille)
        self.largeur = len(self.__grille[0])

        self.nbLignesArmoire = len(armoire["intensites"])    #faible, moyenne, forte
        self.nbColonnesArmoire = len(armoire["emotions"])    #les 8 emotions de la roue

        self.posArmoire = tuple(carte["armoire"]["position"])
        self.posDictionnaire = tuple(carte["dictionnaire"]["position"])
        self.posResidents = {}
        for resident in carte["residents"] :
            self.posResidents[resident["id"]] = tuple(resident["position"])

        residents = []
        for resident in carte["residents"] :
            residents.append({
                "id": resident["id"],
                "nom": resident["nom"],
                "position": tuple(resident["position"]),
            })

        etiquettes = []
        for casier in armoire["casiers"] :
            etiquettes.append({
                "ligne": casier["ligne"],
                "colonne": casier["colonne"],
                "emotion": casier["emotion"],
                "intensite": casier["intensite"],
            })

        self.__infos = {  #Ce que le robot a le droit de voir comme informations 
            "hauteur": carte["dimensions"]["hauteur"],
            "largeur": carte["dimensions"]["largeur"],
            "depart": tuple(carte["depart_robot"]),
            "armoire": self.posArmoire,
            "dictionnaire": self.posDictionnaire,
            "residents": residents,
            "casier_depart": tuple(armoire["casier_depart"]),
            "etiquettes": etiquettes,
        }

        self.position = tuple(carte["depart_robot"])
        self.casier = tuple(armoire["casier_depart"])
        self.objetPorte = None

    def infos_initiales(self) :
        return copy.deepcopy(self.__infos)

    def percevoir(self) :
        perception = {}
        for direction in ("N", "S", "E", "O") :
            caseVoisine = self.__voisine(self.position, direction)
            perception[direction] = self.__typeCase(caseVoisine)
        return perception

    def contenu_casier(self) :
        if not self.__adjacentA(self.posArmoire) :
            return None
        else :
            return self.__objets.get(self.casier)


    def appliquer(self, action, argument=None, resident=None) :
        if action == "AVANCER" :
            self.__avancer(argument)
        elif action == "CONSULTER" :
            self.__consulter()
        elif action == "CHERCHER" :
            self.__chercher(argument)
        elif action == "PRENDRE" :
            self.__prendre(argument)
        elif action == "DONNER" :
            self.__donner(argument, resident)
        elif action == "ATTENDRE" :
            pass
        else :
            raise Exception("Action inconnue : " + str(action))

    def dessiner(self) :
        lignes = []
        for l in range(self.hauteur) :
            ligne = ""
            for c in range(self.largeur) :
                if (l, c) == self.position :
                    ligne += "R"
                elif self.__grille[l][c] == "R" : #Qd le robot n'y est pas 
                    ligne += "."
                else :
                    ligne += self.__grille[l][c]
            lignes.append(ligne)
        return "\n".join(lignes)


    def __avancer(self, direction) :
        if direction not in DEPLACEMENTS :
            raise Exception("Direction inconnue : " + str(direction))

        caseCible = self.__voisine(self.position, direction)

        if self.__typeCase(caseCible) != "libre" :
            raise Exception("Impossible d'avancer : la case " + str(caseCible) + " n'est pas libre")
        else :
            self.position = caseCible


    def __consulter(self) :
        if not self.__adjacentA(self.posDictionnaire) :
            raise Exception("Impossible de consulter : pas à côté du dictionnaire")



    def __chercher(self, direction) :
        if not self.__adjacentA(self.posArmoire) :
            raise Exception("Impossible de chercher : pas à côté de l'armoire")

        if direction not in DEPLACEMENTS :
            raise Exception("Direction inconnue : " + str(direction))

        ligne, colonne = self.casier
        dl, dc = DEPLACEMENTS[direction]
        nouvelleLigne = ligne+dl
        if nouvelleLigne < 0 or nouvelleLigne >= self.nbLignesArmoire :
            raise Exception("Impossible de chercher : les lignes de l'armoire ne bouclent pas")
        else :
            nouvelleColonne = (colonne+dc)%self.nbColonnesArmoire
            self.casier = (nouvelleLigne, nouvelleColonne)



    def __prendre(self, objet) :
        if not self.__adjacentA(self.posArmoire) :
            raise Exception("Impossible de prendre : pas à côté de l'armoire")
        if self.objetPorte is not None :
            raise Exception("Impossible de prendre : le robot porte déjà " + self.objetPorte)
        contenu = self.__objets.get(self.casier)
        if contenu is None :
            raise Exception("Impossible de prendre : le casier " + str(self.casier) + " est vide")
        if objet != contenu :
            raise Exception("Impossible de prendre " + str(objet) + " : le casier contient " + contenu)
        else :
            self.objetPorte = contenu



    def __donner(self, objet, resident) :
        if resident not in self.posResidents :
            raise Exception("Résident inconnu : " + str(resident))
        if not self.__adjacentA(self.posResidents[resident]) :
            raise Exception("Impossible de donner : pas à côté de " + resident)
        if self.objetPorte is None or self.objetPorte != objet :
            raise Exception("Impossible de donner " + str(objet) + " : le robot porte " + str(self.objetPorte))
        else :
            self.objetPorte = None



    def __voisine(self, case, direction) :
        dl, dc = DEPLACEMENTS[direction]
        return (case[0]+dl, case[1]+dc)



    def __typeCase(self, case) :
        ligne, colonne = case
        if ligne < 0 or ligne >= self.hauteur or colonne < 0 or colonne >= self.largeur :
            return "mur"
        else :
            return TYPE_PAR_SYMBOLE[self.__grille[ligne][colonne]]



    def __adjacentA(self, cible) :
        ligne, colonne = self.position
        return abs(ligne-cible[0]) + abs(colonne-cible[1]) == 1