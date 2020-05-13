# -*- coding: utf-8 -*-
import numpy

from library import tools as t, lexicon
import numpy as np
import re
from library.SentiWordNet import SentiWordNet


class AnalyseModels:
    language = "en"
    model_general = ""
    sub_model_verb = ""
    sub_model_adjective = ""
    sub_model_noun = ""
    connector = ""
    polarity_sub_model_verb = 0
    polarity_sub_model_noun = 0
    polarity_sub_model_adjective = 0

    def __init__(self, language, model):
        self.language = language
        self.model_general = model

    def extract_sub_models(self):
        s = self.model_general
        ss = str(s.split())
        for i in range(len(ss)):
            if ss[i] == t.Tools.sc_model_global_connector.replace(" ", ""):
                self.connector = ss[i + 1]
                break
        result = re.search(t.Tools.sc_verb_start + "(.*)" + t.Tools.sc_verb_end, s)
        if result is not None:
            self.sub_model_verb = result.group(1)
        result = re.search(t.Tools.sc_adjective_start + "(.*)" + t.Tools.sc_adjective_end, s)
        if result is not None:
            self.sub_model_adjective = result.group(1)
        result = re.search(t.Tools.sc_noun_start + "(.*)" + t.Tools.sc_noun_end, s)
        if result is not None:
            self.sub_model_noun = result.group(1)

    def extract_element_verb(self):
        sub_model_verb = self.sub_model_verb
        table_verb = sub_model_verb.split(t.Tools.sc_verb_cordination)
        table_dic_verb = []
        for verb in table_verb:
            [v, a, n] = AnalyseModels.get_elements_verb(verb)
            table_dic_verb.append({"verb": v, "adverb": a, "negation": n})
        return table_dic_verb

    def extract_element_adjective(self):
        sub_model_adjective = self.sub_model_adjective
        table_adjective = sub_model_adjective.split(t.Tools.sc_adjective_cordination)
        table_dic_adjective = []
        for adj in table_adjective:
            [v, a, n] = AnalyseModels.get_elements_adjective(adj)
            table_dic_adjective.append({"adjective": v, "adverb": a, "negation": n})
        return table_dic_adjective

    def extract_element_noun(self):
        sub_model_noun = self.sub_model_noun
        table_noun = sub_model_noun.split(t.Tools.sc_noun_addition)
        return table_noun

    def get_polarity_sub_model_verb(self):
        """ recuperer polarite de sous models verbe """
        if self.sub_model_verb:  # test s'il existe sous model verb
            array_polarity_verb = []
            for element in self.extract_element_verb():
                polarity = self.get_elements_polarity_verb(element.get("verb"), element.get("adverb"),
                                                           element.get("negation"))
                array_polarity_verb.append(polarity)
            self.polarity_sub_model_verb = numpy.array(array_polarity_verb).mean()

    def get_polarity_sub_model_adjective(self):
        """ recuperer polarite de sous model adjective """
        if self.sub_model_adjective:
            array_polarity_adjective = []
            for element in self.extract_element_adjective():
                polarity = self.get_elements_polarity_adjective(element.get("adjective"), element.get("adverb"),
                                                                element.get("negation"))
                array_polarity_adjective.append(polarity)
            self.polarity_sub_model_adjective = numpy.array(array_polarity_adjective).mean()

    def get_polarity_sub_model_noun(self):
        if self.sub_model_noun:
            array_polarity_noun = []
            for element in self.extract_element_noun():
                array_polarity_noun.append(SentiWordNet.get_sentiment(element, self.language, "n"))
            while -1000 in array_polarity_noun:
                array_polarity_noun.remove(-1000)
            if not array_polarity_noun:
                self.polarity_sub_model_noun = 0
            else:
                self.polarity_sub_model_noun = numpy.array(array_polarity_noun).mean()

    def polarity_model(self):

        if self.sub_model_adjective and self.sub_model_verb and self.sub_model_noun:
            return (3 * self.polarity_sub_model_verb +
                    2 * self.polarity_sub_model_adjective + self.polarity_sub_model_noun) / 6
        elif self.sub_model_verb and self.sub_model_noun:
            return (3 * self.polarity_sub_model_verb +
                    self.polarity_sub_model_noun) / 4
        elif self.sub_model_adjective and self.sub_model_noun:
            return (3 * self.polarity_sub_model_adjective + self.polarity_sub_model_noun) / 4
        elif self.sub_model_adjective and self.sub_model_verb:
            return (2 * self.polarity_sub_model_verb +
                    1 * self.polarity_sub_model_adjective) / 3
        elif self.sub_model_adjective:
            return self.polarity_sub_model_adjective
        elif self.sub_model_noun:
            return self.polarity_sub_model_noun
        elif self.sub_model_verb:
            return self.polarity_sub_model_verb

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
        elements_verb_polarity = AnalyseModels.get_polarity_adverb_neg(polarity_verb, adverb, neg, self.language)
        polarity_verb=elements_verb_polarity[0]
        while -1000 in elements_verb_polarity[1]:
            elements_verb_polarity[1].remove(-1000)
        if len(elements_verb_polarity[1]) > 0:
            mean_adv = np.array(elements_verb_polarity[1]).mean()
        else:
            mean_adv = 0

        if polarity_verb > 0:
            return polarity_verb + (1 - polarity_verb) * mean_adv
        else:
            return polarity_verb - (1 + polarity_verb) * mean_adv

    def get_elements_polarity_adjective(self, adj, adverb, neg):
        """recuper polarite groupe adjective """
        polarity_adj = 0
        if adj != "":
            polarity_adj = SentiWordNet.get_sentiment(adj, self.language, "a")
        elements_adjective_polarity = AnalyseModels.get_polarity_adverb_neg(polarity_adj, adverb, neg, self.language)
        polarity_adjective = elements_adjective_polarity[0]
        if len(elements_adjective_polarity[1]) > 0:  # calcul moyenne polarite adverbe
            mean_adv = np.array(elements_adjective_polarity[1]).mean()
        else:
            mean_adv = 0
        if polarity_adjective > 0:
            return polarity_adjective + (1 - polarity_adjective) * mean_adv
        else:
            return polarity_adjective - (1 - polarity_adjective) * mean_adv

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


