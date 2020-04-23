from flask import Flask, render_template
from library import tools as t
from library import generation_models_en as en
from library import generation_models_fr as fr
from flask import request

app = Flask(__name__)
l = ""


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
        error.append("" + str(t.Tools.correction_orthographe(str(ph), language)))

    return render_template('correction.html', language=lang, phrases=phrases, erreurs=error)


@app.route('/creationModeles', methods=['POST'])
def creation_modeles():
    all_sentences = []
    subjective_state = []
    subjective_sentences = []
    print(request.form)
    global l
    for x in request.form:
        if "r_id" in x:
            all_sentences.append(request.form[x])
        else:
            subjective_state.append(request.form[x])
    for i in range(len(all_sentences)):
        if subjective_state[i] == "true":
            subjective_sentences.append(all_sentences[i])
    print(subjective_sentences)
    # Instanciation du module Génération des modèles
    models = []
    types = []
    if l == "fr":
        generator = fr.GenerationModels()
        # Lancer le processuss de traitement
        for ph in subjective_sentences:
            num = generator.process(str(ph))[1]
            m = generator.process(str(ph))[0]
            types.append(generator.list_models().get(num))
            print(types)
            models.append(m)
    elif l == "en":
        generator = en.GenerationModels()
        # Lancer le processuss de traitement
        for ph in subjective_sentences:
            num = generator.process(str(ph))[1]
            m = generator.process(str(ph))[0]
            types.append(generator.list_models().get(num))
            print(types)
            models.append(m)
    elif l == "ar":
        models = "arabic"
    else:
        models = "langues non definite"

    return render_template('resultat.html', language=l, modeles=models, phrases=subjective_sentences, types=types)


@app.route('/SubjectivityFiltering', methods=['POST'])
def subjectivity_filtering():
    subjective_state = []
    sentences = []
    global l
    for x in request.form:
        sentences.append(request.form[x])
    subjective_state = t.Tools.subjectivity_filtering(sentences, l)[1]

    return render_template('sentencesSubjective.html', subjective_state=subjective_state, sentences=sentences)


if __name__ == "__main__":
    app.run(debug=True)
