

class DataBase(object):
	"""docstring for DataBase"""
	def __init__(self):
		self.auth_dict = {"123456789": [1,2,4]}
		
	def validate(self, list_knock , _pass):
		return (_pass in self.auth_dict.keys() and self.validate_knock(self.auth_dict[_pass], list_knock ) ) 
	

	def create(self, list_knock , _pass):
		if not (_pass in self.auth_dict.keys()):
			self.auth_dict[ _pass ] = list_knock
		return

	def validate_knock(self, k_stored , k1):
		return True
		