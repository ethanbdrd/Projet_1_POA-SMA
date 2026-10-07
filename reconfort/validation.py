SYMBOLES_VALIDES = ["#", ".", "R", "A", "D", "P"]


class ErreurValidation(Exception) :
    pass


def champ(donnees, cle , typeAttendu, fichier) :
    if cle not in donnees :
        raise ErreurValidation(fichier + " : champ " + cle + " absent")
    if type(donnees[cle]) is not typeAttendu :
        raise ErreurValidation(fichier + " : " + cle + " doit être de type " + typeAttendu.__name__)
    return donnees[cle]




def position(coordonnees, nomPosition, nomFichier, hauteur, largeur):

    if type(coordonnees) is not list:
        raise ErreurValidation(nomFichier + " : " + nomPosition + " n'est pas une position")

    if len(coordonnees) != 2:
        raise ErreurValidation(nomFichier + " : " + nomPosition + " doit contenir une ligne et une colonne")

    if type(coordonnees[0]) is not int or type(coordonnees[1]) is not int:
        raise ErreurValidation(nomFichier + " : " + nomPosition + " doit contenir deux entiers")

    ligne = coordonnees[0]
    colonne = coordonnees[1]

    if ligne < 0 or ligne >= hauteur or colonne < 0 or colonne >= largeur:
        raise ErreurValidation(nomFichier + " : " + nomPosition + " hors de la grille")

    return coordonnees




def version(donnees, fichier) :
    if type(donnees.get("version")) is not int or donnees["version"] != 1 :
        raise ErreurValidation(fichier + " : version invalide")



def valider_carte(carte) :
    version(carte, "carte")
    champ(carte, "nom", str, "carte")
    dimensions = champ(carte, "dimensions", dict, "carte")
    hauteur = champ(dimensions, "hauteur", int, "carte")
    largeur = champ(dimensions, "largeur", int, "carte")
    grille = champ(carte, "grille", list, "carte")

    if len(grille) == 0 :
        raise ErreurValidation("carte : grille vide")
    if type(grille[0]) is not str or len(grille[0]) == 0 :
        raise ErreurValidation("carte : grille vide")
    for ligne in grille :
        if type(ligne) is not str :
            raise ErreurValidation("carte : la grille n'est pas une chaine de caracteres .")
        if len(ligne) != len(grille[0]) :
            raise ErreurValidation("carte : grille non rectangulaire")

        for symbole in ligne : 
            if symbole not in SYMBOLES_VALIDES :
                raise ErreurValidation("carte : Symbole inconnu " + symbole)

    if len(grille) != hauteur or len(grille[0]) != largeur :
        raise ErreurValidation("carte : Dimensions incohérentes avec la grille")


    #Verif que tous les cote d ela grille soit des #

    for ligne in grille :
        if ligne[0] != "#" or ligne[-1] != "#" :
            raise ErreurValidation("carte : la grille doit être entourée de murs")

    for symbole in grille[0] + grille[-1] :
        if symbole != "#" :
            raise ErreurValidation("carte : la grille doit être entourée de murs")



    # Vérification de la position de départ du robot
    departRobot = champ(carte, "depart_robot", list, "carte")
    position(departRobot, "depart_robot", "carte", hauteur, largeur) #Verification
    ligne = departRobot[0]
    colonne = departRobot[1]
    if grille[ligne][colonne] != "R" :
        raise ErreurValidation("carte : le depart du robot n'est pas sur R")

    for element, symbole in (("armoire", "A"), ("dictionnaire", "D")) :
        bloc = champ(carte, element, dict, "carte")         # la position de l'armoire 
        coordonnees= champ(bloc, "position", list, "carte")
        position(coordonnees, element, "carte", hauteur, largeur)   #Verification 
        ligne=coordonnees[0]
        colonne=coordonnees[1]

        if grille[ligne][colonne] != symbole :
            raise ErreurValidation("carte : " + element + " n'est pas sur un " + symbole)


    # Vérification des résidents et des doublons
    identifiants=[]
    for resident in champ(carte,"residents",list,"carte"):
        if type(resident) is not dict:
            raise ErreurValidation("carte : resident mal formé ")

        identifiant=champ(resident,"id",str,"carte")
        champ(resident,"nom",str,"carte")
        coordonnees=champ(resident,"position",list,"carte")
        position(coordonnees, identifiant , "carte", hauteur, largeur) 
        ligne=coordonnees[0]
        colonne=coordonnees[1]
        if grille[ligne][colonne] != "P":
            raise ErreurValidation("carte : le resident " + identifiant + " n'est pas sur le P")
        if identifiant in identifiants :
            raise ErreurValidation("carte : identifiant " + identifiant + " en double")
        identifiants.append(identifiant)




