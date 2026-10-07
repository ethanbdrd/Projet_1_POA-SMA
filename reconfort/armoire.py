"""Choix du casier et deplacement du selecteur (enonce 6.2, annexe C)."""


def candidats(emotion, intensite, emotions, intensites):
    """Les 15 casiers a distance <= 2, tries : [((ligne, colonne), repli), ...]."""
    raise NotImplementedError


def trajet(casier, cible, nb_lignes, nb_colonnes):
    """Les directions CHERCHER pour aller de casier a cible."""
    raise NotImplementedError


class MemoireArmoire:
    """Ce que le robot a deja vu dans l'armoire."""

    def __init__(self, casier_depart):
        self.casier = casier_depart
        self.contenus = {}

    def noter(self, casier, objet):
        """Enregistre le contenu constate d'un casier."""
        raise NotImplementedError

    def est_connu(self, casier):
        raise NotImplementedError

    def contenu(self, casier):
        """L'objet du casier, None s'il est vide ou jamais vu."""
        raise NotImplementedError
