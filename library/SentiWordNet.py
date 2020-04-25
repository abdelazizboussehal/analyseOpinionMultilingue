import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


class SentiWordNet:
    @staticmethod
    def penn_to_wn(tag):
        """
        Convert between the PennTreebank tags to simple Wordnet tags
        """
        if tag.startswith('J'):
            return wn.ADJ
        elif tag.startswith('N'):
            return wn.NOUN
        elif tag.startswith('R'):
            return wn.ADV
        elif tag.startswith('V'):
            return wn.VERB
        return None

    @staticmethod
    def get_sentiment(word):
        """ returns list of pos neg and objective score. But returns empty list if not present in senti wordnet. """
        words_data = [word]

        pos_val = nltk.pos_tag(words_data)
        if len(pos_val) > 0:
            word = pos_val[0][0]
            tag = pos_val[0][1]
        else:
            word = []
            tag = []
        lemmatizer = WordNetLemmatizer()
        wn_tag = SentiWordNet.penn_to_wn(tag)
        if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
            return []

        lemma = lemmatizer.lemmatize(word, pos=wn_tag)
        if not lemma:
            return []

        synsets = wn.synsets(word, pos=wn_tag)
        if not synsets:
            return []

        # Take the first sense, the most common
        synset = synsets[0]

        swn_synset = swn.senti_synset(synset.name())
        if swn_synset.pos_score() < swn_synset.neg_score():
            return -1 * swn_synset.neg_score()
        elif swn_synset.pos_score() > swn_synset.neg_score():
            return swn_synset.pos_score()
        else:
            return 0


print(SentiWordNet.get_sentiment(""))
