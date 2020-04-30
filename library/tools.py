import numpy
import spacy
from enchant.checker import SpellChecker
from textblob import TextBlob as textblobEnglish, TextBlob
from textblob_ar import TextBlob as textblobArabic
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob_ar import TextBlob as nlpAr
from pattern.web import Twitter, cache

from library import analyse_models

textblob_arabic = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

nlpEn = spacy.load("en_core_web_sm")
nlpFr = spacy.load("fr_core_news_sm")


class Tools:
    sc_adv_start = "( "
    sc_adv_end = " ) "
    sc_adv_cordination = " && "
    sc_negation = " 7 "
    sc_verb = " <= "
    sc_adjective = " <= "

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
            phrase = nlpFr(content).sents
        elif language == "en":
            phrase = nlpEn(content).sents
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
                test_subjective = textblobEnglish(phrase)
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
        blob = blob.translate(from_lang=language_source, to=language_destination)
        return str(blob)

    @staticmethod
    def get_emoji_from_polarity(polarity):
        """entrer plarite et retourner emoji"""
        if polarity == -1000:
            return 128078
        elif polarity == 0:
            return 128529
        elif polarity < - 0.5:
            return 128531;
        elif polarity <= 0:
            return 128530
        elif polarity < 0.5:
            return 128522
        else:
            return 128514

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
