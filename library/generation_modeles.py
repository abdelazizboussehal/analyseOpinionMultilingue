import spacy
from spacy.matcher.phrasematcher import PhraseMatcher

from library import tools as t


class GenerationModels:
    table_word_negation = ["isn't", "no", "not", "n't", "never", "none", "nobody", "nowhere", "nothing", "neither",
                           "do not",
                           "have not"]
    # connector english
    addition = ["and", "plus", "furthermore", "moreover", "in addition", "also"]
    contract_end = ["but", "though", "nevertheless", "whereas", "on the contrary", "in contrast", "on the other hand",
                    "notwithstanding"]
    contract_start = ["although", "however", "despite", "while", "whereas"]
    # elemnt
    element_modele_segement_linguistique_verbe = []
    element_modele_segement_linguistique_adjectif = []
    element_modele_segement_linguistique_nom = []
    # modele verbe et adjective et none et connecteur
    sentence = ""
    modele_globale = ""
    # modele segement linguistique
    modele_segement_linguistique_verbe = ""
    modele_segement_linguistique_adjectif = ""
    modele_segement_linguistique_nom = ""
    connector = ""

    def __init__(self, sentence):
        self.nlp = spacy.load("en_core_web_sm")
        self.sentence = sentence
        # tableau des negation et modificateur et connector
        self.negation_adj = []
        self.modificateur_adj = []
        self.negation_verb = []
        self.modificateur_verb = []
        self.connector_negation_table = []
        self.connector_addition_table = []
        # modele unite linguitique
        self.table_m_u_l_v = []
        self.table_m_u_l_a = []

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
                    if child.pos_ == "ADV" and child.text not in self.table_word_negation:
                        adv_test = True
                        adv.append(child.lemma_)
                    if child.dep_ == "neg" or child.text in self.table_word_negation:
                        neg = True
                        self.negation_verb.append(str(child.text))
                if neg:
                    v = t.Tools.sc_negation + token.lemma_
                else:
                    v = token.text
                if adv_test:
                    text_adv = t.Tools.sc_adv_start
                    for i in range(len(adv) - 1):
                        self.modificateur_verb.append(adv[i])
                        text_adv = text_adv + adv[i] + t.Tools.sc_adv_cordination
                    text_adv = text_adv + adv[len(adv) - 1] + t.Tools.sc_adv_end
                    v = v + t.Tools.sc_verb + text_adv
                verb.append(v)
            self.element_modele_segement_linguistique_verbe = verb

    def create_sub_model_verb(self):
        """ cree sous model adjective """
        self.extract_element_sub_model_verb()
        sub_model_verb = t.Tools.sc_verb_start
        for verb in self.element_modele_segement_linguistique_verbe:
            sub_model_verb = sub_model_verb + verb + t.Tools.sc_verb_cordination
            self.table_m_u_l_v.append(verb)
        sub_model_verb = t.Tools.delete_string_from_end(sub_model_verb, t.Tools.sc_verb_cordination)
        self.modele_segement_linguistique_verbe = sub_model_verb + t.Tools.sc_verb_end

    def extract_element_sub_model_adjective(self):
        """extraire les adjectives avec la negation s'il existe"""
        doc = self.nlp(str(self.sentence))  # dictionnaire d'unité linguistique et les relations
        adjective = []
        for token in doc:

            if token.pos_ == "ADJ":  # si l'unite linguistique est une adjectif
                negation = ""
                adverb = []
                adverb_string = ""
                for child in token.children:  # les elements en ralation avec l'adjectif
                    if child.pos_ == "ADV":  # si l'unite linguistique est une adverbe
                        adverb.append(child.lemma_)  # garder seul le lemme
                    if child.dep_ == "neg" or child.text in self.table_word_negation:
                        negation = t.Tools.sc_negation
                        self.negation_adj.append(str(child.text))
                if token.head.pos_ == "AUX":  # negation de l'adjectif avec auxiliaire
                    for child in token.head.children:
                        if child.text in self.table_word_negation:
                            negation = t.Tools.sc_negation
                            self.negation_adj.append(str(child.text))

                if len(adverb) > 0:
                    adverb_string = t.Tools.sc_adv_start
                    for i in range(len(adverb) - 1):
                        adverb_string = adverb_string + adverb[i] + t.Tools.sc_adv_cordination
                        self.modificateur_adj.append(adverb[i])
                    adverb_string = adverb_string + adverb[len(adverb) - 1] + t.Tools.sc_adv_end
                    self.modificateur_adj.append(adverb[len(adverb) - 1])

                    adjective.append(negation + token.lemma_ + t.Tools.sc_adjective + adverb_string)
                else:
                    adjective.append(negation + token.lemma_)
            self.element_modele_segement_linguistique_adjectif = adjective

    def create_sub_model_adjective(self):
        """cree sous modele adjective """
        self.extract_element_sub_model_adjective()
        sub_model_adjective = t.Tools.sc_adjective_start
        for adjective in self.element_modele_segement_linguistique_adjectif:
            sub_model_adjective = sub_model_adjective + adjective + t.Tools.sc_adjective_cordination
            self.table_m_u_l_a.append(adjective)
        sub_model_adjective = t.Tools.delete_string_from_end(sub_model_adjective, t.Tools.sc_adjective_cordination)
        self.modele_segement_linguistique_adjectif = sub_model_adjective + t.Tools.sc_adjective_end

    def extract_element_sub_model_noun(self):
        doc = self.nlp(str(self.sentence))
        nouns = []
        for chunk in doc.noun_chunks:
            nouns.append(chunk.root.text)
        self.element_modele_segement_linguistique_nom = nouns

    def create_sub_model_noun(self):
        self.extract_element_sub_model_noun()
        sub_model_nouns = t.Tools.sc_noun_start
        for noun in self.element_modele_segement_linguistique_nom:
            sub_model_nouns = sub_model_nouns + noun + t.Tools.sc_noun_addition
        self.sub_model_noun = t.Tools.delete_string_from_end(sub_model_nouns,
                                                             t.Tools.sc_noun_addition) + t.Tools.sc_noun_end

    def extract_connector(self):
        doc = self.nlp(str(self.sentence).lower())
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
            # gat texte
            span = doc[start:end]
            if string_id == "ContractListEnd" or string_id == "ContractListStart":
                self.connector_negation_table.append(str(span.text))
                self.connector = " 7 "
                break
            elif string_id == "AdditionList":
                self.connector_addition_table.append(str(span.text))
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
        if len(self.element_modele_segement_linguistique_verbe) > 0:
            model = model + self.modele_segement_linguistique_verbe
        if len(self.element_modele_segement_linguistique_adjectif) > 0:
            model = model + self.modele_segement_linguistique_adjectif
        if len(self.element_modele_segement_linguistique_nom) > 0:
            model = model + self.sub_model_noun
        self.modele_globale = model + t.Tools.sc_model_global_end


