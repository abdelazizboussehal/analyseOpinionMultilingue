from textblob import TextBlob
from os import path as os_path
from CreationModele import CreationModele
from AnalyseModeles import AnalyseModeles
""" module creation """
cr = CreationModele()
cr.lecture()
cr.preTraitement()
cr.creationModele()
""" module analyse """
analyse = AnalyseModeles("Python")
analyse.lectureModee()
analyse.filtrage()
print(analyse.analyse())

