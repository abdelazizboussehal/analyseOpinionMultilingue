import xml.dom.minidom
from textblob.translate import Translator


class Lexicon:
    doc = ""

    def __init__(self):
        self.doc = xml.dom.minidom.parse("ven/Lib/site-packages/textblob/en/en-sentiment.xml")

    def get_polarity_lexicon(self, word, pos):
        """ entrer mot et type retourne ça polarite"""
        word = str(word).lower()
        expertise = self.doc.getElementsByTagName("word")

        for skill in expertise:
            if skill.getAttribute("pos") == pos and skill.getAttribute("form") == word:  # cherche le mot
                return skill.getAttribute("polarity")
        return -1000  # n'existe pas ce mot


class FrenchLexicon(Lexicon):
    def __init__(self):
        self.doc = xml.dom.minidom.parse("ven/Lib/site-packages/pattern/text/fr/fr-sentiment.xml")


class ArabicLexicon(Lexicon):

    def get_polarity_lexicon(self, word, pos):
        """ entrer mot et type retourne ça polarite"""
        word = Translator().translate(word, from_lang='ar')
        return super().get_polarity_lexicon(word, pos)
