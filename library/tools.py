from textblob import TextBlob
import spacy

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
    def segmentationParPhrase(content, language):
        if language == "fr":
            phrase = nlpFr(content).sents
        elif language == "en":
            phrase = nlpEn(content).sents
        return phrase
