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

    def analyse(self, modeles, num_modele):

        """ 1 """
        bool = 0
        sujet = ""
        opinion = []
        verbe = []
        holder = ""
        modeles = modeles.split()
        num_element = 1
        for terme in modeles:
            if num_modele == 1:
                if num_element == 1:
                    sujet = terme
                    num_element += 1
                elif num_element == 2:
                    if terme != "(" and terme != "&&" and terme != ")" and terme != "<-":
                        opinion.append(terme)
                    if terme == ")":
                        num_element += 1
                elif num_element == 3:
                    if terme != "@":
                        holder = terme
        print(sujet)
        print(opinion)
        print(holder)
        if num_modele == 1:
            wikiop = TextBlob(sujet)
            scorp_sujet = wikiop.sentiment.subjectivity
            print(type(scorp_sujet))
            scorp_opinion = 0
            for op in opinion:
                wikiop = TextBlob(op)
                x = wikiop.sentiment.subjectivity
                scorp_opinion = scorp_opinion + int(x)
            scorp_opinion = scorp_opinion / len(opinion)
            print(scorp_opinion)

            wikiop = TextBlob(holder)
            scorp_holder = wikiop.sentiment.subjectivity
            resultat = (scorp_sujet * 2 + scorp_opinion * 3 + scorp_holder) / 6
            print(resultat)

    """
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
    """
