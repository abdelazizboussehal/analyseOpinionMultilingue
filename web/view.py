from flask import Flask, render_template
from library import tools as t
from library import generation_models_en as en
from library import generation_models_fr as fr
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/modeles', methods=['POST'])
def modeles():
    content = request.form['input']
    print(content)
    dt = t.Tools.languageDetection(content)
    if dt == "en":
        langue = "anglais"
        # Segmentation de text par phrase
        phrasee = t.Tools.segmentationParPhrase(content, dt)
        phrase = []
        for ph in phrasee:
            phrase.append(str(ph))
    elif dt == "fr":
        langue = "français"
        # Segmentation de text par phrase
        phrasee = t.Tools.segmentationParPhrase(content, dt)
        phrase = []
        for ph in phrasee:
            phrase.append(str(ph))
    elif dt == "ar":
        langue = "arabic"
    else:
        langue = "autre langue"

    # Instanciation du module Génération des modèles
    model = []
    types = []
    if dt == "fr":
        generator = fr.GenerationModels()
        # Lancer le processuss de traitement
        for ph in phrase:
            m = generator.process(str(ph))
            model.append(m)

    elif dt == "en":
        generator = en.GenerationModels()
        # Lancer le processuss de traitement
        for ph in phrase:
            num = generator.process(str(ph))[1]
            m = generator.process(str(ph))[0]
            types.append(generator.list_models().get(num))
            print(types)
            model.append(m)
    elif dt == "ar":
        model = "arabic"
    else:
        model = "langues non definite"

    return render_template('resultat.html', language=langue, modeles=model, phrases=phrase, types=types)


if __name__ == "__main__":
    app.run()
