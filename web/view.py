import os
import secrets

import numpy
from flask import Flask, render_template, jsonify, session
from flask import request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from library import generation_modeles
from library import tools as t, analyse_models

secret = secrets.token_urlsafe(32)
app = Flask(__name__)
app.secret_key = secret

CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/a')
def indexa():
    return render_template('index1.html')


@app.route('/preTreatment', methods=['POST'])
def pretreatment():
    content = request.form['input']
    language = t.Tools.language_detection(content)
    phrase = t.Tools.sentence_segmentation(content, language)
    error = []
    phrases = []
    list_word = []
    list_suggestion = []
    global l
    l = language
    if language == "en":
        lang = "anglais"
    elif language == "fr":
        lang = "français"
    elif language == "ar":
        lang = "arabe"

    for ph in phrase:
        phrases.append(ph)
        list_word.append(t.Tools.correction_orthographe(str(ph), language)[0])
        list_suggestion.append(t.Tools.correction_orthographe(str(ph), language)[1])

    return render_template('correction.html', language=lang, phrases=phrases, list_word=list_word,
                           list_suggestion=list_suggestion)


@app.route('/SubjectivityFiltering', methods=['POST'])
def subjectivity_filtering():
    subjective_state = []
    sentences = []
    global l
    for x in request.form:
        sentences.append(request.form[x])
    subjective_state = t.Tools.subjectivity_filtering(sentences, l)[1]

    return render_template('sentencesSubjective.html', subjective_state=subjective_state, sentences=sentences)


@app.route('/ExtractAdjVrb', methods=['POST'])
def extract_adj_verb():
    global l
    all_sentences = []
    subjective_state = []
    subjective_sentences = []
    verbs = []
    adjs = []
    nouns = []
    array_model_verb = []
    emoji_verb = []
    array_polarity_verb = []
    array_model_adjective = []
    emoji_adjective = []
    array_polarity_adjective = []
    connectors = []

    for x in request.form:
        if "r_id" in x:  # pour recuperer sentence
            all_sentences.append(request.form[x])
        else:
            subjective_state.append(request.form[x])  # pour recuperer valeur de radio
    for i in range(len(all_sentences)):
        if subjective_state[i] == "true":
            if l == "en":
                generation_model = generation_modeles.GenerationModels(all_sentences[i])
            elif l == "fr":
                generation_model = generation_modeles.GenerationFrenchModels(all_sentences[i])
            generation_model.create_model()
            subjective_sentences.append(all_sentences[i])
            verbs.append(generation_model.sub_model_verb)
            adjs.append(generation_model.sub_model_adjective)
            nouns.append(generation_model.sub_model_noun)
            connectors.append(generation_model.connector)

            if l == "en":
                analyse_model = analyse_models.AnalyseModels(l, generation_model.model_general)
            elif l == "fr":
                analyse_model = analyse_models.AnalyseFrenchModels(l, generation_model.model_general)
            analyse_model.extract_sub_models()
            analyse_model.get_polarity_sub_model_verb()
            analyse_model.get_polarity_sub_model_adjective()
            analyse_model.get_polarity_sub_model_noun()
            # traitemnt verbe
            array_polarity_verb.append(analyse_model.polarity_sub_model_verb)
            emoji_verb.append(t.Tools.get_emoji_from_polarity(analyse_model.polarity_sub_model_verb))
            # traitement adjective
            array_polarity_adjective.append(analyse_model.polarity_sub_model_adjective)
            emoji_adjective.append(t.Tools.get_emoji_from_polarity(analyse_model.polarity_sub_model_adjective))

    return render_template('verb_adj.html', sentences=subjective_sentences, verbs=verbs, adjs=adjs, nouns=nouns,
                           emoji_verb=emoji_verb, array_polarity_verbe=array_polarity_verb,
                           emoji_adjective=emoji_adjective, array_polarity_adjective=array_polarity_adjective,
                           language=l, connectors=connectors)


@app.route('/EnterText', methods=['POST'])
def enter_text():
    return render_template('textinput.html')


@app.route('/GetTextFromTwitter', methods=['POST'])
def get_text_from_twitter():
    aziz = request.form.get("subject")
    twitters = t.Tools.get_twit_from_twitter(request.form.get("subject"), 6)
    sentences = []
    errors = []
    languages = ["ar", "en", "fr"]
    for twit in twitters:
        if twit[2] in languages:
            sentences.append(twit[1])
            errors.append("" + str(t.Tools.correction_orthographe(str(twit[1]), twit[2])))

    return render_template('correction.html', language="", phrases=sentences, erreurs=errors)


@app.route('/ConnectorSegmentation', methods=['POST'])
def connector_segmentation():
    global l
    all_sentences = []
    subjective_state = []
    for x in request.form:
        if "r_id" in x:  # pour recuperer sentence
            all_sentences.append(request.form[x])
        else:
            subjective_state.append(request.form[x])  # pour recuperer valeur de radio
    sub_sentence = []
    for i in range(len(all_sentences)):
        if subjective_state[i] == "true":
            sub_sentence.extend(t.Tools.segmentation_with_connectors(all_sentences[i], l))
    sub_sentence_subjectivity = t.Tools.subjectivity_filtering(sub_sentence, l)[1]
    return render_template('sub_sentence_subjectivity.html', sentences=sub_sentence,
                           subjective_state=sub_sentence_subjectivity, language=l)


