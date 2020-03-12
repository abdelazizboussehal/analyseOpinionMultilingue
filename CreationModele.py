# -*- coding: utf-8 -*-
from textblob import TextBlob
import pickle
from os import path as os_path


class CreationModele:
    text = ""
    language = ""
    wiki = ""
    arraySenetence = ""
    modeles = []

    def __init__(self):
        self.text = ""
        self.language = "en"

    """ Lire text depuis un fichier """

    def lecture(self,fichier):
        self.text = open(os_path.abspath(os_path.split(__file__)[0]) + "/"+fichier, "r").read()
        print(self.text)

    """ phase de pre traitement 
    1 detection de la langues
    2 correction d'orthographe
    3 segmenetation de texte par phrase
    """

    def preTraitement(self):
        self.wiki = TextBlob(self.text)
        """ 1 """
        self.language = self.wiki.detect_language()
        print("la langue de ce texte est : " + self.language)
        """ 2 """
        self.wiki = self.wiki.correct()
        print(self.wiki)
        """ 3 """
        self.arraySenetence = self.wiki.sentences
        print(self.arraySenetence)

    """ cree les modeles pour chaque phrase
    1 extraire sujet
    2 extraire aspect
    3 extraire opinion
    4 formulation de modele
    5 sauvgarder dans un fichier pkl
    """

    def creationModele(self):
        for sentence in self.arraySenetence:
            print(sentence.pos_tags)
            tasarray = sentence.pos_tags
            opinion = []
            bool = 0
            for word in tasarray:
                """ 1 """
                if word[1] == "NNP" and bool == 0:
                    bool = 1
                    print(word)
                    sujet = word[0]
                """ 2 """
                if word[1] == "NN":
                    aspect = word[0]
                """ 3 """
                if word[1] == "JJ":
                    opinion.append(word[0])
            """ 4 """
            modele = sujet + " <- " + aspect + " ( "
            for i in range(0, len(opinion) - 1):
                modele = modele + opinion[i] + " && "
            modele = modele + opinion[len(opinion) - 1] + " )"
            self.modeles.append(modele)
        print("les modeles avant le filtrage")
        print(self.modeles)
        print("les modeles avant le filtrage ******")
        """ 5 """
        """ sauvgarder les modeles dans le fichier modeles.pkl"""
        with open(os_path.abspath(os_path.split(__file__)[0]) + '/modeles.pkl', 'wb') as output:
            pickle.dump(self.modeles, output, pickle.HIGHEST_PROTOCOL)
