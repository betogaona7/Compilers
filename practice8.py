
# PRACTICE 8:

# Use a file, and manage symbol table for declaration of arrays


# Open a file in read mode
fichero = open("file6", "r")

import sys

def isInteger(string):
	try:
		int(string)
		return True
	except ValueError:
		return False

def isFloat(string):
	try:
		float(string)
		return True
	except ValueError:
		return False


tokens = []
variables_table = []

index = 0
line = 1
r = 1
typee = 0
type_var = 0


constant = ""
variable = ""
aux_line = ""

declared = False

def analysis(character):

	global r
	global typee
	global constant
	global variable

	global type_var
	global aux_line
	global declared
	
#                    "     .   0-9 space OC
	states = [[0,    0,    0,   0,   0,    0], 
			  [0,    4,    0,   2,   1, 1000], # 1
			  [0,  -50,    3,   2, -50,  -50], # 2
			  [0,  -51,  -51,   3, -51,  -51], # 3
			  [0,  -52,    4,   4,   4,    4]];# 4

	reserved_words = [[ 1, "BEGIN" ],  #General structure
					  [ 2, "MAIN"  ],
					  [ 3, "END"   ],
					  [ 6, "ALFA"  ],  #Type of variables
					  [ 7, "NUM"   ],
					  [ 4, "GET"   ],  #Input/Output
					  [ 5, "SHOW"  ],
					  [10, "IF"    ],  #Control sentences
					  [11, "ELSE"  ],
					  [12, "FOR"   ],
					  [13, "EXIT"  ],
					  [17, "SUB"   ],  #Functions
					  [18, "RETURN"],
					  [19, "GOSUB" ],
					  [25, "#"     ]]; #Comments

	special_operators = [[20, "=" ],
						 [21, "-" ],
						 [22, "+" ],
						 [23, "*" ],
						 [24, "/" ],
						 [26, "LT"], # LT
						 [27, "GT"], # GT
						 [28, "LE"], # LE
						 [29, "GE"], # GE
						 [30, "EQ"], # EQ
						 [31, "NE"], # NE
						 [32, "&" ],
						 [33, "|" ],
						 [34, "!" ],
						 [35, "(" ],
						 [36, ")" ],
						 [37, "{" ],
						 [38, "}" ],
						 [39, ";" ],
						 [40, "," ]];

	column = 0
	value = 0

	code = ord(character)

	if (code == 34): # "
		column = 1
		typee = 16
	elif (code == 46): # .
		column = 2
		typee = 41          
	elif (code >= 48 and code <= 57): # 0 - 9
		column = 3
	elif (code == 32): # ' '
		column = 4
		typee = 41
	else:
		column = 5
		typee = 41

	value = states[r][column]
	r = value
	flag = False
#-----------------------------------------------------------------------------------------------------------------------
	if (r > 1 and r < 5):
		if (variable != ''):
			r = 1
		else:
			constant += character
#-----------------------------------------------------------------------------------------------------------------------
	if (r < 0):
		integer = 0
		double = 0
		string = '"'

		if (isInteger(constant) == True):
			typee = 15
		elif (isFloat(constant) == True): 
			typee = 14
		elif ((constant[0] == string) and (constant == string)):
			typee = 16

		token = [typee, line, 0, constant.replace('"','')]
		tokens.append(token)
		r = 1
		constant = ""

		if (character != string):
			if(character != ' '): 
				cont = 0
				for operator in special_operators:
					if (special_operators[cont][1] == character):
						typee = special_operators[cont][0]
						flag = True
					else:
						typee = 42
					if (flag == True):
						flag = False
						break
					cont += 1
				token = [typee, line, 0, character]
				tokens.append(token)
#--------------------------------------------------------------------------------------------------------------------------
	if (r == 1000 or (r == 1 and variable != "")):
		if ((code >= 65 and code <= 90) or (code >= 97 and code <= 122)): # If the character is a letter
			variable += character
		else:
			is_reserved_word = False
			array = False 
			cont = 0

			for word in reserved_words:
				if (reserved_words[cont][1] == variable):
					is_reserved_word = True
					typee = reserved_words[cont][0]
				if (is_reserved_word == True):
					break
				cont += 1

			if (is_reserved_word == True):
				if(typee == 6 or typee == 7 or typee == 17 or typee == 19):
					if(typee == 6):
						type_var = 8
					elif (typee == 7):
						type_var = 9
					elif (typee == 17):
						type_var = 43
					else:
						type_var = 44

					#type_var = typee - 20
					declared = True
				else:
					type_var = 0
					declared = False

				token = [typee, line, 0, variable]
				tokens.append(token)


			elif ((is_reserved_word == False) and ((variable == "") == False)):
				if(variable != "LT" and variable != "GT" and variable != "EQ" and variable != "LE" and variable != "GE" and variable != "NE"):
					direction = 1
					for var in variables_table:
						
						temp = str(var).split(' ')
						if(temp[2] == variable):
							flag = True
							token = [temp[0], line, direction, variable] #CHANGE
							tokens.append(token)
						direction += 1

					if(flag == False):
						dimensions = 0
						left = 0
						right = 0

						if (character == ','):
							dimensions = 0
							left = 0
							right = 0
						elif (character == '('):

							data = aux_line[(index + 1):(aux_line.index(')', index) - index - 1)]
							temp = []
							array = True

							if(data.find(',') != -1): 
								temp = data.split(',')
								dimensions = 2
								left = temp[0]
								right = temp[1]
							else:
								dimensions = 1
								left = data

							index = aux_line.index(')', index)

						flag = False 
						#PENDIENTE
						var = [type_var, variable, dimensions, left, right, declared]
						token = [type_var, line, direction, variable]
						tokens.append(token)
						variables_table.append(var)

				else:
					cont = 0
					for var in variables_table:
						if(variable == variables_table[cont][1]):
							typee = variables_table[cont][0]
							flag = True
						if(flag == True):
							flag = False
							break
						cont += 1

					token = [typee, line, 0, variable]
					tokens.append(token)
					variable = ""
			if (character != ' ' and array == False): #HERE
				cont = 0
				for operator in special_operators:
					if (special_operators[cont][1] == character):
						typee = special_operators[cont][0]
						flag = True
					if (flag == True):
						flag = False
						break
					cont += 1
				token = [typee, line, 0, character]
				tokens.append(token)

			if (character != ',' and character != ' ' and character != '(' and character != ')'):
				type_var = 0
				declared = False

			variable = ""
			typee = 0
		r = 1
#-----------------------------------------------------------------------------------------------------------------------
	if (r == 0):
		print "Error, caracter no valido"
		r = 1
#-----------------------------------------------------------------------------------------------------------------------




while True:
	letra = fichero.read(1)
	if (letra == '\n'):
		line += 1
	elif not letra:
		break
	if (letra  != '\n'):
		analysis(letra.upper())


for token in tokens:
	print token

print "\n"


for variable in variables_table:
	print variable

fichero.close()




