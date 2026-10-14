"""Lecture de l'emotion d'un message"""
from reconfort.reconfort_io import normaliser

_dernier_dictionnaire = None
_dernier_index = None

def construire_index(dictionnaire):
    """Transforme les entrees du dictionnaire en un index mot -> (emotion, intensite)"""
    index={}
    for entree in dictionnaire["entrees"] :
        for forme in entree["formes"]:
            index[forme]=(entree["emotion"],entree["intensite"])
    return index

def index_de(dictionnaire):
    """Renvoie l'index du dictionnaire, construit une seule fois.On garde le dernier dictionnaire recu et son index : si on recoit le meme dictionnaire, on reutilise l'index au lieu de le reconstruire.
    """
    global _dernier_dictionnaire, _dernier_index
    if dictionnaire is not _dernier_dictionnaire:
        _dernier_index = construire_index(dictionnaire)
        _dernier_dictionnaire = dictionnaire
    return _dernier_index

def lire_emotion(message, dictionnaire):
    """Renvoie (emotion, intensite) du premier mot reconnu du message, ou None."""
    index=index_de(dictionnaire)
    for mot in normaliser(message):
        if mot in index:
            return index[mot]
    return None
