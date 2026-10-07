"""Lecture de l'emotion d'un message (enonce 6.1)."""

from reconfort.reconfort_io import normaliser

def construire_index(dictionnaire):
    index={}
    for entree in dictionnaire["entrees"] :
        for forme in entree["formes"]:
            index[forme]=(entree["emotion"],entree["intensite"])
    return index



def lire_emotion(message, dictionnaire):
    index=construire_index(dictionnaire)
    for mot in normaliser(message):
        if mot in index:
            return index[mot]
    return None
