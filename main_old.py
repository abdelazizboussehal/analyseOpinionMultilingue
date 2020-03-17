# -*- coding: utf-8 -*-
"""
	Proposition d’un pivot interlangue (Ar-Fr-Ang) pour la traduction automatique afin d’aider à l’analyse d’opinion
	@group: Abdelaziz boussehal, Abderraouf Mahmoudi
	@date: 2019-2020
"""

from CreationModele import CreationModele
from CreationModele_fr import CreationModele_fr
from CreationModele_fr import CreationModele_fr
from AnalyseModeles import AnalyseModeles
"""
	cr_fr = CreationModeles_ar()
	cr_fr.lecture("test_ar.txt")
	cr_fr.preTraitement()
	cr_fr.creationModele()
"""
cr_fr = CreationModele_fr()
cr_fr.lecture("test_fr.txt")
cr_fr.preTraitement()
cr_fr.creationModele()

""" module creation 
cr = CreationModele()
cr.lecture("test_en.txt")
cr.preTraitement()
cr.creationModele()
"""
""" module analyse 
analyse = AnalyseModeles("Python")
analyse.lectureModee()
analyse.filtrage()
print(analyse.analyse())
"""


