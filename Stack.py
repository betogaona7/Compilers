#Stack

class Stack:

	def __init__(self):
		#Create a new stack
		self.items = []

	def Push(self, x):
		#Add a new element
		self.items.append(x)

	def Pop(self):
		#Return the last element and delete this element
		try:
			return self.items.pop()
		except IndexError:
			raise ValueError("The stack is empty")

	def is_empty(self):
		#return true if the stack is empty, False if it's not
		return self.items == []

	def length(self):
		return len(self.items)