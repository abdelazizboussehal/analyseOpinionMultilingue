import os
import secrets

import numpy
from flask import Flask, render_template, session
from flask import request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from library import gerenration_modele_optimized as gmo
from library import tools as t, analyse_models

secret = secrets.token_urlsafe(32)
app = Flask(__name__)
app.secret_key = secret

CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


def correction(content):
    global l
    language = t.Tools.language_detection(content)
    list_word = []
    list_suggestion = []
    session['l'] = language
    sub_sentence = []
    if language == "en":
        lang = "anglais"
    elif language == "fr":
        lang = "français"
    elif language == "ar":
        lang = "arabe"
    list_word.append(t.Tools.correction_orthographe(str(content), language)[0])
    list_suggestion.append(t.Tools.correction_orthographe(str(content), language)[1])
    return lang, list_word, list_suggestion


def subjectivity(sub_sentence, sub_sentence_subjectivity, l):
    # nbr phrase sub
    nbr_sub = 0
    nbr_obj = 0
    for x in sub_sentence_subjectivity:
        if x:
            nbr_sub += 1
        else:
            nbr_obj += 1

    # creation des modeles
    subjective_sentences = []
    # tableux des sous models
    verbs = []
    adjs = []
    nouns = []
    connectors = []
    # tableau segment linguistique
    tab_s_l_v = []
    tab_s_l_a = []
    tab_s_l_n = []

    # tableau segment linguistique
    tab_u_l_v = []
    tab_u_l_a = []
    # tableaux negation connecteur modificateur
    negationv_total = []
    negationv_chaque_phrase = []
    negationa_total = []
    negationa_chaque_phrase = []
    generation_model_optimized = ""
    modificateura_total = []
    modificateura_chaque_phrase = []
    modificateurv_total = []
    modificateurv_chaque_phrase = []

    total_adverbe = []
    total_negation = []

    tableaux_vis_dep = []
    tableaux_vis_ent = []

    stat_verb = []
    stat_nom = []
    stat_adj = []
    stat_total = 0
    stat_aux = []
    stat_propre_noun = []
    stat_adv = []

    model_global = []
    for i in range(len(sub_sentence)):
        if sub_sentence_subjectivity[i]:
            if l == "en":
                generation_model_optimized = gmo.GenerationModels(sub_sentence[i])
            elif l == "fr":
                generation_model_optimized = gmo.GenerationFrenchModels(sub_sentence[i])
            generation_model_optimized.create_model()
            subjective_sentences.append(sub_sentence[i])
            verbs.append(generation_model_optimized.modele_segement_linguistique_verbe)
            adjs.append(generation_model_optimized.modele_segement_linguistique_adjectif)
            nouns.append(generation_model_optimized.modele_segement_linguistique_nom)
            connectors.extend(generation_model_optimized.connectors)
            stat_verb.extend(generation_model_optimized.verbC)
            stat_adj.extend(generation_model_optimized.adjectifC)
            stat_nom.extend(generation_model_optimized.nounC)
            stat_aux.extend(generation_model_optimized.auxC)
            stat_propre_noun.extend(generation_model_optimized.propnC)
            stat_adv.extend(generation_model_optimized.adverbC)
            model_global.append(generation_model_optimized.modele_globale)
            tableaux_vis_dep.append(generation_model_optimized.vis_dep)
            tableaux_vis_ent.append(generation_model_optimized.vis_ent)
            stat_total = stat_total + generation_model_optimized.total

            tab_s_l_a.append(generation_model_optimized.modele_segement_linguistique_adjectif)
            tab_s_l_v.append(generation_model_optimized.modele_segement_linguistique_verbe)
            tab_s_l_n.append(generation_model_optimized.modele_segement_linguistique_nom)

            tab_u_l_a.extend(generation_model_optimized.table_m_u_l_a)
            tab_u_l_v.extend(generation_model_optimized.table_m_u_l_v)

            negationv_total.extend(generation_model_optimized.negation_verb)
            negationv_chaque_phrase.append(generation_model_optimized.negation_verb)

            negationa_total.extend(generation_model_optimized.negation_adj)
            negationa_chaque_phrase.append(generation_model_optimized.negation_adj)

            modificateura_total.extend(generation_model_optimized.modificateur_adj)
            modificateura_chaque_phrase.append(generation_model_optimized.modificateur_adj)

            modificateurv_total.extend(generation_model_optimized.modificateur_verb)
            modificateurv_chaque_phrase.append(generation_model_optimized.modificateur_verb)

    session['stat_verb'] = stat_verb
    session['stat_adj'] = stat_adj
    session['stat_nom'] = stat_nom
    session['stat_total'] = stat_total
    session['stat_aux'] = stat_aux
    session['stat_propre_noun'] = stat_propre_noun
    session['total_adverbe'] = stat_adv
    session['stat_other'] = stat_total - len(stat_verb) - len(stat_adj) - len(stat_nom) - len(
        stat_aux) - len(stat_adv) - len(stat_propre_noun)
    total_negation.extend(negationa_total)
    total_negation.extend(negationv_total)

    total_adverbe.extend(modificateura_total)
    total_adverbe.extend(modificateurv_total)
    session['tab_s_l_n'] = tab_s_l_n
    session['tab_s_l_v'] = tab_s_l_v
    session['tab_s_l_a'] = tab_s_l_a
    session['tab_u_l_v'] = tab_u_l_v
    session['tab_u_l_a'] = tab_u_l_a
    session['visualizer_dep'] = tableaux_vis_dep
    session['visualizer_ent'] = tableaux_vis_ent
    session['total_connectors'] = connectors
    session['total_adverbe'] = generation_model_optimized.adverbC

    return ("phrase", sub_sentence, sub_sentence_subjectivity, nbr_sub, nbr_obj, total_adverbe, total_negation,
            "", subjective_sentences, verbs, adjs, nouns, model_global)


