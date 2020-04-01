from operator import itemgetter
import spacy

nlp = spacy.load("fr_core_news_sm")


class GenerationModels:

    def process(self, content):
        """ Le processus du traitement """
        blob = nlp(content)
        tags = []
        for word in blob:

            if (not word.is_stop or word.dep_ == "dobj" or word.pos_ == "PRON") and word.is_alpha:
                text = word.text
                type_pos = word.pos_
                type_dep = word.dep_
                label = "none"
                if word.pos_ == "PROPN":
                    doc2 = nlp(str(word.text))
                    for ent in doc2.ents:
                        label = ent.label_
                    element = (type_pos, type_dep, text, label)
                else:
                    element = (type_pos, type_dep, text, label)
                tags.append(element)

        model = self.build_model(tags)
        return model

    def build_model(self, tags):
        """
            Prendre les POS-tags-deps-lebels comme paramètre et trouver le modèle correspondant puis le générer
        """

        code_model = self.get_model(tags)  # quel modèle on va choisir
        subject = ''
        adjectif = ''
        root = ''
        model = "none"
        if 1 == code_model:
            for tag in tags:
                if tag[1] == 'ROOT':
                    root = tag[2]
                elif tag[1] == 'nsubj':
                    subject = tag[2]
                elif tag[0] == "ADJ":
                    adjectif = tag[2]

            model = self.build_model_one(subject, root, adjectif)
        elif 2 == code_model:
            for tag in tags:
                if tag[1] == 'nsubj':
                    subject = tag[2]
                elif tag[0] == "ADJ":
                    adjectif = tag[2]
            model = self.build_model_two(subject, adjectif)

        return model

    def get_model(self, tags):
        """ Trouver le modèle correspondant à partir des POS-tag disponible """
        code_dep = list(map(itemgetter(1), tags))
        code_pos = list(map(itemgetter(0), tags))

        if "ROOT" in code_dep and "nsubj" in code_dep and "ADJ" in code_pos:
            return 1
        elif "nsubj" in code_dep and "ADJ" in code_pos:
            return 2
        else:
            return -1  # unknown

    def models_parts(self):
        """ Les éléments nécessaires pour chaque modèle """
        models = {
            "1": ["NN", "JJ"],
            "2": [],
            "3": [],
            "4": [],
            "n": "..."
        }
        return models

    def list_models(self):
        """ Les modèles disponibles pour but d'affichage (Utilser une BDD pour les stocker par la suite) """
        models = {
            "1": "Subject <- opinion",
            "2": "Subject <- opinion(aspect)",
            "3": "Subject <- opinion(aspect)@time",
            "4": "Subject <- opinion(aspect)@time?holder",
            "n": "..."
        }
        return models

    def build_model_one(self, subject, root, adjectif):
        """ Construction du premier modèle """
        return subject + " <- " + root + " ( " + adjectif + " )"

    def build_model_two(self, subject, adjectif):
        """ Construction du deuxième modèle """
        return subject + " ( " + adjectif + " ) "
