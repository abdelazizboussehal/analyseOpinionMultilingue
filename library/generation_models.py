from textblob import TextBlob
from operator import itemgetter

class GenerationModels():

	def process(self, content):
		""" Le processus du traitement """
		blob = TextBlob(content)
		tags = blob.tags
		model = self.build_model(tags)
		return model


	def build_model(self, tags):
		""" Prendre les POS-tags comme paramètre et trouver le modèle correspondant puis le générer.
		"""
		code_tags = list(map(itemgetter(1), tags)) # Gader les tags seulement
		code_model = self.get_model(code_tags) # quel modèle on va choisir
		subject = ''
		opinion = ''

		if 1 == code_model:
			for tag in tags:
				if tag[1] == 'NN':
					subject = tag[0]
				elif tag[1] == 'JJ':
					opinion = tag[0]

			model = self.build_model_one(subject, opinion)
			return model


	def get_model(self, tags):
		""" Trouver le modèle correspondant à partir des POS-tag disponible.
		Args:
			tags: array
		Returns:
			int, number id of the model
		"""
		if 'NN' in tags and 'JJ' in tags:
			return 1
		else:
			return -1 # unknown


	def models_parts(self):
		""" Les éléments nécessaires pour chaque modèle. """
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
			"1": "Subject <- opinion",
			"2": "Subject <- opinion(aspect)",
			"3": "Subject <- opinion(aspect)@time",
			"4": "Subject <- opinion(aspect)@time?holder",
			"n": "..."
		}
		return models


	def build_model_one(self, subject, opinion):
		""" Construction du premier modèle.
		Args:
			subject: String, the subject
			opinion: String, the opinion
		Returns:
			String of model
		"""
		return subject + " <- "  + opinion


	def build_model_two(self, subject, opinion, aspect):
		""" Construction du deuxième modèle.
		Args:
			subject: String, the subject
			opinion: String, the opinion
			aspect: String, the aspect
		Returns:
			String of model
		"""
		return subject + " <- "  + opinion + "(" + aspect + ")"

