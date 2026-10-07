"""L'agent : percevoir -> memoriser -> decider -> agir."""


class Robot:
    def __init__(self, infos, simulateur, trace, dictionnaire):
        self.simulateur = simulateur
        self.trace = trace
        self.dictionnaire = dictionnaire
        self.carte = None            # CarteMentale, a construire depuis infos
        self.memoire_armoire = None  # MemoireArmoire
        self.residents = {}          # id -> position
        self.perception = None       # perception du tour courant
        self.demande = None          # numero de la demande en cours
        self.objet_porte = None

    def executer_demande(self, numero, resident, message):
        """Deroule une demande : dictionnaire, armoire, resident (enonce 4)."""
        raise NotImplementedError

    def percevoir(self):
        """Interroge le simulateur et met a jour la carte mentale."""
        raise NotImplementedError

    def aller_a(self, cible):
        """Avance jusqu'a une case voisine de cible. False si inaccessible."""
        raise NotImplementedError

    def fouiller(self, emotion, intensite):
        """Suit l'ordre de 6.2. Renvoie (casier, objet, repli), ou None."""
        raise NotImplementedError

    def agir(self, action, argument=None, resident=None, commentaire=None):
        """Execute l'action via le simulateur et la journalise dans la trace."""
        raise NotImplementedError
