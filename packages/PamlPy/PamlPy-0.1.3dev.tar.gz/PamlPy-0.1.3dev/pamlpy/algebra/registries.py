
class Functions:
	# Variables
	known_functions=	[];
	
	@staticmethod
	def add_function(func):
		"""Adds a function to the list of known functions"""
		Functions.known_functions.append(func);
	#add_function
#Functions

__all__=	["Functions"];