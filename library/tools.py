from textblob import TextBlob
import spacy
from enchant.checker import SpellChecker
import enchant
from textblob import TextBlob as textblob_en
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer

tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
from textblob_ar import TextBlob as textblob_fr

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
    def languageDetection(content):
        b = TextBlob(content)
        return b.detect_language()

    @staticmethod
    #correction orthographe
    def correction(content, langue):
        erreur = []
        if langue == "en":
            chkr = SpellChecker("en_US")
            chkr.set_text(content)
            for err in chkr:
                erreur.append("ERROR:" + err.word + " sugestion :" + str(err.suggest()))
            return erreur
        elif langue == "fr":
            chkr = SpellChecker("fr")
            chkr.set_text(content)
            for err in chkr:
                erreur.append("ERROR:" + err.word + " sugestion :" + str(err.suggest()))
            return erreur
        elif langue == "ar":
            chkr = SpellChecker("ar")
            chkr.set_text(content)
            for err in chkr:
                erreur.append("ERROR:" + err.word + " sugestion :" + str(err.suggest()))
            return erreur

    @staticmethod
    def segmentationParPhrase(content, language):
        if language == "fr":
            phrase = nlpFr(content).sents
        elif language == "en":
            phrase = nlpEn(content).sents
        return phrase

    @staticmethod
    def filtrageSubjectivity(content, language):
        resultat = []
        if language == "en":
            for phrase in content:
                testimonial = textblob_en(phrase)
                if testimonial.sentiment.subjectivity > 0:
                    resultat.append(phrase)
        elif language == "fr":
            for phrase in content:
                blob1 = tb(u"" + phrase)
                if blob1.sentiment[1] > 0:
                    resultat.append(phrase)

        elif language == "ar":
            for phrase in content:
                blob = textblob_fr(phrase)
                if blob.sentiment.subjectivity > 0:
                    resultat.append(phrase)
        return resultat