class GenerationFrenchModels(GenerationModels):
    table_word_negation = ["n'", "ne", "ni", "non", "pas", "rien", "sans", "aucun", "jamais"]
    alternative = ["t'"]
    # connector french
    contract_end = ["mais", "quoique", "tandis que", "alors que", " même si", "cependant", "pourtant",
                    "toutefois", "néanmoins", "en revanche", "au contraire", "certes"]
    contract_start = ["malgré tout", "malgré", "bien que"]
    addition = ["et de même que", "sans compter que", "ainsi que", "ensuite", "voire", "d'ailleurs", "encore",
                "de plus", "quant à", "non seulement", "mais encore", "de surcroît", "en outre"]

    def __init__(self, sentence):
        self.nlp = spacy.load("fr_core_news_sm")
        self.sentence = sentence
        self.negation_adj = []
        self.modificateur_adj = []
        self.negation_verb = []
        self.modificateur_verb = []
        self.connector_negation_table = []
        self.connector_addition_table = []

        # modele unite linguitique
        self.table_m_u_l_v = []
        self.table_m_u_l_a = []

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
                        self.negation_verb.append(child.text)
                        continue
                    if child.text in self.table_word_negation:

                        self.negation_verb.append(child.text)
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
                        self.modificateur_verb.append(adv[i])
                    text_adv = text_adv + adv[len(adv) - 1] + t.Tools.sc_adv_end
                    self.modificateur_verb.append(adv[len(adv) - 1])
                    v = v + t.Tools.sc_verb + text_adv
                verb.append(v)
        self.element_modele_segement_linguistique_verbe = verb

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
                    if child.text in self.table_word_negation:
                        neg = t.Tools.sc_negation
                        self.negation_adj.append(child.text)
                    elif child.pos_ == "ADV":
                        adv.append(child.lemma_)
                if len(adv) > 0:
                    adverb = t.Tools.sc_adv_start
                    for i in range(len(adv) - 1):
                        adverb = adverb + adv[i] + t.Tools.sc_adv_cordination
                        self.modificateur_adj.append(adv[i])
                    adverb = adverb + adv[len(adv) - 1] + t.Tools.sc_adv_end
                    self.modificateur_adj.append(adv[len(adv) - 1])

                    adjective.append(neg + token.lemma_ + t.Tools.sc_adjective + adverb)
                else:
                    adjective.append(neg + token.lemma_)
        self.element_modele_segement_linguistique_adjectif = adjective
