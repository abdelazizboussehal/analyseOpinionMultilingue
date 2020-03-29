# -*- coding: utf-8 -*-
"""
	Proposition d’un pivot interlangue (Ar-Fr-Ang) pour la traduction automatique afin d’aider à l’analyse d’opinion
	@group: Abdelaziz boussehal, Abderraouf Mahmoudi
	@date: 2019-2020
"""

from library import generation_models_fr as g
from library import tools as t

if __name__ == "__main__":
    # Lecture du fichier
    content = t.Tools.read("./data/test_fr.txt")

    # Instanciation du module Génération des modèles
    generator = g.GenerationModels()

    # Lancer le processuss de traitement
    model = generator.process(content)

    # Affichage dans la console
    print("\n")
    print("- Contenu du fichier : ", content)
    print("- Modèle généré : ", model)

    # Sauvegarder le modèle dans un fichier
    t.Tools.write(model)
