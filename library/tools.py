import numpy
import spacy
from enchant.checker import SpellChecker
from pattern.web import Twitter, cache
from spacy import displacy
from spacy.lang.en import English
from spacy.lang.fr import French
from spacy.matcher.phrasematcher import PhraseMatcher
from textblob import Blobber
from textblob import TextBlob as textblobEnglish, TextBlob
from textblob_ar import TextBlob as nlpAr
from textblob_fr import PatternTagger, PatternAnalyzer

from library import analyse_models

textblobFrench = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())


class Tools:
    # adverb
    sc_adv_start = "( "
    sc_adv_end = " ) "
    sc_adv_cordination = " &ad& "

    # verb
    sc_negation = " 7 "
    sc_verb = " <= "
    sc_verb_cordination = " &v& "
    sc_verb_start = " <<v "
    sc_verb_end = " v>> "

    # adjective
    sc_adjective = " <= "
    sc_adjective_start = " <<a "
    sc_adjective_end = " a>> "
    sc_adjective_cordination = " §§ "

    # noun
    sc_noun_addition = " && "
    sc_noun_start = " <<n "
    sc_noun_end = " n>> "

    # model gobal
    sc_model_global_start = " [ "
    sc_model_global_end = " ] "
    sc_model_global_connector = "cc>"

    # connector english
    addition = ["and", "plus", "furthermore", "moreover", "in addition", "also", ","]
    contract_end = ["but", "though", "nevertheless", "despite", "whereas", "while", "on the contrary",
                    "notwithstanding", "however"]
    contract_start = ["although"]
    # connector french
    contract_end_fr = ["mais", "quoique", "tandis que", "alors que", " même si", "cependant", "pourtant",
                       "toutefois", "néanmoins", "en revanche", "au contraire", "certes"]
    contract_start_fr = ["malgré tout", "malgré", "bien que"]
    addition_fr = ["et de même que", "sans compter que", "ainsi que", "ensuite", "voire", "d'ailleurs", "encore",
                   "de plus", "quant à", "non seulement", "mais encore", "de surcroît", "en outre", ","]
    verbC = []
    adjectifC = []
    nounC = []
    propnC = []
    auxC = []
    adverbC = []
    total = 0

    @staticmethod
    def read(path):
        f = open(path, "r")
        content = f.read()
        f.close()
        return content

    @staticmethod
    def write(content, name="models", extension="txt", folder="generated"):
        f = open(folder + "/" + name + "." + extension, "w")
        for line in content:
            f.write(line)
        f.close()

    @staticmethod
    def language_detection(content):
        blob = TextBlob(content)
        return blob.detect_language()

    @staticmethod
    def correction_orthographe(content, language):
        if language == "en":
            checker = SpellChecker("en_US")  # Fonction pour la langue anglais
        elif language == "fr":
            checker = SpellChecker("fr")  # Fonction pour la langue anglais
        checker.set_text(content)
        list_word = []
        list_suggestion = []
        for error in checker:
            list_word.append(error.word)  # Les mots erronés
            list_suggestion.append(error.suggest())  # Les suggestions
        return list_word, list_suggestion

    @staticmethod
    def sentence_segmentation(content, language):
        phrase = []
        content = str(content).lower()
        if language == "fr":
            nlp_fr = French()  # just the language with no model
            sentencizer = nlp_fr.create_pipe("sentencizer")
            nlp_fr.add_pipe(sentencizer)
            sentence = nlp_fr(content).sents

            for sent in sentence:
                phrase.append(str(sent))
        elif language == "en":
            nlp_en = English()  # just the language with no model
            sentencizer = nlp_en.create_pipe("sentencizer")
            nlp_en.add_pipe(sentencizer)
            sentence = nlp_en(content).sents
            for sent in sentence:
                phrase.append(str(sent))
        elif language == "ar":
            blob = nlpAr(content)
            for sentence in blob.sentences:
                phrase.append(str(sentence))

        return phrase

    @staticmethod
    def subjectivity_filtering(table_sentence, language):
        """enter une liste des phrases et la langue  retourner etat de la subjectivité"""
        subjective_stat = []  # table d'etat de subjecvité
        if language == "en":
            for phrase in table_sentence:
                test_subjective = textblobEnglish(str(phrase))  # utilise TextBlob pour la langue anglaise
                if test_subjective.sentiment.subjectivity > 0:
                    subjective_stat.append(True)
                else:
                    subjective_stat.append(False)
        elif language == "fr":
            for phrase in table_sentence:
                test_subjective = textblobFrench(u"" + phrase)  # utilise TextBlob pour la langue française
                if test_subjective.sentiment[1] > 0:
                    subjective_stat.append(True)
                else:
                    subjective_stat.append(False)
        return table_sentence, subjective_stat  # registre des segments linguistiques avec ses etats

    @staticmethod
    def get_twit_from_twitter(subject, number):
        """recuprer des twits depuis twitter avec l autor sur un sujet donne"""
        twitter = Twitter()
        index = None
        sentence = []
        for j in range(1):
            for tweet in twitter.search(subject, start=index, count=number):
                sentence.append((tweet.author, tweet.text, tweet.language))
        cache.clear()
        return sentence

    @staticmethod
    def translate_word_to_other_language(language_source, language_destination, word):
        blob = TextBlob(word)
        try:
            blob = blob.translate(from_lang=language_source, to=language_destination)
        except:
            return ""

        return str(blob)

    @staticmethod
    def get_emoji_from_polarity(polarity):
        """entrer plarite et retourner emoji"""
        if polarity is None:
            return 128373
        if polarity == -1996:
            return 128373
        if polarity == -1000:
            return 9940
        elif 1 >= polarity >= -1:
            if polarity < - 0.5:
                return "em em-cry"
            elif polarity < 0:
                return "em em-confused"
            elif polarity == 0:
                return "em em-neutral_face"
            elif polarity < 0.5:
                return "em em-smile"
            elif polarity <= 1:
                return "em em-sweat_smile"
        else:
            return 9940

    @staticmethod
    def mean_array_polarity_verb(array_model_verb, language):
        """ entrer array des model return la moyenne polarite """
        analyse_model = analyse_models.AnalyseModels(language)
        array_polarity_verb = []
        for amv in array_model_verb:
            polarity = analyse_model.calculation_polarity_verb(amv)
            if polarity != -1000:
                array_polarity_verb.append(polarity)
        return numpy.array(array_polarity_verb).mean()

    @staticmethod
    def mean_array_polarity_adjective(array_model_adjective, language):
        """ entrer array des model return la moyenne polarite """
        analyse_model = analyse_models.AnalyseModels(language)
        array_polarity_adjective = []
        for ama in array_model_adjective:
            polarity = analyse_model.calculation_polarity_adjective(ama)
            if polarity != -1000:
                array_polarity_adjective.append(polarity)
        return numpy.array(array_polarity_adjective).mean()

    @staticmethod
    def segmentation_with_connectors(text, language):
        """entrer un texte et resulation des phrases segemente par connecteur """
        """entrer un texte et resulation des phrases segemente par connecteur """
        if language == "fr":
            nlp = French()  # just the language with no model
            sentencizer = nlp.create_pipe("sentencizer")
            nlp.add_pipe(sentencizer)
        elif language == "en":
            nlp = English()  # just the language with no model
            sentencizer = nlp.create_pipe("sentencizer")
            nlp.add_pipe(sentencizer)

        def set_custom_boundaries(doc):
            matcher = PhraseMatcher(nlp.vocab)
            # Only run nlp.make_doc to speed things up
            if language == "fr":
                patterns_contract_end = [nlp.make_doc(text) for text in Tools.contract_end_fr]
                patterns_contract_start = [nlp.make_doc(text) for text in Tools.contract_start_fr]
                patterns_addition = [nlp.make_doc(text) for text in Tools.addition_fr]
            elif language == "en":
                patterns_contract_end = [nlp.make_doc(text) for text in Tools.contract_end]
                patterns_contract_start = [nlp.make_doc(text) for text in Tools.contract_start]
                patterns_addition = [nlp.make_doc(text) for text in Tools.addition]

            matcher.add("ContractListEnd", None, *patterns_contract_end)
            matcher.add("ContractListStart", None, *patterns_contract_start)
            matcher.add("AdditionList", None, *patterns_addition)
            matches = matcher(doc)
            for match_id, start, end in matches:
                string_id = nlp.vocab.strings[match_id]
                texteturu = doc[start:end]

                if string_id == "ContractListEnd":
                    doc[end].is_sent_start = True
                elif string_id == "ContractListStart":
                    doc[start].is_sent_start = True
                elif string_id == "AdditionList":
                    doc[start].is_sent_start = True
            return doc

        phrases = []
        nlp.add_pipe(set_custom_boundaries, after="sentencizer")
        doc = nlp(text)
        for sc in doc.sents:
            phrases.append(str(sc))
        return phrases

    @staticmethod
    def delete_string_from_end(text, suffix):
        if suffix and text.endswith(suffix):
            return text[:-len(suffix)]
        return text

    @staticmethod
    def statistic(sentence, langue):
        Tools.verbC = []
        Tools.adjectifC = []
        Tools.nounC = []
        Tools.propnC = []
        Tools.auxC = []
        Tools.adverbC = []
        Tools.total = 0
        if langue == "en":
            nlp = spacy.load("en_core_web_sm")
        elif langue == "fr":
            nlp = spacy.load("fr_core_news_md")
        doc = nlp(sentence)
        for token in doc:
            Tools.total += 1
            if token.pos_ == "VERB":
                Tools.verbC.append(str(token.text))
            if token.pos_ == "ADJ":
                Tools.adjectifC.append(str(token.text))
            if token.pos_ == "NOUN":
                Tools.nounC.append(str(token.text))
            if token.pos_ == "PROPN":
                Tools.propnC.append(str(token.text))
            if token.pos_ == "AUX":
                Tools.auxC.append(str(token.text))
            if token.pos_ == "ADV":
                Tools.adverbC.append(str(token.text))

    @staticmethod
    def visualize_dep(content, langue):
        nlp = ""
        doc = ""
        if langue == "en":
            nlp = spacy.load("en_core_web_sm")
        else:
            nlp = spacy.load("fr_core_news_sm")
        doc = nlp(content)
        options = {"compact": True, "bg": "#09a3d5",
                   "color": "white", "font": "Source Sans Pro"}
        return displacy.render(doc, style="dep", options=options)

    @staticmethod
    def visualize_ent(content, langue):
        nlp = ""
        doc = ""
        if langue == "en":
            nlp = spacy.load("en_core_web_sm")
        else:
            nlp = spacy.load("fr_core_news_sm")
        doc = nlp(content)
        return displacy.render(doc, style="ent")
