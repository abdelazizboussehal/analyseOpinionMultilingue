from operator import itemgetter
import spacy
from spacy.matcher.phrasematcher import PhraseMatcher

from library import tools as t


class GenerationModels:
    neg = ["no", "not", "n't", "never", "none", "nobody", "nowhere", "nothing", "neither"]
    # connector english
    addition = ["and", "plus", "furthermore", "moreover", "in addition", "also"]
    contract_end = ["but", "though", "nevertheless", "despite", "whereas", "while", "on the contrary",
                    "notwithstanding"]
    contract_start = ["although", "however"]
    # elemnt
    element_sub_model_verb = []
    element_sub_model_adjective = []
    element_sub_model_noun = []
    # modele verbe et adjective et none et connecteur
    sentence = ""
    model_general = ""
    sub_model_verb = ""
    sub_model_adjective = ""
    sub_sub_model_noun = ""
    connector = ""

    def __init__(self, sentence):
        self.nlp = spacy.load("en_core_web_sm")
        self.sentence = sentence

    def extract_element_sub_model_verb(self):
        """extraire le verbe avec leur negation et ces adverbes s'ils existe"""

        doc = self.nlp(str(self.sentence))
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
            self.element_sub_model_verb = verb

    def create_sub_model_verb(self):
        """ cree sous model adjective """
        self.extract_element_sub_model_verb()
        sub_model_verb = t.Tools.sc_verb_start
        for verb in self.element_sub_model_verb:
            sub_model_verb = sub_model_verb + verb + t.Tools.sc_verb_cordination
        sub_model_verb = t.Tools.delete_string_from_end(sub_model_verb, t.Tools.sc_verb_cordination)
        self.sub_model_verb = sub_model_verb + t.Tools.sc_verb_end

    def extract_element_sub_model_adjective(self):
        """extraire les adjectives avec la negation s'il existe"""
        doc = self.nlp(str(self.sentence))
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
            self.element_sub_model_adjective = adjective

    def create_sub_model_adjective(self):
        """cree sous modele adjective """
        self.extract_element_sub_model_adjective()
        sub_model_adjective = t.Tools.sc_adjective_start
        for adjective in self.element_sub_model_adjective:
            sub_model_adjective = sub_model_adjective + adjective + t.Tools.sc_adjective_cordination
        sub_model_adjective = t.Tools.delete_string_from_end(sub_model_adjective, t.Tools.sc_adjective_cordination)
        self.sub_model_adjective = sub_model_adjective + t.Tools.sc_adjective_end

    def extract_element_sub_model_noun(self):
        doc = self.nlp(str(self.sentence))
        nouns = []
        for chunk in doc.noun_chunks:
            nouns.append(chunk.root.text)
        self.element_sub_model_noun = nouns

    def create_sub_model_noun(self):
        self.extract_element_sub_model_noun()
        sub_model_nouns = t.Tools.sc_noun_start
        for noun in self.element_sub_model_noun:
            sub_model_nouns = sub_model_nouns + noun + t.Tools.sc_noun_addition
        self.sub_model_noun = t.Tools.delete_string_from_end(sub_model_nouns,
                                                             t.Tools.sc_noun_addition) + t.Tools.sc_noun_end

    def extract_connector(self):
        doc = self.nlp(self.sentence)
        matcher = PhraseMatcher(self.nlp.vocab)
        patterns_contract_end = [self.nlp.make_doc(text) for text in self.contract_end]
        patterns_contract_start = [self.nlp.make_doc(text) for text in self.contract_start]
        patterns_addition = [self.nlp.make_doc(text) for text in self.addition]
        matcher.add("ContractListEnd", None, *patterns_contract_end)
        matcher.add("ContractListStart", None, *patterns_contract_start)
        matcher.add("AdditionList", None, *patterns_addition)
        matches = matcher(doc)
        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]
            if string_id == "ContractListEnd" or string_id == "ContractListStart":
                self.connector = " 7 "
                break
            elif string_id == "AdditionList":
                self.connector = " + "
                break
            else:
                self.connector = "none"

    def create_model(self):
        self.create_sub_model_noun()
        self.create_sub_model_adjective()
        self.create_sub_model_verb()
        self.extract_connector()
        model = t.Tools.sc_model_global_start
        if self.connector != "none":
            model = model + t.Tools.sc_model_global_connector + self.connector
        if len(self.element_sub_model_verb) > 0:
            model = model + self.sub_model_verb
        if len(self.element_sub_model_adjective) > 0:
            model = model + self.sub_model_adjective
        if len(self.element_sub_model_noun) > 0:
            model = model + self.sub_model_noun
        self.model_general = model + t.Tools.sc_model_global_end


class GenerationFrenchModels(GenerationModels):
    neg = ["n'", "ne", "ni", "non", "pas", "rien", "sans", "aucun", "jamais"]
    alternative = ["t'"]
    # connector french
    contract_end = ["mais", "quoique", "tandis que", "alors que", " même si", "cependant", "pourtant",
                    "toutefois", "néanmoins", "en revanche", "au contraire", "certes"]
    contract_start = ["malgré tout", "malgré", "bien que"]
    addition = ["et de même que", "sans compter que", "ainsi que", "ensuite", "voire", "d'ailleurs", "encore",
                "de plus", "quant à", "non seulement", "mais encore", "de surcroît", "en outre"]

    def __init__(self, sentence):
        self.nlp = spacy.load("fr_core_news_md")
        self.sentence = sentence

    def extract_element_sub_model_verb(self):
        """extraire le verbe avec leur negation et ces adverbes s'ils existe"""

        doc = self.nlp(self.sentence)
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
        self.element_sub_model_verb = verb

    def extract_element_sub_model_adjective(self):
        """extraire les adjectives avec la negation s'il existe"""
        doc = self.nlp(self.sentence)
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
        self.element_sub_model_adjective = adjective
