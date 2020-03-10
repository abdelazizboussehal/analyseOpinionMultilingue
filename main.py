'''
Proposition d’un pivot interlangue (Ar-Fr-Ang) pour la traduction automatique afin d’aider à l’analyse d’opinion
@group: Abdelaziz boussehal, Abderraouf Mahmoudi
@date: 2019-2020
'''

from textblob import TextBlob
from os import path as os_path
from CreationModele import CreationModele
from AnalyseModeles import AnalyseModeles


""" module creation """
cr = CreationModele()
cr.lecture("text.txt")
cr.preTraitement()
cr.creationModele()

""" module analyse """
analyse = AnalyseModeles("Python")
analyse.lectureModee()
analyse.filtrage()
print(analyse.analyse())

