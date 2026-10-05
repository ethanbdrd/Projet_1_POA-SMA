INCONNU = "inconnu" ; LIBRE = "libre" ; MUR = "mur" ; ARMOIRE = "armoire" ; DICTIONNAIRE = "dictionnaire" ; RESIDENT = "resident"
DEPLACEMENTS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
SYMBOLES = { INCONNU: "?", LIBRE: ".", MUR: "#", ARMOIRE: "A", DICTIONNAIRE: "D", RESIDENT: "P"}
SYMBOLE_ROBOT = "R"

class CarteMentale :
    def __init__(self, hauteur, largeur, depart, position_armoire, position_dictionnaire, positions_residents) :
        self.hauteur = hauteur
        self.largeur = largeur
        self.depart = depart
        self.position_armoire = position_armoire
        self.position_dictionnaire = position_dictionnaire
        self.positions_residents = positions_residents
        self.grille = [[INCONNU for _ in range(largeur)] for _ in range(hauteur)]
        for i in range(self.hauteur):
            for j in range(self.largeur):
                if i == 0:
                    self.grille[i][j] = MUR
                if j == 0:
                    self.grille[i][j] = MUR
                if i == self.hauteur - 1:
                    self.grille[i][j] = MUR
                if j == self.largeur - 1:
                    self.grille[i][j] = MUR
        self.grille[position_armoire[0]][position_armoire[1]] = ARMOIRE
        self.grille[position_dictionnaire[0]][position_dictionnaire[1]] = DICTIONNAIRE
        self.grille[depart[0]][depart[1]] = LIBRE
        for position_resident in positions_residents:
            self.grille[position_resident[0]][position_resident[1]] = RESIDENT

    def dans_la_grille(self, case) :
        if self.hauteur > case[0] >= 0 and self.largeur > case[1] >= 0 :
            return True
        return False

    def type_de(self, case) :
        if self.dans_la_grille(case) :
            return self.grille[case[0]][case[1]]
        raise Exception("Case hors grille")

    def voisines(self, case) :
        if not self.dans_la_grille(case) :
            raise Exception("Case hors grille")
        voisines = []
        ligne = case[0]
        colonne = case[1]
        for (d1,d2) in DEPLACEMENTS.values() :
            if self.dans_la_grille((ligne + d1, colonne + d2)) :
                voisines.append((ligne + d1, colonne + d2))
        return voisines

    def mettre_a_jour(self,position, perception) :
        ligne = position[0]
        colonne = position[1]
        self.grille[ligne][colonne] = LIBRE
        for direction , (d1,d2) in DEPLACEMENTS.items() :
            if self.dans_la_grille((ligne + d1, colonne + d2)) :
                self.grille[ligne+d1][colonne+d2] = perception[direction]

    def est_connue(self,case) :
        return self.type_de(case) != INCONNU

    def case_d_acces(self, cible):
        cases = self.voisines(cible)
        cases_d_acces = []
        for case in cases :
            if self.type_de(case) == INCONNU or self.type_de(case) == LIBRE :
                cases_d_acces.append(case)
        return cases_d_acces

    def dessiner(self, robot):
        if not self.dans_la_grille(robot) :
            raise Exception("Case hors grille")
        lignes = []
        for ligne in self.grille:
            caracteres = []
            for element in ligne :
                caracteres.append(SYMBOLES[element])
            lignes.append(caracteres)
        lignes[robot[0]][robot[1]] = SYMBOLE_ROBOT
        return "\n".join("".join(ligne) for ligne in lignes)

