"""L'agent : percevoir -> memoriser -> decider -> agir."""
from reconfort.armoire import MemoireArmoire, candidats, trajet
from reconfort.carte_mentale import CarteMentale
from reconfort.dictionnaire import lire_emotion
from reconfort.planification import predicat_optimiste, plus_court_chemin, direction_entre


class Robot:
    def __init__(self, infos, simulateur, trace, dictionnaire):
        self.simulateur = simulateur
        self.trace = trace
        self.dictionnaire = dictionnaire
        self.carte = CarteMentale(infos["hauteur"], infos["largeur"], infos["depart"], infos["armoire"], infos["dictionnaire"], [r["position"] for r in infos["residents"]])
        self.memoire_armoire = MemoireArmoire(infos["casier_depart"])
        self.residents = {r["id"]:r["position"] for r in infos["residents"]}
        self.perception = None
        self.demande = None
        self.objet_porte = None
        self.est_traversable = predicat_optimiste(self.carte)

    def executer_demande(self, numero, resident, message):
        self.demande = numero
        dictionnaire_accessible =  self.aller_a(self.carte.position_dictionnaire)
        if dictionnaire_accessible is False :
            self.trace.ajouter_livraison(demande=self.demande, resident=resident, emotion=None, intensite=None,succes=False, motif_echec="dictionnaire inaccessible", repli="aucun", objet=None,casier_choisi=None)
            return
        self.agir("CONSULTER")
        resultat = lire_emotion(message, self.dictionnaire)
        if resultat is None :
            self.trace.ajouter_livraison(demande=self.demande, resident=resident, emotion=None, intensite=None, succes=False, motif_echec="emotion indeterminee", repli="aucun", objet=None, casier_choisi=None)
            return
        emotion, intensite = resultat
        armoire_accessible = self.aller_a(self.carte.position_armoire)
        if armoire_accessible is False :
            self.trace.ajouter_livraison(demande=self.demande, resident=resident, emotion=emotion, intensite=intensite,objet=None, succes=False, motif_echec="armoire inaccessible", casier_choisi=None,repli="aucun")
            return
        fouillage = self.fouiller(emotion, intensite)
        if fouillage is None :
            self.trace.ajouter_livraison(demande=self.demande, resident=resident, emotion=emotion, intensite=intensite, objet=None, succes=False, motif_echec="armoire vide", casier_choisi=None, repli="aucun")
            return
        casier, objet, repli = fouillage
        self.agir("PRENDRE", objet)
        resident_accessible = self.aller_a(self.residents[resident])
        if resident_accessible is False :
            self.trace.ajouter_livraison(demande=self.demande, resident=resident, emotion=emotion, intensite=intensite, objet=objet, motif_echec="resident inaccessible", repli=repli, casier_choisi=casier, succes=False)
            return
        self.agir("DONNER", objet, resident)
        self.trace.ajouter_livraison(demande=self.demande, resident=resident, emotion=emotion, intensite=intensite, objet=objet, repli=repli, casier_choisi=casier, succes=True)

    def percevoir(self):
        self.perception = self.simulateur.percevoir()
        self.carte.mettre_a_jour(self.simulateur.position, self.perception)
        return self.perception

    def aller_a(self, cible):
        while True:
            self.percevoir()
            arrivees = self.carte.case_d_acces(cible)
            chemin = plus_court_chemin(self.simulateur.position, arrivees, self.est_traversable)
            if chemin is None : return False
            if len(chemin) == 1 : return True
            else :
                self.agir("AVANCER", direction_entre(chemin[0], chemin[1]))

    def fouiller(self, emotion, intensite):
        self.percevoir()
        emotions = self.dictionnaire["emotions"]
        intensites = self.dictionnaire["intensites"]
        self.memoire_armoire.noter(self.simulateur.casier, self.simulateur.contenu_casier())
        liste_candidats = candidats(emotion, intensite, emotions, intensites)
        for (casier, repli) in liste_candidats :
            if self.memoire_armoire.est_connu(casier) and self.memoire_armoire.contenu(casier) is None: continue
            else :
                for d in trajet(self.simulateur.casier, casier, len(intensites), len(emotions)) :
                    self.agir("CHERCHER", d)
                    self.memoire_armoire.noter(self.simulateur.casier, self.simulateur.contenu_casier())

                contenu = self.simulateur.contenu_casier()
                if contenu is not None :
                    return casier, contenu, repli

        return None

    def agir(self, action, argument=None, resident=None, commentaire=None):
        position = self.simulateur.position
        casier = self.simulateur.casier
        contenu = self.simulateur.contenu_casier()
        self.simulateur.appliquer(action, argument, resident)
        self.trace.ajouter_pas(demande=self.demande,position=position,casier=casier, action=action, argument=argument, perception=self.perception, contenu_casier=contenu, commentaire=commentaire)
        self.objet_porte = self.simulateur.objetPorte
