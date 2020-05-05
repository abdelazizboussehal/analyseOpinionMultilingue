from operator import itemgetter
import spacy
from library import tools as t


class GenerationModels:
    neg = ["no", "not", "n't", "never", "none", "nobody", "nowhere", "nothing", "neither"]

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_verb_with_modifier(self, sentence):
        """extraire le verbe avec leur negation et ces adverbes s'ils existe"""

        doc = self.nlp(str(sentence))
        verb = []
        for token in doc:
            v = ""
            neg = False
            adv_test = False
            adv = []

            if token.pos_ == "VERB":
                for child in token.children:
                    if child.pos_ == "ADV" and child.text not in self.neg:
                        adv_test = True
                        adv.append(child.lemma_)
                    if child.dep_ == "neg" or child.text in self.neg:
                        neg = True
                if neg:
                    v = t.Tools.sc_negation + token.lemma_
                else:
                    v = token.text
                if adv_test:
                    text_adv = t.Tools.sc_adv_start
                    for i in range(len(adv) - 1):
                        text_adv = text_adv + adv[i] + t.Tools.sc_adv_cordination
                    text_adv = text_adv + adv[len(adv) - 1] + t.Tools.sc_adv_end
                    v = v + t.Tools.sc_verb + text_adv
                verb.append(v)
        return verb

    def extract_adjective(self, text):
        """extraire les adjectives avec la negation s'il existe"""
        doc = self.nlp(str(text))
        adjective = []
        for token in doc:

            if token.pos_ == "ADJ":
                neg = ""
                adv = []
                adverb = ""
                for child in token.children:
                    if child.pos_ == "ADV":
                        adv.append(child.lemma_)
                    if child.dep_ == "neg":
                        neg = t.Tools.sc_negation
                if token.head.pos_ == "AUX":
                    for child in token.head.children:
                        if child.text in self.neg:
                            neg = t.Tools.sc_negation

                if len(adv) > 0:
                    adverb = t.Tools.sc_adv_start
                    for i in range(len(adv) - 1):
                        adverb = adverb + adv[i] + t.Tools.sc_adv_cordination
                    adverb = adverb + adv[len(adv) - 1] + t.Tools.sc_adv_end

                    adjective.append(neg + token.lemma_ + t.Tools.sc_adjective + adverb)
                else:
                    adjective.append(neg + token.lemma_)
        return adjective

    def extract_noun_and_noun_complex(self, text):
        doc = self.nlp(str(text))
        nouns = t.Tools.sc_noun_start
        for chunk in doc.noun_chunks:
            nouns = nouns + chunk.root.text + t.Tools.sc_noun_addition
        nouns = t.Tools.delete_string_from_end(nouns, t.Tools.sc_noun_addition) + t.Tools.sc_noun_end

        return nouns

    def extract_connector(self, text):
        doc = self.nlp(str(text))
        for token in doc:
            if str(token.text).lower() in t.Tools.contract:
                return "7"
            if str(token.text).lower() in t.Tools.addition:
                return "+"
        return "none"


class GenerationFrenchModels(GenerationModels):
    neg = ["n'", "ne", "ni", "non", "pas", "rien", "sans", "aucun", "jamais"]
    alternative = ["t'"]

    def __init__(self):
        self.nlp = spacy.load("fr_core_news_md")

    def extract_verb_with_modifier(self, sentence):
        """extraire le verbe avec leur negation et ces adverbes s'ils existe"""

        doc = self.nlp(sentence)
        verb = []
        for token in doc:
            v = ""
            neg = False
            adv_test = False
            adv = []
            if token.text in self.alternative:
                continue
            if token.pos_ == "VERB" or token.pos_ == "AUX":
                for child in token.children:
                    if child.text in self.alternative:
                        continue
                    if child.text in self.neg:
                        print(child.text)
                        neg = True
                    elif child.pos_ == "ADV":
                        adv_test = True
                        adv.append(child.lemma_)

                if neg:
                    v = t.Tools.sc_negation + token.lemma_
                else:
                    v = token.text
                if adv_test:
                    text_adv = t.Tools.sc_adv_start
                    for i in range(len(adv) - 1):
                        text_adv = text_adv + adv[i] + t.Tools.sc_adv_cordination
                    text_adv = text_adv + adv[len(adv) - 1] + t.Tools.sc_adv_end
                    v = v + t.Tools.sc_verb + text_adv
                verb.append(v)
        return verb

    def extract_adjective(self, text):
        """extraire les adjectives avec la negation s'il existe"""
        doc = self.nlp(text)
        adjective = []
        for token in doc:

            if token.pos_ == "ADJ":
                neg = ""
                adv = []
                adverb = ""
                for child in token.children:
                    if child.text in self.neg:
                        neg = t.Tools.sc_negation
                    elif child.pos_ == "ADV":
                        adv.append(child.lemma_)

                if len(adv) > 0:
                    adverb = t.Tools.sc_adv_start
                    for i in range(len(adv) - 1):
                        adverb = adverb + adv[i] + t.Tools.sc_adv_cordination
                    adverb = adverb + adv[len(adv) - 1] + t.Tools.sc_adv_end

                    adjective.append(neg + token.lemma_ + t.Tools.sc_adjective + adverb)
                else:
                    adjective.append(neg + token.lemma_)
        return adjective
