# coding=utf8
import spacy

nlp = spacy.load("fr_core_news_sm")

import pickle
from os import path as os_path


class CreationModele_fr:
    text = ""
    language = ""
    wiki = ""
    arraySenetence = []
    modeles = []

    def __init__(self):
        self.text = ""
        self.language = "en"
        self.tb = ""

    """ Lire text depuis un fichier """

    def lecture(self, fichier):
        self.text = open(os_path.abspath(os_path.split(__file__)[0]) + "/" + fichier, "r").read()
        print(self.text)

    """ phase de pre traitement 
    1 detection de la langues
    2 correction d'orthographe
    3 segmenetation de texte par phrase
    """

    def preTraitement(self):
        self.wiki = nlp(self.text)
        """ 1 """

        """ 2 """
        """ 3 """
        for sentence in self.wiki.sents:
            self.arraySenetence.append(sentence.text)
        print(self.arraySenetence)

    """ cree les modeles pour chaque phrase
    1 extraire adj propn noun pron de chaque phrase
    2 definire sujet aspect holder opinion 
    3 fomulation de modele
    4 sauvgarder dans un fichier pkl
    """

    def creationModele(self):
        for sentence in self.arraySenetence:
            print(sentence)
            sentence = nlp(sentence)
            adj = []
            propn = []
            noun = []
            pron = []
            opinion = []
            """  1  """
            for word in sentence:
                if word.pos_ == "ADJ":
                    adj.append(word.text)
                if word.pos_ == "PROPN":
                    propn.append(word.text)
                if word.pos_ == "NOUN":
                    noun.append(word.text)
                if word.pos_ == "PRON":
                    pron.append(word.lemma_)


            """ 2 """
            if len(propn) != 0:
                sujet = propn[0]
                if len(noun) != 0:
                    aspect = noun[0]
            else:
                if len(noun) != 0:
                    sujet = noun[0]
                if len(noun) > 1:
                    aspect = noun[1]
                else:
                    aspect = noun[0]

            if len(adj) != 0:
                for i in range(len(adj)):
                    opinion.append(adj[i])

            """ 3 """
            modele = sujet + " <- " + aspect + " ( "
            for i in range(0, len(opinion) - 1):
                modele = modele + opinion[i] + " && "
            modele = modele + opinion[len(opinion) - 1] + " )"
            if len(pron)!=0:
                modele=modele+" ? "+pron[0]
            self.modeles.append(modele)


        print("les modeles avant le filtrage")
        print(self.modeles)
        print("les modeles avant le filtrage ******")


        """ 4 """
        """ sauvgarder les modeles dans le fichier modeles.pkl"""
        with open(os_path.abspath(os_path.split(__file__)[0]) + '/modeles.pkl', 'wb') as output:
            pickle.dump(self.modeles, output, pickle.HIGHEST_PROTOCOL)