@app.route('/res', methods=['POST'])
def res():
    billet = 0  # le point de reprendre le processus
    content = ""
    if request.form['id_reprocess'] == 'id_text':  # Acquisition depuis la zone de saisie
        content = request.form['input']

    elif request.form['id_reprocess'] == 'id_file':  # Acquisition depuis une fichier
        file = request.files['file_text']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(filename))
            content = open(os.path.join(filename), 'r').read().replace("\n", " ")
    elif request.form['id_reprocess'] == 'twitter':  # Acquisition depuis twitter
        twitters = t.Tools.get_twit_from_twitter(request.form.get("subject"), 6)
        languages = ["ar", "en", "fr"]
        for twit in twitters:
            if twit[2] in languages:
                x = 0
    elif request.form['id_reprocess'] == 'form_correction':  # retraitement correction
        content = request.form['content']
    elif request.form['id_reprocess'] == 'form_subjectivity':  # retraitement subjectivité
        billet = 1
        sub_sentence = []
        sub_sentence_subjectivity = []
        for x in request.form:
            x = str(x)
            if x.startswith("r_id"):
                sub_sentence.append(request.form[x])
            if x.startswith("optradio"):
                if request.form[x] == "true":
                    sub_sentence_subjectivity.append(True)
                else:
                    sub_sentence_subjectivity.append(False)

    if billet < 1:
        session['content'] = content
        correction_var = correction(content)
        session['language'] = correction_var[0]

        list_word = correction_var[1]
        list_suggestion = correction_var[2]
        session['list_word'] = list_word
        session['list_suggestion'] = list_suggestion
        # segemntation phrase
        phrase = t.Tools.sentence_segmentation(content, session['l'])
        session['phrase'] = phrase

        # segmentation sous phrase
        sub_sentence = []
        for ph in phrase:
            sub_sentence.extend(t.Tools.segmentation_with_connectors(str(ph), session['l']))
            # subjectivite
            sub_sentence_subjectivity = t.Tools.subjectivity_filtering(sub_sentence, session['l'])[1]
    if billet < 2:

        # reprocess subjectivity
        subjectivity_var = subjectivity(sub_sentence, sub_sentence_subjectivity, session['l'])
        session['sub_sentence'] = subjectivity_var[1]
        session['subjective_state'] = subjectivity_var[2]
        session['nbr_sub'] = subjectivity_var[3]
        session['nbr_obj'] = subjectivity_var[4]
        session['total_negation'] = subjectivity_var[6]
        session['subjective_sentences'] = subjectivity_var[8]
        session['verbs'] = subjectivity_var[9]
        session['adjs'] = subjectivity_var[10]
        session['nouns'] = subjectivity_var[11]
        session['model_global'] = subjectivity_var[12]

        tableaux_dic_model_global = []
        tableaux_plarity_global_sentence = []
        tableaux_emoji_global_sentence = []

        for model_glob in session['model_global']:
            # module analyse
            if session['l'] == "en":
                analyse_model = analyse_models.AnalyseModels(session['l'], model_glob)
            elif session['l'] == "fr":
                analyse_model = analyse_models.AnalyseFrenchModels(session['l'], model_glob)
            analyse_model.extract_sub_models()
            analyse_model.get_polarity_sub_model_verb()
            analyse_model.get_polarity_sub_model_adjective()
            analyse_model.get_polarity_sub_model_noun()
            analyse_model.extract_element_model_global()
            tableaux_dic_model_global.append(analyse_model.dictionnaire_model_global)
            tableaux_plarity_global_sentence.append(analyse_model.polarity_model())
            tableaux_emoji_global_sentence.append(t.Tools.get_emoji_from_polarity(analyse_model.polarity_model()))

        session['dictionnaire_model_global'] = tableaux_dic_model_global
        session['polarity_global'] = numpy.array(tableaux_plarity_global_sentence).mean()
        session['emoji_global'] = t.Tools.get_emoji_from_polarity(session['polarity_global'])
        session['polarity_sentences'] = tableaux_plarity_global_sentence
        session['emoji_sentences'] = tableaux_emoji_global_sentence

    return render_template('resultatfinal.html')


if __name__ == "__main__":
    app.run(debug=True)
