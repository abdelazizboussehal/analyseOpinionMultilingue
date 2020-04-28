# -*- coding: utf-8 -*-
import pickle

from Crypto import Math
from textblob import TextBlob
from library import tools as t
import numpy as np
from os import path as os_path

from library.SentiWordNet import SentiWordNet


class AnalyseModels:
    language = "en"

    def __init__(self, language):
        self.language = language

    @staticmethod
    def get_elements_verb(model):
        array_model = model.split()
        verb = ""
        adverb = []
        neg = False

        for i in range(len(array_model)):
            if i == 0:
                if array_model[i] == t.Tools.sc_negation.replace(" ", ""):
                    neg = True
                    verb = array_model[i + 1]
                else:
                    verb = array_model[i]
            elif array_model[i] == t.Tools.sc_verb.replace(" ", ""):
                adverb.append(array_model[i + 2])
            elif array_model[i] == t.Tools.sc_adv_cordination.replace(" ", ""):
                adverb.append(array_model[i + 1])
        return verb, adverb, neg

    @staticmethod
    def get_elements_adjective(model):
        array_model = model.split()
        adjective = ""
        adverb = []
        neg = False

        for i in range(len(array_model)):
            if i == 0:
                if array_model[i] == t.Tools.sc_negation.replace(" ", ""):
                    neg = True
                    adjective = array_model[i + 1]
                else:
                    adjective = array_model[i]

            elif array_model[i] == t.Tools.sc_verb.replace(" ", ""):
                adverb.append(array_model[i + 2])
            elif array_model[i] == t.Tools.sc_adv_cordination.replace(" ", ""):
                adverb.append(array_model[i + 1])
        return adjective, adverb, neg

    @staticmethod
    def get_polarity_adverb_neg(polarity_element, adverb, neg, language):
        """recuprer polarite de liste des adverbes et negation"""
        polarity_adv_total = []
        if polarity_element != 0 and polarity_element != []:
            if neg:
                polarity_element = -1 * polarity_element
            if len(adverb) != 0:
                for adv in adverb:
                    polarity_adv = SentiWordNet.get_sentiment(adv, language, "r")
                    if polarity_adv != -2000:
                        polarity_adv_total.append(polarity_adv)
        return polarity_element, polarity_adv_total

    def get_elements_polarity_verb(self, verb, adverb, neg):
        """recuper polarite groupe  verbe"""
        polarity_verb = 0
        if verb != "":
            polarity_verb = SentiWordNet.get_sentiment(verb, self.language, "v")
        return AnalyseModels.get_polarity_adverb_neg(polarity_verb, adverb, neg, self.language)

    def get_elements_polarity_adjective(self, adj, adverb, neg):
        """recuper polarite groupe adjective """
        polarity_adj = 0
        if adj != "":
            polarity_adj = SentiWordNet.get_sentiment(adj, self.language, "a")
        return AnalyseModels.get_polarity_adverb_neg(polarity_adj, adverb, neg, self.language)

    def get_polarity_verb(self, model_verb):
        elements_verb = AnalyseModels.get_elements_verb(model_verb)
        elements_verb_polarity = self.get_elements_polarity_verb(elements_verb[0], elements_verb[1], elements_verb[2])
        polarity_verb = elements_verb_polarity[0]
        if isinstance(polarity_verb, list):
            return -1000
        if len(elements_verb_polarity[1]) > 0:
            mean_adv = np.array(elements_verb_polarity[1]).mean()
        else:
            mean_adv = 0
        if polarity_verb > 0:
            return polarity_verb + (1 - polarity_verb) * mean_adv
        else:
            return polarity_verb - (1 - polarity_verb) * mean_adv


"""

    models = []
    sujet = ""
    modelesFiltrer = []

    def __init__(self, sujet):
        self.sujet = sujet

lire les modeles depuis le fichier modeles.pkl

    def lectureModee(self):
        with open(os_path.abspath(os_path.split(__file__)[0]) + '/modeles.pkl', 'rb') as input:
            self.modeles = pickle.load(input)

garder sauf les modeles lie a notre sujet

    def filtrage(self):
        self.modelesFiltrer = []
        for modele in self.modeles:
            if modele.split()[0] == self.sujet:
                self.modelesFiltrer.append(modele)

    Analyse des modeles 
    1 extraire les adjectif pour chaque modeles
    2  calculer la moyennes
    
    

    def analyse(self, modeles, num_modele):

        
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
