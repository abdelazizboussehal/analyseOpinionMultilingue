import spacy
from enchant.checker import SpellChecker
from textblob import TextBlob as textblobEnglish
from textblob_ar import TextBlob as textblobFrench
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob_ar import TextBlob as nlpAr
from pattern.web import Twitter, cache

textblob_arabic = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

nlpEn = spacy.load("en_core_web_sm")
nlpFr = spacy.load("fr_core_news_sm")


class Tools():

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
                test_subjective = textblobFrench(phrase)
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