class AnalyseFrenchModels(AnalyseModels):
    lexicon_lib = ""

    def __init__(self, language, model):
        self.language = language
        self.model_general = model
        self.lexicon_lib = lexicon.FrenchLexicon()

    def get_polarity_adverb_neg(self, polarity_element, adverb, neg, language):
        """recuprer polarite de liste des adverbes et negation"""
        polarity_adv_total = []
        if polarity_element != 0 and polarity_element != []:
            if neg:
                polarity_element = -1 * polarity_element
            if len(adverb) != 0:
                for adv in adverb:
                    polarity_adv = self.lexicon_lib.get_polarity_lexicon(adv, "RB")
                    if polarity_adv == -1000:
                        polarity_adv = SentiWordNet.get_sentiment(adv, language, "r")
                    if polarity_adv != -2000:
                        polarity_adv_total.append(polarity_adv)
        return polarity_element, polarity_adv_total

    def get_elements_polarity_verb(self, verb, adverb, neg):
        """recuper polarite groupe  verbe"""
        polarity_verb = 0
        if verb != "":
            polarity_verb = self.lexicon_lib.get_polarity_lexicon(verb, "VB")
            if polarity_verb == -1000:
                polarity_verb = SentiWordNet.get_sentiment(verb, self.language, "v")
        elements_verb_polarity = self.get_polarity_adverb_neg(polarity_verb, adverb, neg, self.language)
        polarity_verb = elements_verb_polarity[0]
        while -1000 in elements_verb_polarity[1]:
            elements_verb_polarity[1].remove(-1000)
        if len(elements_verb_polarity[1]) > 0:
            mean_adv = np.array(elements_verb_polarity[1]).mean()
        else:
            mean_adv = 0

        if polarity_verb > 0:
            return polarity_verb + (1 - polarity_verb) * mean_adv
        else:
            return polarity_verb - (1 + polarity_verb) * mean_adv

    def get_elements_polarity_adjective(self, adj, adverb, neg):
        """recuper polarite groupe adjective """
        polarity_adj = 0
        if adj != "":
            polarity_adj = self.lexicon_lib.get_polarity_lexicon(adj, "JJ")
            if polarity_adj == -1000:
                polarity_adj = SentiWordNet.get_sentiment(adj, self.language, "a")
        elements_adjective_polarity = AnalyseModels.get_polarity_adverb_neg(polarity_adj, adverb, neg,
                                                                            self.language)
        polarity_adjective = elements_adjective_polarity[0]
        if len(elements_adjective_polarity[1]) > 0:  # calcul moyenne polarite adverbe
            mean_adv = np.array(elements_adjective_polarity[1]).mean()
        else:
            mean_adv = 0
        if polarity_adjective > 0:
            return polarity_adjective + (1 - polarity_adjective) * mean_adv
        else:
            return polarity_adjective - (1 - polarity_adjective) * mean_adv


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
