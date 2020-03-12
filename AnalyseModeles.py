# -*- coding: utf-8 -*-
import pickle
from textblob import TextBlob
from os import path as os_path


class AnalyseModeles:
    modeles = []
    sujet = ""
    modelesFiltrer = []

    def __init__(self, sujet):
        self.sujet = sujet

    """ lire les modeles depuis le fichier modeles.pkl"""

    def lectureModee(self):
        with open(os_path.abspath(os_path.split(__file__)[0]) + '/modeles.pkl', 'rb') as input:
            self.modeles = pickle.load(input)

    """ garder sauf les modeles lie a notre sujet"""

    def filtrage(self):
        self.modelesFiltrer = []
        for modele in self.modeles:
            if modele.split()[0] == self.sujet:
                self.modelesFiltrer.append(modele)

    """Analyse des modeles 
    1 extraire les adjectif pour chaque modeles
    2  calculer la moyennes
    
    """

    def analyse(self):

        """ 1 """

        opinion = []
        for modele in self.modelesFiltrer:
            modele = modele.split()
            print(modele)
            bool = 0
            for i in range(0, len(modele) - 1):
                if modele[i] == "(":
                    bool = 1
                if bool > 1 and modele[i] != "&&":
                    opinion.append(modele[i])
                if bool == 1:
                    bool += 1

        """ 2 """

        scors = []
        for op in opinion:
            wikiop = TextBlob(op)
            scors.append(wikiop.sentiment)
        moy = 0
        for scor in scors:
            moy = moy + scor[0]
        if (moy > 0):
            print("senetiement positif")
            return 1
        else:
            print("senetiement negatif")
            return 0
