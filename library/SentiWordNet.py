import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from library import tools as t
from nltk.stem import WordNetLemmatizer


class SentiWordNet:

    @staticmethod
    def get_sentiment(word, language, tag):
        """ recuperer le polarite d'un mot """
        if language == "ar" or language == "fr" or language == "en":
            if language != "en":
                word = t.Tools.translate_word_to_other_language(language, "en", word)
                print(word)
        else:
            return []

        synsets = wn.synsets(word, pos=tag)
        if not synsets:
            return -2000

        # Take the first sense, the most common
        synset = synsets[0]

        swn_synset = swn.senti_synset(synset.name())
        if swn_synset.pos_score() == swn_synset.neg_score() == 0:  # neutre
            return 0
        elif swn_synset.pos_score() == swn_synset.neg_score():  # egaux pos 0.5 neg 0.5
            return swn_synset.pos_score()
        elif swn_synset.pos_score() < swn_synset.neg_score():
            return -1 * swn_synset.neg_score()
        elif swn_synset.pos_score() > swn_synset.neg_score():
            return swn_synset.pos_score()
        elif tag == "r":
            return max(swn_synset.pos_score(), swn_synset.neg_score())