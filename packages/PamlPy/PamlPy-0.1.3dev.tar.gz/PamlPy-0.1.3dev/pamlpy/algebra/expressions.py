
import math as Math;
import operator;
from .registries import Functions;

class Expression:
	def __init__(self, text="", parenth=False):
		"""
		Constructs the expression.
		text:(str)	The input of the expression
		parenth:(bool)	True if this expression is enclosed by parenthesis
		"""
		self.text=	str(text);
		self.is_parenthesis=	bool(parenth);
		# TODO: Add ExpressionParamters. That way we can catch the ',' issue
		#self.parameters=	[ExpressionParameter()];
		self.buckets=	[];
		if(self.text!= ""):
			self.build();
	#__init__
	
	def build(self):
		"""
		Builds the expression
		"""
		# Variables
		scope=	0;
		bucket=	"+";
		neg_flag=	False;
		
		for c in self.text:
			# Once we hit the delimiters (+ and -) and our scope is in it's outter most scope
			# TODO: Push to parameters
			#if(scope== 0 and c== ','):
			#	self.push_parameter();
			if(scope== 0 and (c== '+' or c== '-')):
				# This one is if the character is a negative sign but the current bucket doesn't
				# have a negative sign then make it negative. Continues because we do not want
				# any empty buckets
				# i.e. pos * neg = neg
				if(bucket== "+"):
					if(c== "-"):
						bucket=	"-";
					continue;
				# This one is if the character is a negative sign but the current bucket has a
				# negative sign then make it positive. Continues because we do not want any empty
				# buckets
				# i.e. neg * neg = pos
				if(bucket== "-"):
					if(c== "-"):
						bucket=	"+";
					continue;
				# Adds the finished bucket without adding that sign
				self._add_bucket(bucket);
				# Append the sign to the next bucket
				bucket=	c;
				continue;
			# Here is a scoping trick. If we found a parenthesis then the scope> 0
			if(c== '('):
				scope+=	1;
			# Then if we found the closing parenthesis then the scope>= 0
			elif(c== ')'):
				scope-=	1;
			# Appends the current character to the bucket
			bucket+=	c;
		# If the scope is not 0, then they did not close up the parenthesis
		if(scope> 0):
			print("Equation is not completed");
		# Adds the finished bucket
		self._add_bucket(bucket);
	#build
	
	def _add_bucket(self, bucket):
		"""
		Adds the given bucket into the expression's buckets.
		bucket:(str)	A string that represents a segment of the expression. x^2+4x => +x^2 is a bucket and +4x is another bucket but x^2+4x is not a bucket
		"""
		self.buckets.append(ExpressionBucket(bucket));
		pass;
	#add_bucket
	
	def __str__(self):
		"""Returns the expression in string form"""
		# TODO: Make the expression look cleaner
		bk=	"','".join([str(b) for b in self.buckets]);
		bk=	"['"+bk+"']";
		return (
			"Ascii: "+self.text+"\n"+
			"Buckets: "+bk
		);
	#__str__
#Expression

"""
class ExpressionParameter:
	pass;
#ExpressionParameter
"""

"""
################
################

Expression Bucket

################
################
"""

