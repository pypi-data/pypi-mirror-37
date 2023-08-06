import pandas as pd
import numpy as np
import datetime
from sklearn.externals import joblib


def __init__(self):
		''' Constructor for this class. '''
		
# сохранение модели
def save_model(model, name, path = ""):
	version = datetime.datetime.now().strftime('%Y-%m-%d')
	all_data = dict({"name": name,
					 "model": model,
					 "version": version})
	file = path + name + ".pkl"
	
	try:
		joblib.dump(all_data, file)
		print("Model %s is successfully saved in %s" % (name, file))
	except Exception as e:
		print("Error during saving: " + str(e))

# загрузка модели
def load_model(file):
	try:
		model = joblib.load(file)
		if not isinstance(model, dict):
			print("Model is not a dictionary instance")
			return model
		else:
			if model.get("version") is None or model.get("model") is None or model.get("name") is None:
				raise Exception("Error! Wrong format of the model dictionary!")
			
			version = model["version"]
			name = model["name"]
			print("Model %s with version %s is successfully loaded from %s" % (name, version, file))
			return model["model"]
	except Exception as e:
		print("Error during loading: " + str(e))

