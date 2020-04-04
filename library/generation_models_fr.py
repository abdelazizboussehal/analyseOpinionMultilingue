from operator import itemgetter
import spacy

nlp = spacy.load("fr_core_news_sm")


class GenerationModels:

    def process(self, content):
        """ Le processus du traitement """
        blob = nlp(content)
        tags = []
        for word in blob:

            if (not word.is_stop or word.dep_ == "dobj" or word.pos_ == "PRON") and (
                    word.is_alpha or word.pos_ == "PRON"):
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
        opinion = []
        model = "none"
        verb = []
        holder = ''
        propn = []
        time = []

        if 1 == code_model:
            for tag in tags:
                if "nous" == str.lower(tag[2]) or "je" == str.lower(tag[2]) or "j'" == str.lower(tag[2]):
                    subject = tag[2]
                    holder = tag[2]
                elif 'nsubj' in tag[1]:
                    subject = tag[2]
                elif "dobj" in tag[1] or "pobj" in tag[1] or "iobj" in tag[1] or "ob" in tag[1]:
                    subject = tag[2]
                elif tag[0] == "ADJ":
                    opinion.append(tag[2])
                if "LOC" in tag[3] or "ORG" in tag[3] or "GPE" in tag[3] or "PERSON" in tag[3] or "PRODUCT" in tag[3]:
                    propn.append(tag[2] + " : " + tag[3])
                if "DATE" in tag[3]:
                    time.append(tag[2])

            model = self.build_model_one(subject, opinion, holder, propn, time)
        elif 2 == code_model:
            for tag in tags:
                if 'nsubj' in tag[1]:
                    subject = tag[2]
                elif "dobj" in tag[1] or "pobj" in tag[1] or "iobj" in tag[1] or "ob" in tag[1]:
                    subject = tag[2]
                elif tag[1] == 'ROOT':
                    verb.append(tag[2] + " * ")
                elif tag[0] == "VERB":
                    verb.append(tag[2])
                elif tag[0] == "ADJ":
                    opinion.append(tag[2])
                if "LOC" in tag[3] or "ORG" in tag[3] or "GPE" in tag[3] or "PERSON" in tag[3] or "PRODUCT" in tag[3]:
                    propn.append(tag[2] + " : " + tag[3])

            model = self.build_model_two(subject, verb, opinion, propn, time)
        elif 3 == code_model:
            for tag in tags:
                if "nous" == str.lower(tag[2]) or "je" == str.lower(tag[2]) or "j'" == str.lower(tag[2]):
                    subject = tag[2]
                    holder = tag[2]
                elif 'nsubj' in tag[1]:
                    subject = tag[2]
                elif "dobj" in tag[1] or "pobj" in tag[1] or "iobj" in tag[1] or "ob" in tag[1]:
                    subject = tag[2]
                elif tag[1] == 'ROOT':
                    verb.append(tag[2] + " * ")
                elif tag[0] == "VERB":
                    verb.append(tag[2])
                elif tag[0] == "ADJ":
                    opinion.append(tag[2])
                if "LOC" in tag[3] or "ORG" in tag[3] or "GPE" in tag[3] or "PERSON" in tag[3] or "PRODUCT" in tag[3]:
                    propn.append(tag[2] + " : " + tag[3])
                if "DATE" == tag[3]:
                    time.append(tag[2])
            model = self.build_model_three(subject, verb, opinion, holder, propn, time)
        elif 4 == code_model:
            for tag in tags:
                if 'nsubj' in tag[1]:
                    subject = tag[2]
                elif "dobj" in tag[1] or "pobj" in tag[1] or "iobj" in tag[1] or "ob" in tag[1]:
                    subject = tag[2]
                elif tag[1] == 'ROOT':
                    verb.append(tag[2] + " * ")
                elif tag[0] == "VERB":
                    verb.append(tag[2])
                elif tag[0] == "ADJ":
                    opinion.append(tag[2])
                if "LOC" in tag[3] or "ORG" in tag[3] or "GPE" in tag[3] or "PERSON" in tag[3] or "PRODUCT" in tag[3]:
                    propn.append(tag[2] + " : " + tag[3])
                if "DATE" in tag[3]:
                    time.append(tag[2])
            model = self.build_model_four(subject, verb, opinion, propn, time)
        elif 5 == code_model:
            for tag in tags:
                if "nsubj" in tag[1]:
                    subject = tag[2]
                elif "ob" in tag[1]:
                    subject = tag[2]
                elif tag[0] == "ADJ":
                    opinion.append(tag[2])
                if "LOC" in tag[3] or "ORG" in tag[3] or "GPE" in tag[3] or "PERSON" in tag[3] or "PRODUCT" in tag[3]:
                    propn.append(tag[2] + " : " + tag[3])
                if "DATE" in tag[3]:
                    time.append(tag[2])
            model = self.build_model_five(subject, opinion, propn, time)
        elif 7 == code_model:
            for tag in tags:
                if "nsubj" in tag[1]:
                    subject = tag[2]
                elif "dobj" in tag[1] or "pobj" in tag[1] or "iobj" in tag[1] or "ob" in tag[1]:
                    subject = tag[2]
                elif tag[1] == 'ROOT':
                    verb.append(tag[2] + " * ")
                elif tag[0] == "VERB":
                    verb.append(tag[2])
                if "LOC" in tag[3] or "ORG" in tag[3] or "GPE" in tag[3] or "PERSON" in tag[3] or "PRODUCT" in tag[3]:
                    propn.append(tag[2] + " : " + tag[3])
                if "DATE" in tag[3]:
                    time.append(tag[2])
            model = self.build_model_seven(subject, verb, propn, time)
        elif 6 == code_model:
            for tag in tags:
                if "nous" == str.lower(tag[2]) or "je" == str.lower(tag[2]) or "j'" == str.lower(tag[2]):
                    subject = tag[2]
                    holder = tag[2]
                elif "nsubj" in tag[1]:
                    subject = tag[2]
                elif "dobj" in tag[1] or "pobj" in tag[1] or "iobj" in tag[1] or "ob" in tag[1]:
                    subject = tag[2]
                elif tag[1] == 'ROOT':
                    verb.append(tag[2] + " * ")
                elif tag[0] == "VERB":
                    verb.append(tag[2])
                if "LOC" in tag[3] or "ORG" in tag[3] or "GPE" in tag[3] or "PERSON" in tag[3] or "PRODUCT" in tag[3]:
                    propn.append(tag[2] + " : " + tag[3])
                if "DATE" in tag[3]:
                    time.append(tag[2])
            model = self.build_model_six(subject, verb, holder, propn, time)

        return model, code_model

    def get_model(self, tags):
        """ Trouver le modèle correspondant à partir des POS-tag disponible """
        code_dep = list(map(itemgetter(1), tags))
        code_pos = list(map(itemgetter(0), tags))
        code_leb = list(map(itemgetter(3), tags))
        text = list(map(itemgetter(2), tags))

        sujet = 0
        verb = 0
        opinion = 0
        time = 0
        propn = 0
        holder = 0
        for t in text:
            if "je" == str.lower(str(t)) or "nous" == str.lower(str(t)) or "j'" == str.lower(str(t)):
                holder = 1

        if "dobj" in code_dep or "pobj" in code_dep or "iobj" in code_dep or "obj" in code_dep or "obl" in code_dep:
            sujet = 1
        else:
            for s in code_dep:
                if s.startswith("nsubj"):
                    sujet = 1

        if "VERB" in code_pos:
            verb = 1

        if "ADJ" in code_pos:
            opinion = 1

        if sujet == 1 and opinion == 1 and verb == 1 and holder == 1:
            return 3
        elif sujet == 1 and opinion == 1 and verb == 1:
            return 4
        elif sujet == 1 and opinion == 1:
            return 5
        elif sujet == 1 and opinion == 1 and holder == 1:
            return 1
        elif sujet == 1 and verb == 1 and holder == 1:
            return 6
        elif sujet == 1 and verb == 1:
            return 7
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
            1: "Subject <- (opinion&&opinion)@holder ",
            3: "Subject <- // root*&&verb // (opinion&&opinion) @ holder",
            4: "Subject <- // root*&&verb // (opinion&&opinion) ",
            5: "Subject <- (opinion&&opinion) ",
            6: "Subject <- // root*&&verb //  @ holder",
            7: "Subject <- // root*&&verb //",

            -1: "..."
        }
        return models

    def build_model_one(self, subject, opinion, holder, propn, time):
        """ Construction du premier modèle """
        model = ""
        model = model + subject + " <- " + " ( "

        for i in range(0, len(opinion) - 1):
            model = model + opinion[i] + " && "
        model = model + opinion[len(opinion) - 1] + " ) @ " + holder
        if len(time) > 0:
            model = model + " ? "
            for i in range(len(time) - 1):
                model = model + time[i] + " && "
            model = model + time[len(time) - 1]

        if len(propn) > 0:
            model = model + " [ "
            for i in range(len(propn) - 1):
                model = model + propn[i] + " && "
            model = model + propn[len(propn) - 1] + " ] "

        return model

    def build_model_two(self, subject, verb, opinion, propn):
        """ Construction du deuxième modèle """
        model = ""
        model = model + subject + " <- " + " // "
        for i in range(len(verb) - 1):
            model = model + verb[i] + " && "
        model = model + verb[len(verb) - 1] + " // ("
        for i in range(0, len(opinion) - 1):
            model = model + opinion[i] + " && "
        model = model + opinion[len(opinion) - 1] + " ) " + " [ "
        for i in range(len(propn) - 1):
            model = model + propn[i] + " && "
        model = model + propn[len(propn) - 1] + " ] "

        return model

    def build_model_three(self, subject, verb, opinion, holder, propn, time):
        """ Construction du premier modèle """
        model = ""
        model = model + subject + " <- " + " // "
        for i in range(len(verb) - 1):
            model = model + verb[i] + " && "
        model = model + verb[len(verb) - 1] + " // ("
        for i in range(0, len(opinion) - 1):
            model = model + opinion[i] + " && "
        model = model + opinion[len(opinion) - 1] + " ) @ " + holder
        if len(time) > 0:
            model = model + " ? "
            for i in range(len(time) - 1):
                model = model + time[i] + " && "
            model = model + time[len(time) - 1]

        if len(propn) > 0:
            model = model + " [ "
            for i in range(len(propn) - 1):
                model = model + propn[i] + " && "
            model = model + propn[len(propn) - 1] + " ] "
        return model

    def build_model_four(self, subject, verb, opinion, propn, time):
        """ Construction du premier modèle """
        model = ""
        model = model + subject + " <- " + " // "
        for i in range(len(verb) - 1):
            model = model + verb[i] + " && "
        model = model + verb[len(verb) - 1] + " // ("
        for i in range(0, len(opinion) - 1):
            model = model + opinion[i] + " && "
        model = model + opinion[len(opinion) - 1] + " ) "
        if len(time) > 0:
            model = model + " ? "
            for i in range(len(time) - 1):
                model = model + time[i] + " && "
            model = model + time[len(time) - 1]

        if len(propn) > 0:
            model = model + " [ "
            for i in range(len(propn) - 1):
                model = model + propn[i] + " && "
            model = model + propn[len(propn) - 1] + " ] "
        return model

    def build_model_five(self, subject, opinion, propn, time):
        """ Construction du premier modèle """
        model = ""
        model = model + subject + " <- ("
        for i in range(0, len(opinion) - 1):
            model = model + opinion[i] + " && "
        model = model + opinion[len(opinion) - 1] + " ) "
        if len(time) > 0:
            model = model + " ? "
            for i in range(len(time) - 1):
                model = model + time[i] + " && "
            model = model + time[len(time) - 1]

        if len(propn) > 0:
            model = model + " [ "
            for i in range(len(propn) - 1):
                model = model + propn[i] + " && "
            model = model + propn[len(propn) - 1] + " ] "
        return model

    def build_model_six(self, subject, verb, holder, propn, time):
        """ Construction du premier modèle """
        model = ""
        model = model + subject + " <- " + " // "
        for i in range(len(verb) - 1):
            model = model + verb[i] + " && "
        model = model + verb[len(verb) - 1] + " // @ " + holder
        if len(time) > 0:
            model = model + " ? "
            for i in range(len(time) - 1):
                model = model + time[i] + " && "
            model = model + time[len(time) - 1]

        if len(propn) > 0:
            model = model + " [ "
            for i in range(len(propn) - 1):
                model = model + propn[i] + " && "
            model = model + propn[len(propn) - 1] + " ] "
        return model

    def build_model_seven(self, subject, verb, propn, time):
        """ Construction du premier modèle """
        model = ""
        model = model + subject + " <- " + " // "
        for i in range(len(verb) - 1):
            model = model + verb[i] + " && "
        model = model + verb[len(verb) - 1] + " //"
        if len(time) > 0:
            model = model + " ? "
            for i in range(len(time) - 1):
                model = model + time[i] + " && "
            model = model + time[len(time) - 1]

        if len(propn) > 0:
            model = model + " [ "
            for i in range(len(propn) - 1):
                model = model + propn[i] + " && "
            model = model + propn[len(propn) - 1] + " ] "
        return model