class ExpressionBucket:
	# Variables
	SPLIT_FLAG_NONE=	0;
	SPLIT_FLAG_EXPRESSION=	1;
	SPLIT_FLAG_FUNCTION=	2;
	SPLIT_FLAG_VARIABLE=	3;
	SPLIT_FLAG_NUMBER=	4;
	SPLIT_FLAG_CONSTANT=	5;
	SPLIT_FLAG_EXPONENT=	6;
	SPLIT_FLAG_DIVISION=	7;
	
	@staticmethod
	def is_nan(obj):
		"""Finds if the given object is not a number"""
		try:
			return Math.isnan(float(obj));
		except:
			return True;
	#is_nan
	
	@staticmethod
	def _append_node(nodes, text, flag):
		"""Appends the given node into the list of nodes"""
		if(text== ""):
			return;
		if(flag== ExpressionBucket.SPLIT_FLAG_FUNCTION):
			pass;
		elif(flag== ExpressionBucket.SPLIT_FLAG_VARIABLE):
			for func in Functions.known_functions:
				# Variables
				f=	str(func["name"]);
				if(f in text):
					# Variables
					i=	text.index(f);
					j=	i+len(f);
					
					ExpressionBucket._append_node(nodes, text[:i], flag);
					ExpressionBucket._append_node(nodes, text[i:j], ExpressionBucket.SPLIT_FLAG_FUNCTION);
					ExpressionBucket._append_node(nodes, text[j:], flag);
					return;
				#if
			#for
		#else if variable
		nodes.append((flag, text));
	#_append_node
	
	def __init__(self, bucket=""):
		self.text=	str(bucket[1:]);
		self.is_positive=	True;
		if(bucket[0]== '+' or bucket[0]== '-'):
			self.is_positive=	(bucket[0]== '+');
		self.numerator=	[];
		self.denominator=	[ExpressionNode(num=1)];
		self._build();
	#__init__
	
	def _build(self):
		"""Builds the bucket"""
		self._split();
		self._merge_to_nodes();
		self._sort_and_combine(self.numerator);
		self._sort_and_combine(self.denominator);
		# TODO: Simplify common numerator and denominator
	#_build
	
	def _split(self):
		"""Splits up the text into it's respective nodes"""
		# Variables
		txt=	"";
		scope=	0;
		flag=	ExpressionBucket.SPLIT_FLAG_NONE;
		nodes=	[];
		varflag=	False;
		
		# FIXME: sinx^2 is broken
		# FIXME: sin(x)^2 is broken in a different way
		# TODO: Detect d{func}/d{wrt} and turn it into its own derivative node
		
		for c in self.text:
			if(varflag and flag== ExpressionBucket.SPLIT_FLAG_NUMBER):
				flag=	ExpressionBucket.SPLIT_FLAG_VARIABLE;
			if(scope== 0):
				if((not ExpressionBucket.is_nan(c) or c== '.') and not varflag):
					if(flag!= ExpressionBucket.SPLIT_FLAG_NUMBER):
						ExpressionBucket._append_node(nodes, txt, flag);
						txt=	"";
					flag=	ExpressionBucket.SPLIT_FLAG_NUMBER;
					txt+=	c;
				elif(c== '('):
					varflag=	False;
					ExpressionBucket._append_node(nodes, txt, flag);
					txt=	c;
					scope+=	1;
					flag=	ExpressionBucket.SPLIT_FLAG_EXPRESSION;
				elif(c== '*' or c== ' '):
					varflag=	False;
					ExpressionBucket._append_node(nodes, txt, flag);
					txt=	"";
					flag=	ExpressionBucket.SPLIT_FLAG_NONE;
				elif(c== '^'):
					varflag=	False;
					ExpressionBucket._append_node(nodes, txt, flag);
					txt=	c;
					flag=	ExpressionBucket.SPLIT_FLAG_EXPONENT;
				elif(c== '/'):
					varflag=	False;
					ExpressionBucket._append_node(nodes, txt, flag);
					txt=	c;
					flag=	ExpressionBucket.SPLIT_FLAG_DIVISION;
				else:
					if(flag!= ExpressionBucket.SPLIT_FLAG_VARIABLE):
						varflag=	False;
						ExpressionBucket._append_node(nodes, txt, flag);
						txt=	"";
					varflag=	True;
					txt+=	c;
					flag=	ExpressionBucket.SPLIT_FLAG_VARIABLE;
			#if scope
			else:
				txt+=	c;
				if(c== '('):
					scope+=	1;
				elif(c== ')'):
					scope-=	1;
					if(scope== 0):
						ExpressionBucket._append_node(nodes, txt, flag);
						txt=	"";
				#elif
			#else scope
		#for
		ExpressionBucket._append_node(nodes, txt, flag);
		self.numerator+=	nodes;
	#_split

	def _merge_to_nodes(self):
		# Variables
		temp=	[];
		temp_d=	[];
		ix=	iter(range(len(self.numerator)));
		
		for i in ix:
			flag=	self.numerator[i][0];
			if(flag== ExpressionBucket.SPLIT_FLAG_FUNCTION):
				temp.append(ExpressionNode(
					op="#",
					left=self._popnode(i),
					right=self._popnode(i+1)
				));
				next(ix);
			elif(flag== ExpressionBucket.SPLIT_FLAG_EXPONENT):
				temp.append(ExpressionNode(
					op="^",
					left=self._popnode(i-1),
					right=self._popnode(i+1)
				));
				del temp[len(temp)-2];
				next(ix);
			elif(flag== ExpressionBucket.SPLIT_FLAG_DIVISION):
				temp_d.append(self._popnode(i+1));
				next(ix);
			else:
				temp.append(self._popnode(i));
		del self.numerator[:];
		self.numerator+=	temp;
		if(len(temp_d)> 0):
			del self.denominator[:];
			self.denominator+=	temp_d;
	#_merge_to_nodes
	
	def _popnode(self, i):
		"""Pops out the node at index i"""
		if(self.numerator[i][0]== ExpressionBucket.SPLIT_FLAG_NUMBER):
			return ExpressionNode(num=self.numerator[i][1]);
		return ExpressionNode(str_=self.numerator[i][1]);
	#_popnode
	
	def _sort_and_combine(self, nodes= []):
		"""Sorts and combines the nodes in the list"""
		for i in range(1, len(nodes)):
			self._insertion_sort(nodes, i);
		# TODO: Figure out how to combine x x x => x^3
		# TODO: Figure out how to combine x y x x => y x^3
		for i in range(len(nodes)-1, 0, -1):
			if(nodes[i-1].is_similar(nodes[i])):
				if(self._combine(nodes, i-1, i)):
					return;
	#_sort_and_combine
	
	def _combine(self, nodes, a, b):
		"""Combines the two elements from the list of nodes together"""
		if(nodes[a].is_number()):
			nodes[a].data*=	nodes[b].data;
			del nodes[b];
		if(nodes[a].is_variable() and nodes[a].data== nodes[b].data):
			nodes[a]=	ExpressionNode(op='^', left=nodes[a], right=ExpressionNode(num=2));
			del nodes[b];
			self._sort_and_combine(nodes);
			return True;
		if(nodes[a].is_exponent() and nodes[a].left.data== nodes[b].left.data):
			nodes[a]=	ExpressionNode(
				op='^',
				left= nodes[a].left,
				right=ExpressionNode(str_="("+str(nodes[a].right)+" + "+str(nodes[b].right)+")")
			);
			del nodes[b];
			self._sort_and_combine(nodes);
			return True;
		return False
	#_combine
	
	def _insertion_sort(self, nodes=[], i=2):
		# Variables
		n=	0;
		
		for i in range(i, 0, -1):
			n=	nodes[i-1].sort_id()-nodes[i].sort_id();
			if(n> 0):
				self._swap(nodes, i-1, i);
			elif(n== 0):
				if(nodes[i-1].sub_sort_id(nodes[i])> 0):
					self._swap(nodes, i-1, i);
				else:
					return;
			else:
				return;
	#_insertion_sort
	
	def _swap(self, nodes, a, b):
		"""Swaps the nodes between the two given indices"""
		nodes[a], nodes[b]=	nodes[b], nodes[a];
	#_swap
	
	# --- Inherited Methods ---
	
	def __str__(self):
		"""Returns the expression bucket in string form"""
		# TODO: Display the bucket in a much cleaner way
		return (str([str(n) for n in self.numerator])+"\n"+
			str([str(d) for d in self.denominator]));
	#__str__
