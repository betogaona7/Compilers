
# PRACTICE 6:

# Read a file and indentify integer constants, real and string 
# Use the method of matrix states as well as the generation of tokens

# Open a file in read mode
fichero = open("file6", "r")

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
constant = ""
variable = ""

def analysis(character):

	global r
	global typee
	global constant
	global variable
	
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
						 [26, "<" ], # LT
						 [27, ">" ], # GT
						 [28, "<="], # LE
						 [29, ">="], # GE
						 [30, "=="], # EQ
						 [31, "<>"], # NE
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

	if (code == 34):
		column = 1
		typee = 16
	elif (code == 46):
		column = 2
		typee = 41          
	elif (code >= 48 and code <= 57):
		column = 3
	elif (code == 32):
		column = 4
		typee = 41
	else:
		column = 5
		typee = 41

	value = states[r][column]
	r = value
	#print "r and value = ", r
	#print " valor que llego ", character, "\n" 
	flag = False
#-----------------------------------------------------------------------------------------------------------------------
	if (r > 1 and r < 5):
		if (variable != ''):
			r = 1
		else:
			constant += character
			#print "constant: ", constant
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
			constant.replace('"','')
		token = [typee, line, 0, constant]
		tokens.append(token)
		r = 1
		constant = ""

		if (character != string):
			if(character == ' '):
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
				token = [typee, line, 0, constant]
				tokens.append(token)
#--------------------------------------------------------------------------------------------------------------------------
	if (r == 1000 or (r == 1 and variable != "")):
		if ((code >= 65 and code <= 90) or (code >= 97 and code <= 122)): 
			variable += character

			#print "it's letra ", variable
		else:
			is_reserved_word = False
			cont = 0
			for word in reserved_words:
				if (reserved_words[cont][1] == variable):
					is_reserved_word = True
					typee = reserved_words[cont][0]
				if (is_reserved_word == True):
					break
				cont += 1

			if (is_reserved_word == True):
				token = [typee, line, 0, variable]
				tokens.append(token)
			elif ((is_reserved_word == False) and ((variable == "") == False)):
				direction = 1;
				alfaNumVar = "42" + variable
				for var in variables_table:
					aux = var.replace(',','')
					if (aux == alfaNumVar):
						flag = True
						break
					direction += 1
				if (flag == True):
					flag = False
				else:
					variables_table.append("70," + variable)

			if (character != ' '):
				cont = 0
				for operator in special_operators:
					if (special_operators[cont][1] == character):
						typee = special_operators[cont][0]
						flag = True
					if (flag == True):
						flag = False
						break
				token = [typee, line, 0, character]
				tokens.append(token)
			variable = ""
			typee = 0
		r = 1
#-----------------------------------------------------------------------------------------------------------------------
	if (r == 0):
		#print "Error, caracter no valido"
		r = 1
#-----------------------------------------------------------------------------------------------------------------------




#variables_table.append("0,0")

while True:
	letra = fichero.read(1)
	if (letra == '\n'):
		line += 1
	elif not letra:
		break
	if (letra  != '\n'):
		#print "character: ", letra, " line: ", lines
		analysis(letra.upper())


for token in tokens:
	print token

print "\n"

for variable in variables_table:
	print variable

fichero.close()




