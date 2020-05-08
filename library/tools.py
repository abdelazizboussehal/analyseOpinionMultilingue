import numpy
import spacy
from enchant.checker import SpellChecker
from spacy.matcher.phrasematcher import PhraseMatcher
from textblob import TextBlob as textblobEnglish, TextBlob
from textblob_ar import TextBlob as textblobArabic
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob_ar import TextBlob as nlpAr
from pattern.web import Twitter, cache
from spacy.lang.en import English
from spacy.lang.fr import French

from library import analyse_models

textblob_arabic = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())


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
    addition = ["and", "plus", "furthermore", "moreover", "in addition", "also"]
    contract_end = ["but", "though", "nevertheless", "despite", "whereas", "while", "on the contrary",
                    "notwithstanding", "however"]
    contract_start = ["although"]
    # connector french
    contract_end_fr = ["mais", "quoique", "tandis que", "alors que", " même si", "cependant", "pourtant",
                       "toutefois", "néanmoins", "en revanche", "au contraire", "certes"]
    contract_start_fr = ["malgré tout", "malgré", "bien que"]
    addition_fr = ["et de même que", "sans compter que", "ainsi que", "ensuite", "voire", "d'ailleurs", "encore",
                   "de plus", "quant à", "non seulement", "mais encore", "de surcroît", "en outre"]

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
        blob = textblobEnglish(content)
        return blob.detect_language()

    @staticmethod
    def correction_orthographe(content, language):
        """"""
        list_error = []
        if language == "en":
            checker = SpellChecker("en_US")
        elif language == "fr":
            checker = SpellChecker("fr")
        elif language == "ar":
            checker = SpellChecker("ar")

        checker.set_text(content)
        for err in checker:
            list_error.append("ERROR:" + err.word + " sugestion :" + str(err.suggest()))
        return list_error

    @staticmethod
    def sentence_segmentation(content, language):
        if language == "fr":
            nlp_fr = French()  # just the language with no model
            sentencizer = nlp_fr.create_pipe("sentencizer")
            nlp_fr.add_pipe(sentencizer)
            phrase = nlp_fr(content).sents
        elif language == "en":
            nlp_en = English()  # just the language with no model
            sentencizer = nlp_en.create_pipe("sentencizer")
            nlp_en.add_pipe(sentencizer)
            phrase = nlp_en(content).sents
        elif language == "ar":
            blob = nlpAr(content)
            phrase = []
            for sentence in blob.sentences:
                phrase.append(str(sentence))
        return phrase

    @staticmethod
    def subjectivity_filtering(content, language):
        """enter une liste des phrases et la langue  retourner seul qui sont subjective"""
        subjective_sentence = []
        subjective_stat = []
        if language == "en":
            for phrase in content:
                test_subjective = textblobEnglish(str(phrase))
                if test_subjective.sentiment.subjectivity > 0:
                    subjective_sentence.append(phrase)
                    subjective_stat.append(True)
                else:
                    subjective_stat.append(False)
        elif language == "fr":
            for phrase in content:
                test_subjective = textblob_arabic(u"" + phrase)
                if test_subjective.sentiment[1] > 0:
                    subjective_sentence.append(phrase)
                    subjective_stat.append(True)
                else:
                    subjective_stat.append(False)

        elif language == "ar":
            for phrase in content:
                test_subjective = textblobArabic(phrase)
                if test_subjective.sentiment.subjectivity > 0:
                    subjective_sentence.append(phrase)
                    subjective_stat.append(True)
                else:
                    subjective_stat.append(False)

        return subjective_sentence, subjective_stat

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
        if polarity == -1000:
            return 9940
        elif 1 >= polarity >= -1:
            if polarity < - 0.5:
                return 128545
            elif polarity < 0:
                return 128542
            elif polarity == 0:
                return 128528
            elif polarity < 0.5:
                return 128513
            elif polarity <= 1:
                return 128514
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
                print(texteturu)
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
