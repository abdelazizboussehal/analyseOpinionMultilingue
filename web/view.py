import numpy
from flask import Flask, render_template, jsonify
from library import tools as t, analyse_models
from library import generation_modeles
from flask import request
from flask_cors import CORS

app = Flask(__name__)
l = ""

CORS(app)


@app.route('/json/')
def index_two():
    return jsonify(username="g.user.username",
                   email="g.user.email",
                   id="g.user.id")


@app.route('/')
def index():
    return render_template('index.html')


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


if __name__ == "__main__":
    app.run(debug=True)
