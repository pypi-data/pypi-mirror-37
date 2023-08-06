
from decimal import Decimal;
import math as Math;

class Set:
	def __init__(self, name, term, condition, known_subsets=[]):
		"""Initiates the set"""
		self.name=	name;
		self.term=	term;
		self.condition=	condition;
		self.known_subsets=	known_subsets;
	#__init__
	
	# --- Methods ---
	
	def is_in(self, obj):
		"""Finds if the given object is within the set"""
		return self.condition(self.term(obj));
	#is_in
	
	def is_subset(self, _set):
		"""Finds if the given set is a subset of this set"""
		if(self.name in _set.known_subsets):
			return True;
		# TODO: Need to figure out how to test if this set is a subset of the given set
		return False;
	#is_subset
#Set

### N
Set.N=	Set(
	name="N",
	term=(lambda n: Decimal(n)),
	condition=(lambda n: (n>= 0 and Math.floor(n)))
);
### Z
Set.Z=	Set(
	name="Z",
	term=(lambda n: Decimal(n)),
	condition=(lambda n: (Math.floor(n)== 0)),
	known_subsets=["N"]
);
### Q
def _q_cond(n):
	# Variables
	num=	n-Math.floor(n);
	if(num== 0.0):
		return True;
	a=	str(num);
	a=	10**len(a[a.index(".")+1:]);
	if(a>= 10**10):
		return False;
	return (Set.Z.is_in(n*a) and Set.Z.is_in(a));
#_q_cond
Set.Q=	Set(
	name="Q",
	term=(lambda n: Decimal(n)),
	condition=_q_cond,
	known_subsets=["N", "Z"]
);
### R
Set.R=	Set(
	name="R",
	term=(lambda n: Decimal(n)),
	condition=(lambda n: True),
	known_subsets=["N", "Q", "Z"]
);

class SetBuilder:
	def __init__(self, s):
		self.set_ascii=	s;
	#__init__
	
	# --- Methods ---
	
	def get_term(self):
		"""Gets the built term"""
		return (lambda n: n);
	#get_term
	
	def get_condition(self):
		"""Gets the built condition"""
		return (lambda n: True);
	#get_condition
#SetBuilder

__all__= ["Set"];