class GenerationModels():

	def process(self):


	def list_models(self):
		models = {
			"1": "Subject <- opinion(aspect)",
			"2": "Subject <- opinion(aspect)@time",
			"3": "Subject <- opinion(aspect)@time?holder",
			"n": "..."
		}
		return models

	def model_one(self, subject, opinion, aspect):
		return subject + "<-"  + opinion + "(" + aspect + ")"