#ExpressionBucket


"""
################
################

Expression Node

################
################
"""

class ExpressionNode:
	# Variables
	DATA_TYPE_UNKNOWN=	-1;
	DATA_TYPE_NUMBER=	0;
	DATA_TYPE_CONSTANT=	1;
	DATA_TYPE_VARIABLE=	2;
	DATA_TYPE_EXPONENT=	3;
	DATA_TYPE_FUNCTION=	4;
	DATA_TYPE_EXPRESSION=	5;
	
	@staticmethod
	def _strdata(node):
		return str(node.data);
	#_strdata
	
	def __init__(self, *args, **kwargs):
		self.left=	None;
		self.right=	None;
		self.data=	"";
		self.data_type=	ExpressionNode.DATA_TYPE_UNKNOWN;
		if(kwargs.get("num")):
			self.data=	float(kwargs.get("num"));
			self.data_type=	ExpressionNode.DATA_TYPE_NUMBER;
			return;
		if(kwargs.get("const")):
			self.data=	str(kwargs.get("const"));
			self.data_type=	ExpressionNode.DATA_TYPE_CONSTANT;
			return;
		if(kwargs.get("var")):
			self.data=	str(kwargs.get("var"));
			self.data_type=	ExpressionNode.DATA_TYPE_VARIABLE;
			return;
		if(kwargs.get("exp")):
			self.data=	"^";
			self.data_type=	ExpressionNode.DATA_TYPE_EXPONENT;
			self.left=	kwargs.get("left");
			self.right=	kwargs.get("right");
			return;
		if(kwargs.get("func")):
			self.data=	"#";
			self.data_type=	ExpressionNode.DATA_TYPE_FUNCTION;
			self.left=	kwargs.get("left");
			self.right=	kwargs.get("right");
			return;
		if(kwargs.get("expr")):
			self.data=	Expression(kwargs.get("expr")[1:-2], True);
			self.data_type=	ExpressionNode.DATA_TYPE_EXPRESSION;
			return;
		if(kwargs.get("op")):
			self.data=	kwargs.get("op");
			self.left=	kwargs.get("left");
			self.right=	kwargs.get("right");
			if(self.data== "^"):
				self.data_type=	ExpressionNode.DATA_TYPE_EXPONENT;
			elif(self.data== "#"):
				self.data_type=	ExpressionNode.DATA_TYPE_FUNCTION;
			return;
		if(kwargs.get("str_")):
			self.data=	kwargs.get("str_");
			self.data_type=	ExpressionNode.DATA_TYPE_VARIABLE;
			if(self.data[0]== '(' and self.data[-1]== ')'):
				self.data=	Expression(kwargs.get("str_")[1:-1], True);
				self.data_type=	ExpressionNode.DATA_TYPE_EXPRESSION;
			return;
		#if
	#__init__
	
	def is_empty(self):
		"""Finds if the node is empty. Empty as in left and right are not traversable"""
		return (self.left== self.right== None);
	#is_empty
	
	def is_number(self):
		"""Finds if the node is just a number (coefficient)"""
		return (self.data_type== ExpressionNode.DATA_TYPE_NUMBER);
	#is_number
	
	def is_constant(self):
		"""Finds if the node is just a constant"""
		return (self.data_type== ExpressionNode.DATA_TYPE_CONSTANT);
	#is_constant
	
	def is_variable(self):
		"""Finds if the node is just a variable"""
		return (self.data_type== ExpressionNode.DATA_TYPE_VARIABLE);
	#is_variable
	
	def is_exponent(self):
		"""Finds if the node is just an exponent"""
		return (self.data_type== ExpressionNode.DATA_TYPE_EXPONENT);
	#is_exponent
	
	def is_function(self):
		"""Finds if the node is just a function"""
		return (self.data_type== ExpressionNode.DATA_TYPE_FUNCTION);
	#is_function
	
	def is_expression(self):
		"""Finds if the node is just an expression"""
		return (self.data_type== ExpressionNode.DATA_TYPE_EXPRESSION);
	#is_expression
	
	def is_similar(self, other):
		"""Finds if the node is similar to the other node"""
		if(self.data_type== other.data_type):
			return True;
		return False;
	#is_similar
	
	def sort_id(self):
		"""Gets the sorting id from the node"""
		if(self.is_number()):
			return 0;
		if(self.is_constant()):
			return 1;
		if(self.is_variable()):
			return 2;
		if(self.is_exponent()):
			return 3;
		if(self.is_function()):
			return 4;
		if(self.is_expression()):
			return 5;
		return 6;
	#sort_id
	
	def sub_sort_id(self, other):
		"""Gets the sorting id between two nodes that are the same"""
		if(self.is_number()):
			return (self.data-other.data);
		if(self.is_exponent() or self.is_function()):
			# Variables
			lsort=	(0 if sorted([self.left, other.left], key=ExpressionNode._strdata)== [self.left, other.left] else 1);
			rsort=	(0 if sorted([self.right, other.right], key=ExpressionNode._strdata)== [self.right, other.right] else 1);
			
			# If x==x. Ignoring x< y
			if(lsort== 0 and str(self.left)== str(other.left)):
				return rsort;
			return lsort;
		if(sorted([self, other], key=ExpressionNode._strdata)== [self, other]):
			return 0;
		return 1;
	#sub_sort_id
	
	def build(self):
		"""Builds out the node. Returns a string containing the full node"""
		if(self.is_empty()):
			return str(self.data);
		# Variables
		s=	"";
		
		if(self.left!= None):
			s+=	" "+self.left.build()+" ";
		if(not self.is_function()):
			s+=	str(self.data);
		if(self.right!= None):
			s+=	" "+self.right.build()+" ";
		return s.strip();
	#build
	
	# --- Methods ---
	
	def __str__(self):
		"""Returns the expression node in string form"""
		return self.build();
	#__str__
#ExpressionNode

__all__=	["Expression"];