from collections import deque

class File :
    def __init__(self) :
        self.elements = deque()
        self.taille = 0

    def enfiler(self, element) :
        self.elements.append(element)
        self.taille += 1

    def defiler(self) :
        if len(self) <= 0:
            raise Exception("Liste vide : impossible à dépiler")
        else :
            self.taille -= 1
            return self.elements.popleft()

    def est_vide(self):
        return self.taille == 0

    def __len__(self):
        return self.taille

class Cycle :
    def __init__(self, elements) :
        if (type(elements) is not list) or (len(elements) == 0) :
            raise Exception("Liste vide")
        elif len(elements) != len(set(elements)) :
            raise Exception("Liste contenant des doublons")
        else :
            self.elements = elements
            self.tailleRoue = len(elements)

    def indice(self, element) :
        if element not in self.elements:
            raise Exception("élement inconnu")
        return self.elements.index(element)

    def element(self,indice) :
        return self.elements[indice%self.tailleRoue]

    def suivant(self, element) :
        if element not in self.elements:
            raise Exception("élement inconnu")
        indiceElement = self.indice(element)
        indiceElementSuivant = (indiceElement+1)%self.tailleRoue
        return self.element(indiceElementSuivant)

    def precedent(self, element) :
        if element not in self.elements:
            raise Exception("élement inconnu")
        indiceElement = self.indice(element)
        indiceElementPrecedent = (indiceElement-1)%self.tailleRoue
        return self.element(indiceElementPrecedent)

    def __distanceEtSens(self, element1, element2) :
        distanceHoraire = 0
        while element1 != element2:
            element1 = self.suivant(element1)
            distanceHoraire+=1
        distanceAntiHoraire = abs(self.tailleRoue-distanceHoraire)
        if distanceAntiHoraire<distanceHoraire:
            return distanceAntiHoraire, "A"
        else :
            return distanceHoraire, "H"

    def distance(self, element1, element2) :
        if element1 not in self.elements:
            raise Exception("élement inconnu")
        if element2 not in self.elements:
            raise Exception("élement inconnu")
        return self.__distanceEtSens(element1, element2)[0]

    def sens(self, element1, element2) :
        if element1 not in self.elements:
            raise Exception("élement inconnu")
        if element2 not in self.elements:
            raise Exception("élement inconnu")
        return self.__distanceEtSens(element1, element2)[1]

    def pas(self, element1, element2) :
        if element1 not in self.elements:
            raise Exception("élément inconnu")
        if element2 not in self.elements:
            raise Exception("élement inconnu")
        return self.__distanceEtSens(element1, element2)