""" route json"""


@app.route('/json/correction', methods=['POST'])
def json_correction():
    global l
    content = request.form['input']
    language = t.Tools.language_detection(content)
    list_word = []
    list_suggestion = []
    l = language
    if language == "en":
        lang = "anglais"
    elif language == "fr":
        lang = "français"
    elif language == "ar":
        lang = "arabe"

    list_word.append(t.Tools.correction_orthographe(str(content), language)[0])
    list_suggestion.append(t.Tools.correction_orthographe(str(content), language)[1])

    return jsonify(language=lang, content=content, list_word=list_word, list_suggestion=list_suggestion)


@app.route('/json/Segmentation', methods=['POST'])
def json_segmentation():
    global l
    content = request.form['input']
    language = t.Tools.language_detection(content)
    phrase = t.Tools.sentence_segmentation(content, language)
    sub_sentence = []
    for ph in phrase:
        sub_sentence.extend(t.Tools.segmentation_with_connectors(str(ph), l))
    sub_sentence_subjectivity = t.Tools.subjectivity_filtering(sub_sentence, l)[1]

    return jsonify(sentences=sub_sentence, subjective_state=sub_sentence_subjectivity)


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
    # tableaux negation connecteur modificateur
    negationv_total = []
    negationv_chaque_phrase = []
    negationa_total = []
    negationa_chaque_phrase = []

    connectora_total = []
    connectora_chaque_phrase = []
    connectorn_total = []
    connectorn_chaque_phrase = []

    modificateura_total = []
    modificateura_chaque_phrase = []
    modificateurv_total = []
    modificateurv_chaque_phrase = []

    total_connectors = []
    total_adverbe = []
    total_negation = []

    model_global = []
    for i in range(len(sub_sentence)):
        if sub_sentence_subjectivity[i]:
            if l == "en":
                generation_model = generation_modeles.GenerationModels(sub_sentence[i])
            elif l == "fr":
                generation_model = generation_modeles.GenerationFrenchModels(sub_sentence[i])
            generation_model.create_model()
            subjective_sentences.append(sub_sentence[i])
            verbs.append(generation_model.sub_model_verb)
            adjs.append(generation_model.sub_model_adjective)
            nouns.append(generation_model.sub_model_noun)
            connectors.append(generation_model.connector)
            model_global.append(generation_model.model_general)

            negationv_total.extend(generation_model.negation_verb)
            negationv_chaque_phrase.append(generation_model.negation_verb)

            negationa_total.extend(generation_model.negation_adj)
            negationa_chaque_phrase.append(generation_model.negation_adj)

            modificateura_total.extend(generation_model.modificateur_adj)
            modificateura_chaque_phrase.append(generation_model.modificateur_adj)

            modificateurv_total.extend(generation_model.modificateur_verb)
            modificateurv_chaque_phrase.append(generation_model.modificateur_verb)

            connectora_chaque_phrase.append(generation_model.connector_addition_table)
            connectora_total.extend(generation_model.connector_addition_table)

            connectorn_chaque_phrase.append(generation_model.connector_negation_table)
            connectorn_total.extend(generation_model.connector_negation_table)

    total_connectors.extend(connectorn_total)
    total_connectors.extend(connectora_total)

    total_negation.extend(negationa_total)
    total_negation.extend(negationv_total)

    total_adverbe.extend(modificateura_total)
    total_adverbe.extend(modificateurv_total)

    return ("phrase", sub_sentence, sub_sentence_subjectivity, nbr_sub, nbr_obj, total_adverbe, total_negation,
            total_connectors, subjective_sentences, verbs, adjs, nouns, model_global)


@app.route('/res', methods=['POST'])
def res():
    billet = 0
    req = request.form
    content = ""
    if request.form['id_reprocess'] == 'id_text':
        content = request.form['input']
    elif request.form['id_reprocess'] == 'id_file':
        file = request.files['file_text']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(filename))
            content = open(os.path.join(filename), 'r').read().replace("\n", " ")
    elif request.form['id_reprocess'] == 'twitter':
        print("twitter")
    elif request.form['id_reprocess'] == 'form_correction':
        content = request.form['content']
    elif request.form['id_reprocess'] == 'form_subjectivity':
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
        session['total_adverbe'] = subjectivity_var[5]
        session['total_negation'] = subjectivity_var[6]
        session['total_connectors'] = subjectivity_var[7]
        session['subjective_sentences'] = subjectivity_var[8]
        session['verbs'] = subjectivity_var[9]
        session['adjs'] = subjectivity_var[10]
        session['nouns'] = subjectivity_var[11]
        session['model_global'] = subjectivity_var[12]

        # statistic
        t.Tools.statistic(session['content'], session['l'])
        session['stat_verb'] = t.Tools.verbC
        session['stat_adj'] = t.Tools.adjectifC
        session['stat_nom'] = t.Tools.nounC
        session['stat_total'] = t.Tools.total - len(t.Tools.verbC) - len(t.Tools.adjectifC) - len(t.Tools.nounC)
        tableaux_dic_model_global = []
        tableaux_plarity_global_sentence = []
        tableaux_emoji_global_sentence = []
        polarity_global = 0

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
