class Calculator(object):

	"""
	Usage:
	
	# initialize a standard calculator:
	# (optional parameters "rule" & "regularization")
	standard = Calculator()

	# check object.rule for priority and behaviours of each operator respectively
	# you can modify it
	print(standard.rule)

	# calculating
	# algebra supported
	print(standard.calculate('1 + 2 * 3'))
	print(standard.calculate('a + b * c' ,a=1 ,b=2 ,c=3))
	"""
	
	def __init__(self, rule = None, regularization = None):
		super(Calculator, self).__init__()

		self.args = {}
		self.rules = rule if rule != None else { '+' : (0 ,lambda x,y:x+y) ,
												'-' : (0 ,lambda x,y:x-y) ,
												'*' : (1 ,lambda x,y:x*y) ,
												'/' : (1 ,lambda x,y:x/y) , 
												'^' : (2 ,lambda x,y:x**y) }
		self.regularization = regularization[0] if regularization != None else lambda x:x.replace("**","^").replace('\\','/')
		try:
			opets ,prios ,funcs = [],[],[]
			for item in self.rules.items():
				opets.append(item[0])
				prios.append(item[1][0])
				funcs.append(item[1][1])
			self.priority_map = dict(tuple(zip(opets,prios)))
			self.behaviours = dict(tuple(zip(opets,funcs)))
			self.priority_map.update({'(':-1,')':-1})
		except Exception as e:
			raise TypeError(f"initialize process supports dictionary type input refering label set & operation set. ErrorMessage: {e}")

	def mid2post(self,expr): 

		# validity check
		if not type(expr) is str:
			raise TypeError("only support string input")

		# regularization
		expr = self.regularization(expr.replace(" ","")+")") 

		# initialization
		# use none empty stack to avoid list empty check
		# use double linked list as a simulation of pointer
		stack ,register ,output = ['('] ,[[]] ,[]

		# move those data from register into output
		def update_register(register = register):
			tmp ,register[0]= ''.join(register[0]) ,[]
			output.append(tmp) if tmp != '' else None

		# pop until 'n' priority
		# make sure elements in stack was strict arange from low priority to high one
		# '(' element could be regard as a lowest priority element 
		def pop_stack(n):
			update_register()
			while stack:
				output.append(stack.pop())
				if output[-1] == '(' or self.priority_map[stack[-1]] < n:
					break

		for char in expr:
			# deal with '(' and ')'
			# due to those two refers to different operation respectively
			# could not simply classify them as same priority operator
			if char == '(':
				stack.append('(')
			elif char == ')':
				pop_stack(-1)
			# if character is operator and not '(' or ')'
			# thus there's two possible operation:
			# push it dirctively into stack\ or pop stack and push new elements
			elif char in self.priority_map.keys():
				if self.priority_map[stack[-1]] == -1:
					stack.append(char)
					update_register()
				elif self.priority_map[char] > self.priority_map[stack[-1]]:
					stack.append(char)
					update_register()
				else:
					pop_stack(self.priority_map[char])
					stack.append(char)
			# if character is none operator,stor it into register 
			else:
				register[0].append(char)
		# finally pop all elements from stack
		else: 
			pop_stack(-1)

		return output

	# post process deal with output stack
	# convert numbers to numbers / remove '('
	# replace algebra into numbers
	def post_process(self,elem):
		try:
			return eval(elem)
		except:
			return self.args[elem] if elem in self.args.keys() else elem if elem != '(' else None

	def calculate_postexp(self,postexp):

		# initialization
		stack = []

		# table driven
		for elem in postexp:
			if elem in self.priority_map.keys():
				op_b ,op_a = stack.pop() , stack.pop()
				stack.append(self.behaviours[elem](op_a,op_b))
			else:
				stack.append(elem)

		return stack[0]

	def calculate(self,exp,**args):

		# if you input exp as nothing
		# it will simply update arguments
		# self.args = iargs
		self.args.update(args)
		if exp == '':
			return 'arguments was updated'

		# post processing
		post_exp = list(map(self.post_process,self.mid2post(exp)))
		while None in post_exp:
			post_exp.remove(None)

		# invalidity check
		for elem in post_exp:
			if not str(elem).replace('.','').isdigit() and elem not in self.behaviours.keys():
				raise Warning(f'invalid element found : could not identify "{elem}" ,check your expression again.')
		
		# calculate
		return self.calculate_postexp(post_exp)

if __name__ == '__main__':
	pass
