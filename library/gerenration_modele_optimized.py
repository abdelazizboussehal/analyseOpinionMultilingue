import spacy
from spacy import displacy
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

    dependacy_tab = {'verbs': [], 'nouns': [], 'adjectives': []}

    # modele verbe et adjective et none et connecteur
    modele_globale = ""
    # modele segement linguistique
    modele_segement_linguistique_verbe = ""
    modele_segement_linguistique_adjectif = ""
    modele_segement_linguistique_nom = ""
    connector = ""

    vis_dep = ""
    vis_ent = ""

    def __init__(self, sentence):
        self.total = 0
        self.propnC = []
        self.auxC = []
        self.verbC = []
        self.adjectifC = []
        self.nounC = []
        self.adverbC = []
        self.nlp = spacy.load("en_core_web_sm")
        self.sentence = sentence
        # tableau des negation et modificateur et connector
        self.negation_adj = []
        self.modificateur_adj = []
        self.negation_verb = []
        self.modificateur_verb = []
        self.connectors = []
        # modele unite linguitique
        self.table_m_u_l_v = []
        self.table_m_u_l_a = []
        # jenere table de dependance
        self.extract_element_sub_model_adjective_verb()
        self.extract_element_sub_model_noun()


    def extract_element_sub_model_adjective_verb(self):
        """extraire liste des adjectifs avec ses modificateur"""
        table_adjectives_with_modifier = []
        table_verb_with_modifier = []
        doc = self.nlp(str(self.sentence))  # Générer dictionnaire d'unité linguistique et les relations

        self.vis_dep = displacy.render(doc, style="dep", options={"compact": True, "bg": "#09a3d5",
                                                                  "color": "white", "font": "Source Sans Pro"})
        self.vis_ent = displacy.render(doc, style="ent")
        for token in doc:

            self.total += 1
            if token.pos_ == "ADV":
                self.adverbC.append(str(token.text))
            if token.pos_ == "VERB":
                self.verbC.append(str(token.text))
            if token.pos_ == "ADJ":
                self.adjectifC.append(str(token.text))
            if token.pos_ == "NOUN":
                self.nounC.append(str(token.text))
            if token.pos_ == "PROPN":
                self.propnC.append(str(token.text))
            if token.pos_ == "AUX":
                self.auxC.append(str(token.text))


            if token.pos_ == "ADJ":  # si l'unite linguistique est une adjectif
                dependency_dicionary_adjective = {'adj': token.lemma_, 'neg': False, 'adv': []}
                adverb = []
                for child in token.children:  # les elements en ralation avec l'adjectif
                    if child.pos_ == "ADV":  # si l'unite linguistique est une adverbe
                        adverb.append(child.lemma_)  # garder seul le lemme
                    if child.dep_ == "neg" or child.text in self.table_word_negation:
                        dependency_dicionary_adjective["neg"] = True
                        self.negation_adj.append(child.text)
                if token.head.pos_ == "AUX":  # negation de l'adjectif avec auxiliaire
                    for child in token.head.children:
                        if child.text in self.table_word_negation or child.dep_ == "neg":
                            dependency_dicionary_adjective["neg"] = True
                dependency_dicionary_adjective['adv'] = adverb
                table_adjectives_with_modifier.append(dependency_dicionary_adjective)

            if token.pos_ == "VERB":  # si l'unite linguistique est une adjectif
                dependency_dicionary_verb = {'verb': token.lemma_, 'neg': False, 'adv': []}
                adverb = []
                for child in token.children:
                    if child.pos_ == "ADV" and child.text not in self.table_word_negation:
                        adv_test = True
                        adverb.append(child.lemma_)
                    if child.dep_ == "neg" or child.text in self.table_word_negation:
                        dependency_dicionary_verb['neg'] = True
                        self.negation_verb.append(child.text)

                dependency_dicionary_verb['adv'] = adverb
                table_verb_with_modifier.append(dependency_dicionary_verb)
        self.dependacy_tab['adjectives'] = table_adjectives_with_modifier
        self.dependacy_tab['verbs'] = table_verb_with_modifier

    def extract_element_sub_model_noun(self):
        doc = self.nlp(str(self.sentence))
        nouns = []
        for chunk in doc.noun_chunks:
            nouns.append(chunk.root.text)
        self.dependacy_tab['nouns'] = nouns

    def create_segment_model_adj(self):
        adverb_string = ""
        tables_dependacy_adj = self.dependacy_tab['adjectives']
        model_segment = t.Tools.sc_adjective_start  # separateur <<a
        for table_dependacy_adj in tables_dependacy_adj:  # pour chaque adjecvtive dans le segement linguitique
            model_unity = ""  # crée modèle unité linguistique adjective
            if table_dependacy_adj['neg']:
                model_unity = t.Tools.sc_negation + table_dependacy_adj['adj']  # ajouté negation dans le modèle
            else:
                model_unity = table_dependacy_adj['adj']
            if len(table_dependacy_adj['adv']) > 0:  # ajouter les adverbes dans le modèle
                adverb = table_dependacy_adj['adv']
                adverb_string = t.Tools.sc_adv_start
                for i in range(len(adverb) - 1):
                    adverb_string = adverb_string + adverb[i] + t.Tools.sc_adv_cordination
                adverb_string = adverb_string + adverb[len(adverb) - 1] + t.Tools.sc_adv_end
                model_unity = model_unity + t.Tools.sc_adjective + adverb_string
            self.table_m_u_l_a.append(model_unity)
            model_segment = model_segment + model_unity + t.Tools.sc_adjective_cordination

        # pour suprimer le dernier serparateur &a&
        model_segment = t.Tools.delete_string_from_end(model_segment, t.Tools.sc_adjective_cordination)
        self.modele_segement_linguistique_adjectif = model_segment + t.Tools.sc_adjective_end  # separateur a>>

    def create_segment_model_verb(self):
        adverb_string = ""
        tables_dependacy_verb = self.dependacy_tab['verbs']
        model_segment = t.Tools.sc_verb_start  # separateur <<a
        for table_dependacy_verb in tables_dependacy_verb:  # pour chaque adjecvtive dans le segement linguitique
            model_unity = ""  # crée modèle unité linguistique adjective
            if table_dependacy_verb['neg']:
                model_unity = t.Tools.sc_negation + table_dependacy_verb['verb']  # ajouté negation dans le modèle
            else:
                model_unity = table_dependacy_verb['verb']
            if len(table_dependacy_verb['adv']) > 0:  # ajouter les adverbes dans le modèle
                adverb = table_dependacy_verb['adv']
                adverb_string = t.Tools.sc_adv_start
                for i in range(len(adverb) - 1):
                    adverb_string = adverb_string + adverb[i] + t.Tools.sc_adv_cordination
                adverb_string = adverb_string + adverb[len(adverb) - 1] + t.Tools.sc_adv_end
                model_unity = model_unity + t.Tools.sc_adjective + adverb_string
            self.table_m_u_l_v.append(model_unity)
            model_segment = model_segment + model_unity + t.Tools.sc_adjective_cordination

        # pour suprimer le dernier serparateur &a&
        model_segment = t.Tools.delete_string_from_end(model_segment, t.Tools.sc_adjective_cordination)
        self.modele_segement_linguistique_verbe = model_segment + t.Tools.sc_verb_end  # separateur a>>

    def create_segment_model_noun(self):
        self.extract_element_sub_model_noun()
        sub_model_nouns = t.Tools.sc_noun_start
        for noun in self.dependacy_tab['nouns']:
            sub_model_nouns = sub_model_nouns + noun + t.Tools.sc_noun_addition
        self.modele_segement_linguistique_nom = t.Tools.delete_string_from_end(sub_model_nouns,
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
            # gat texte
            span = doc[start:end]
            self.connectors.append(str(span.text))
            if string_id == "ContractListEnd" or string_id == "ContractListStart":
                self.connector = " 7 "
                break
            elif string_id == "AdditionList":
                self.connector = " + "
                break
            else:
                self.connector = "none"

    def create_model(self):
        self.create_segment_model_noun()
        self.create_segment_model_verb()
        self.create_segment_model_adj()
        self.extract_connector()
        model = t.Tools.sc_model_global_start
        if self.connector != "none":
            model = model + t.Tools.sc_model_global_connector + self.connector
        if len(self.dependacy_tab['verbs']) > 0:
            model = model + self.modele_segement_linguistique_verbe
        if len(self.dependacy_tab['adjectives']) > 0:
            model = model + self.modele_segement_linguistique_adjectif
        if len(self.dependacy_tab['nouns']) > 0:
            model = model + self.modele_segement_linguistique_nom
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
        self.total = 0
        self.adverbC = []
        self.propnC = []
        self.auxC = []
        self.verbC = []
        self.adjectifC = []
        self.nounC = []
        self.sentence = sentence
        self.negation_adj = []
        self.modificateur_adj = []
        self.negation_verb = []
        self.modificateur_verb = []
        self.connector_negation_table = []
        self.connector_addition_table = []

        self.connectors = []
        # modele unite linguitique
        self.table_m_u_l_v = []
        self.table_m_u_l_a = []
        # jenere table de dependance
        self.extract_element_sub_model_adjective_verb()
        self.extract_element_sub_model_noun()

    def extract_element_sub_model_adjective_verb(self):
        """extraire liste des adjectifs avec ses modificateur"""
        table_adjectives_with_modifier = []
        table_verb_with_modifier = []
        doc = self.nlp(str(self.sentence))  # Générer dictionnaire d'unité linguistique et les relations

        self.vis_dep = displacy.render(doc, style="dep", options={"compact": True, "bg": "#09a3d5",
                                                                  "color": "white", "font": "Source Sans Pro"})
        self.vis_ent = displacy.render(doc, style="ent")
        for token in doc:

            self.total += 1
            if token.pos_ == "ADV":
                self.adverbC.append(str(token.text))
            if token.pos_ == "VERB":
                self.verbC.append(str(token.text))
            if token.pos_ == "ADJ":
                self.adjectifC.append(str(token.text))
            if token.pos_ == "NOUN":
                self.nounC.append(str(token.text))
            if token.pos_ == "PROPN":
                self.propnC.append(str(token.text))
            if token.pos_ == "AUX":
                self.auxC.append(str(token.text))


            if token.pos_ == "ADJ":  # si l'unite linguistique est une adjectif
                dependency_dicionary_adjective = {'adj': token.lemma_, 'neg': False, 'adv': []}
                adverb = []
                for child in token.children:  # les elements en ralation avec l'adjectif
                    if child.pos_ == "ADV":  # si l'unite linguistique est une adverbe
                        adverb.append(child.lemma_)  # garder seul le lemme
                    if child.dep_ == "neg" or child.text in self.table_word_negation:
                        dependency_dicionary_adjective["neg"] = True
                        self.negation_adj.append(child.text)
                aziz = token.head.text
                if token.head.pos_ == "AUX":  # negation de l'adjectif avec auxiliaire
                    for child in token.head.children:
                        if child.text in self.table_word_negation or child.dep_ == "neg":
                            dependency_dicionary_adjective["neg"] = True
                dependency_dicionary_adjective['adv'] = adverb
                table_adjectives_with_modifier.append(dependency_dicionary_adjective)

            if token.pos_ == "VERB":  # si l'unite linguistique est une adjectif
                dependency_dicionary_verb = {'verb': token.lemma_, 'neg': False, 'adv': []}
                adverb = []
                for child in token.children:
                    if child.pos_ == "ADV" and child.text not in self.table_word_negation:
                        adv_test = True
                        adverb.append(child.lemma_)
                    if child.dep_ == "neg" or child.text in self.table_word_negation:
                        dependency_dicionary_verb['neg'] = True
                        self.negation_verb.append(child.text)

                dependency_dicionary_verb['adv'] = adverb
                table_verb_with_modifier.append(dependency_dicionary_verb)

        self.dependacy_tab['adjectives'] = table_adjectives_with_modifier
        self.dependacy_tab['verbs'] = table_verb_with_modifier