def valider_armoire(armoire, dictionnaire) :
    version(armoire, "armoire")
    emotions = champ(armoire, "emotions", list, "armoire")
    intensites = champ(armoire, "intensites", list, "armoire")
    if emotions != dictionnaire["emotions"] or intensites != dictionnaire["intensites"] :
        raise ErreurValidation("armoire : les émotions ou les intensités sont différentes de ceux du dictionnaire")

    coordonnees =champ(armoire, "casier_depart", list, "armoire")
    position(coordonnees,"casier_depart","armoire",3,8)


    dejaVus = []
    for casier in champ(armoire, "casiers", list, "armoire") :
        if type(casier) is not dict :
            raise ErreurValidation("armoire : Le casier est mal formé il doit etre un dictionnaire")
        ligne = champ(casier, "ligne", int, "armoire")
        colonne = champ(casier, "colonne", int, "armoire")
        if  ligne < 0 or ligne >= 3 or colonne < 0 or colonne >= 8 :
            raise ErreurValidation("armoire : casier hors de la taille de l'armoire")
        if (ligne ,colonne ) in dejaVus :
            raise ErreurValidation("armoire : casier en double")
        dejaVus.append((ligne, colonne))
        if champ(casier, "emotion", str, "armoire") != emotions[colonne] or champ(casier, "intensite", str, "armoire") != intensites[ligne] :
            raise ErreurValidation("armoire : étiquette incohérente pour le casier ; soit l'emotion soit l'intensite " + str([ligne, colonne]))
        if "objet" not in casier :
            raise ErreurValidation("armoire : champ objet absent")

    if len(dejaVus) != 3 * 8 :
        raise ErreurValidation("armoire : " + str(len(dejaVus)) + " casiers au lieu de 24")




def valider_scenario(scenario, carte) :  
    version(scenario, "scénario")
    champ(scenario, "nom", str, "scénario")
    champ(scenario, "armoire", str, "scénario")
    if champ(scenario, "carte", str, "scénario") != carte["nom"] :
        raise ErreurValidation("scénario : prévu pour une autre carte")


    identifiants = []
    for resident in carte["residents"] :
        identifiants.append(resident["id"])

    numeros = []
    for demande in champ(scenario, "demandes", list, "scénario") :
        if type(demande) is not dict :
            raise ErreurValidation("scénario : demande mal formée")
        numero = champ(demande, "numero", int, "scénario")
        if numero in numeros :
            raise ErreurValidation("scénario : numero de demande " + str(numero) + " en double")
        numeros.append(numero)
        champ(demande, "message", str, "scénario")
        resident = champ(demande, "resident", str, "scénario")
        if resident not in identifiants :
            raise ErreurValidation("scénario : résident " + resident + " inconnu")


def valider_dictionnaire(dictionnaire) :
    version(dictionnaire, "dictionnaire")
    emotions = champ(dictionnaire, "emotions", list, "dictionnaire")
    intensites = champ(dictionnaire, "intensites", list, "dictionnaire")
    if len(emotions) != 8 or len(intensites) != 3 :
        raise ErreurValidation("dictionnaire : il faut 8 émotions et 3 intensités")

    dejaVus = []
    for entree in champ(dictionnaire, "entrees", list, "dictionnaire") :
        if type(entree) is not dict :
            raise ErreurValidation("dictionnaire : entrée mal formée")
        if champ(entree, "emotion", str, "dictionnaire") not in emotions :
            raise ErreurValidation("dictionnaire : émotion inconnue " + entree["emotion"])
        if champ(entree, "intensite", str, "dictionnaire") not in intensites :
            raise ErreurValidation("dictionnaire : intensité inconnue " + entree["intensite"])
        for mot in champ(entree, "formes", list, "dictionnaire") :
            if type(mot) is not str :
                raise ErreurValidation("dictionnaire : le mot " + str(mot) + " n'est pas une chaîne")
            if mot in dejaVus :
                raise ErreurValidation("dictionnaire : le mot " + mot + " apparaît deux fois")
            dejaVus.append(mot)