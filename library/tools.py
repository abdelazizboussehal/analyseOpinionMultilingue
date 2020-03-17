

class Tools():


	@staticmethod
	def read(path):
		f = open(path, "r")
		content = f.read()
		f.close()
		return content


	@staticmethod
	def write(content, name="models", extension="txt", folder="generated"):
		f = open(folder + "/" + name + "." + extension,"w")
		for line in content:
			f.write(line)
		f.close()