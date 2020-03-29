from operator import itemgetter
import spacy

nlp = spacy.load("fr_core_news_sm")


class GenerationModels:

    def process(self, content):
        """ Le processus du traitement """
        blob = nlp(content)
        tags = []
        for token in blob:
            tags.append((token.text, token.pos_))
        print(tags)
        model = self.build_model(tags)
        return model

    def build_model(self, tags):
        """
            Prendre les POS-tags comme paramètre et trouver le modèle correspondant puis le générer
        """
        code_tags = list(map(itemgetter(1), tags))  # Gader les tags seulement
        code_model = self.get_model(code_tags)  # quel modèle on va choisir
        subject = ''
        opinion = ''

        if 1 == code_model:
            for tag in tags:
                if tag[1] == 'NOUN':
                    subject = tag[0]
                elif tag[1] == 'ADJ':
                    opinion = tag[0]

            model = self.build_model_one(subject, opinion)
            return model

    def get_model(self, tags):
        """ Trouver le modèle correspondant à partir des POS-tag disponible """
        if 'NOUN' in tags and 'ADJ' in tags:
            return 1
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

    def build_model_one(self, subject, opinion):
        """ Construction du premier modèle """
        return subject + " <- " + opinion

    def build_model_two(self, subject, opinion, aspect):
        """ Construction du deuxième modèle """
        return subject + " <- " + opinion + "(" + aspect + ")"
