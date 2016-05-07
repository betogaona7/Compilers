
# PRACTICE 9:

# Use a file, and manage symbol table for declaration of arrays

import sys
from Stack import Stack

# Open a file in read mode
fichero = open("pruebaVCI.txt", "r")

import sys
print '\n'

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


#Compilers part l
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

#Compilers part ll
vicToken = []
pilaIf = Stack()
pilaAux = Stack()
pilaFor = Stack()
pilaBreak = Stack()
beginFor = Stack()
letraFor = Stack()
numeroFor = Stack()
endsub = 0
mainPosition = 0
p = 0
auxP = 0
position = 0
semicolonFor = 0
auxForBreak = 0
mainVariable = None

#State table, reserved words and special characters. 
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
				  [25, "#"     ],
				  [41, "ENDSUB"],
				  [42, "ENDIF" ],
				  [43, "GOTOF" ],
				  [44, "GOTO"  ]]; #Comments

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

prioridades = [["(",  100],
			   ["-u", 90 ],
			   ["*",  80 ],
			   ["/",  80 ],
			   ["+",  70 ],
			   ["-",  70 ],
			   ["LT", 60 ],
			   ["GT", 60 ],
			   ["EQ", 60 ],
			   ["NOT",50 ],
			   ["AND",40 ],
			   ["OR", 30 ],
			   ["=",  20 ],
			   [")",   0 ]];
###########################################################################################################################
def IntermediateCode(s):

	global vicToken 
	global pilaAux
	global pilaIf
	global pilaFor
	global pilaBreak
	global beginFor
	global letraFor
	global numeroFor
	global endsub
	global mainPosition
	global p 
	global auxP 
	global position 
	global semicolonFor 
	global auxForBreak
	global mainVariable 

	global prioridades
	global variables_table

	haveCFS = False
	arrayS = []
	
	for strr in s.split(' '):
		arrayS.append(strr)

	position = len(vciToken);

	if(("SHOW" in arrayS) or  ("GET" in arrayS) or ("EXIT" in arrayS) or ("FOR" in arrayS) or ("IF" in arrayS) or ("ELSE" in arrayS) or ("ENDIF" in arrayS) or ("{" in arrayS) or ("}" in arrayS)):
		haveCFS = True

	if(arrayS[0] == "SUB"):
		endsub = len(vciToken)
		for i in xrange(0, len(variables_table)):
			if (arrayS[1] in variables_table[i]):
				variables_table[i][6] = endsub
				break

	elif(arrayS[0] == "ENDSUB"):
		vciToken.append("<return>")

	elif(arrayS[0] == "MAIN"):
		mainPosition = len(vciToken)
		vciToken[0] = ">> " + str(mainPosition) + " <<"

	elif(arrayS[0] == "GOSUB"):
		for strr in variables_table:
			if(arrayS[1] in strr):
				auxStrSub = strr
				vciToken.append(">> " + str(auxStrSub[len(auxStrSub) - 1]) + " <<")
				vciToken.append("GOSUB")

	elif(arrayS[0] == "END"):
		vciToken.append("END")

	elif(haveCFS == False):
		#logic and arithmetic expressions
		for f in xrange(0, len(arrayS)):
			strAux = str(arrayS[f])
			if(("(" in strAux) or ("-u" in strAux) or ("*" in strAux) or ("/" in strAux) or ("+" in strAux) or ("-" in strAux) or ("LT" in strAux) or ("LE" in strAux) or ("GT" in strAux) or ("EQ" in strAux) or ("NOT" in strAux) or ("AND" in strAux) or ("OR" in strAux) or ("=" in strAux) or (")" in strAux)):
				for i in xrange(0, 14):
					if(prioridades[i][0] in strAux):
						p = prioridades[i][1]
						break

				if(int(pilaAux.length()) == 0):
					pilaAux.Push(strAux)

				elif(p < auxP):
					_n = int(pilaAux.length())
					for n in xrange(0, _n):
						pilaPop1 = pilaAux.Pop()
						if(("(" == pilaPop1) or (")" == pilaPop1) or ("," == pilaPop1)):
							pilaPop1 = ""
						else:
							vciToken.append(pilaPop1)
					pilaAux.Push(strAux)

				else:
					pilaAux.Push(strAux)
				auxP = p
			else:
				if(strAux != ","):
					vciToken.append(strAux)

		_i = int(pilaAux.length())
		for i in xrange(0, _i):
			pilaPop2 = pilaAux.Pop()
			if(("(" == pilaPop2) or (")" == pilaPop2) or ("," == pilaPop2)):
				pilaPop2 = ""
			else:
				vciToken.append(pilaPop2)

	elif(haveCFS == True):
##############################################################################################################################
########################################################## IF ################################################################
		if(arrayS[0] == "IF"):
			#logic and arithmetic expressions
			for f in xrange(1, len(arrayS)):
				strAux = arrayS[f]
				if(("(" in strAux) or ("-u" in strAux) or ("*" in strAux) or ("/" in strAux) or ("+" in strAux) or ("-" in strAux) or ("LT" in strAux) or ("LE" in strAux) or ("GT" in strAux) or ("EQ" in strAux) or ("NOT" in strAux) or ("AND" in strAux) or ("OR" in strAux) or ("=" in strAux) or (")" in strAux)):
					for i in xrange(0, 14):
						if(prioridades[i][0] in strAux):
							p = prioridades[i][1]
							break

					if(int(pilaAux.length()) == 0):
						pilaAux.Push(strAux)

					elif(p < auxP):
						_n = int(pilaAux.length())
						for n in xrange(0, _n):
							pilaPop1 = pilaAux.Pop()
							if(("(" == pilaPop1) or (")" == pilaPop1) or ("," == pilaPop1)):
								pilaPop1 = ""
							else:
								vciToken.append(pilaPop1)
						pilaAux.Push(strAux)
					else:
						pilaAux.Push(strAux)
					auxP = p
				else:
					if(strAux != ","):
						vciToken.append(strAux)

			_i = int(pilaAux.length())
			for i in xrange(0, _i):
				pilaPop2 = pilaAux.Pop()
				if(("(" == pilaPop2) or (")" == pilaPop2) or ("," == pilaPop2)):
					pilaPop2 = ""
				else:
					vciToken.append(pilaPop2)

			vciToken.append(" ")
			pilaIf.Push(len(vciToken))
			vciToken.append("GOTOF")

		elif(arrayS[0] == "ELSE"):
			a = int(pilaIf.Pop())
			b = len(vciToken) + 2
			vciToken[a-1] = ">>" + str(b) + "<<"
			vciToken.append(" ")
			pilaIf.Push(len(vciToken))
			vciToken.append("GOTO")

		elif(arrayS[0] == "ENDIF"):
			a = int(pilaIf.Pop())
			b = len(vciToken)
			vciToken[a-1] = ">>" + str(b) + "<<"
##############################################################################################################################
######################################################### FOR ################################################################
		elif(arrayS[0] == "EXIT"):
			vciToken.append("?")
			pilaBreak.Push(len(vciToken))
			vciToken.append("GOTO")

		elif(arrayS[0] == "FOR"):
			letraFor.Push(arrayS[1])
			#logic and arithmetic expressions
			flag_1 = False
			for f in xrange(1, len(arrayS)):
				mainVariable = arrayS[1]
				strAux = arrayS[f]
				if(";" in strAux):
					_i = int(pilaAux.length())
					for i in xrange(0, _i):
						pilaPop2 = pilaAux.Pop()
						if(("(" == pilaPop2) or (")" == pilaPop2) or ("," == pilaPop2)):
							pilaPop2 = ""
						else:
							vciToken.append(pilaPop2)
					semicolonFor += 1
					if(semicolonFor == 2):
						vciToken.append("LE")
						vciToken.append(" ? ")
						pilaFor.Push(len(vciToken))
						vciToken.append("GOTOF")
						numeroFor.Push(int(arrayS[len(arrayS) -1]))
						semicolonFor = 0
						break
				else:
					if(semicolonFor == 1 and flag_1 == False):
						beginFor.Push(len(vciToken))
						vciToken.append(mainVariable)
						flag_1 = True

					if(("(" in strAux) or ("-u" in strAux) or ("*" in strAux) or ("/" in strAux) or ("+" in strAux) or ("-" in strAux) or ("LT" in strAux) or ("LE" in strAux) or ("GT" in strAux) or ("EQ" in strAux) or ("NOT" in strAux) or ("AND" in strAux) or ("OR" in strAux) or ("=" in strAux) or (")" in strAux)):
						for i in xrange(0, 14):
							if(prioridades[i][0] in strAux):
								p = prioridades[i][1]
								break

						if((int(pilaAux.length())) == 0):
							pilaAux.Push(strAux)

						elif(p < auxP):
							_n = int(pilaAux.length())
							for n in xrange(0, _n):
								pilaPop1 = pilaAux.Pop()
								if(("(" == pilaPop1) or (")" == pilaPop1) or ("," == pilaPop1)):
									pilaPop1 = ""
								else:
									vciToken.append(pilaPop1)
							pilaAux.Push(strAux)

						else:
							pilaAux.Push(strAux)

						auxP = p
					else:
						if(strAux != ","):
							vciToken.append(strAux)

		elif(arrayS[0] == "{"):
			auxForBreak+=1

		elif(arrayS[0] == "}"):
			mV = None
			mV = letraFor.Pop()

			vciToken.append(mV)
			vciToken.append(mV)
			vciToken.append(numeroFor.Pop())
			vciToken.append("+")
			vciToken.append("=")
			vciToken.append(">>" + str(beginFor.Pop()) + "<<")
			vciToken.append("GOTO")
			vciToken[int(pilaBreak.Pop()) - 1] = ">>" + str(len(vciToken)) + "<<"
 			vciToken[int(pilaFor.Pop()) - 1] = ">>" + str(len(vciToken)) + "<<"
			auxForBreak = auxForBreak - 1 

			if(auxForBreak == 0):
				vciToken[int(pilaBreak.Pop()) - 1] = ">>" + str(len(vciToken)) + "<<"
##############################################################################################################################
#################################################### SHOW AND GET ############################################################

		elif(arrayS[0] == "SHOW"):
			for i in xrange(1, len(arrayS)):
				if(("," in arrayS[i]) == False and ("'" in arrayS[i]) == False):
					if("SUCUADRADOES" in arrayS[i]):
						cadenax = "SU CUADRADO ES"
						vciToken.append(cadenax)
					else:
						vciToken.append(arrayS[i])
					vciToken.append("SHOW")
			vciToken.append("<SaltoDeLinea>")

		elif(arrayS[0] == "GET"):
			for f in xrange(1, len(arrayS)):
				strAux = arrayS[f]
				if(("(" in strAux) or ("-u" in strAux) or ("*" in strAux) or ("/" in strAux) or ("+" in strAux) or ("-" in strAux) or ("LT" in strAux) or ("LE" in strAux) or ("GT" in strAux) or ("EQ" in strAux) or ("NOT" in strAux) or ("AND" in strAux) or ("OR" in strAux) or ("=" in strAux) or (")" in strAux)):
					for i in xrange(0, 14):
						if(prioridades[i][0] in strAux):
							p = prioridades[i][1]
							break

					if((int(pilaAux.length())) == 0):
						pilaAux.Push(strAux)

					elif(p < auxP):
						_n = int(pilaAux.length())
						for n in xrange(0, _n):
							pilaPop1 = pilaAux.Pop()
							if(("(" == pilaPop1) or (")" == pilaPop1) or ("," == pilaPop1)):
								pilaPop1 = ""
								vciToken.append("GET")
							else:
								vciToken.append(pilaPop1)
						pilaAux.Push(strAux)
					else:
						pilaAux.Push(strAux)

					auxP = p;
				else:
					if(strAux != ","):
						vciToken.append(strAux)

			_i = int(pilaAux.length())
			for i in xrange(0, _i):
				pilaPop2 = pilaAux.Pop()
				if(("(" == pilaPop2) or (")" == pilaPop2) or ("," == pilaPop2)):
					pilaPop2 = ""
				else:
					vciToken.append(pilaPop2)

			vciToken.append("GET")
			vciToken.append("<return>")

############################################################################################################################
def analysis(character):

	global tokens 
	global variables_table 
	global index
	global line 
	global r 
	global typee
	global type_var 
	global constant 
	global variable 
	global aux_line 
	global declared 
	global special_operators
	global reserved_words
	global states
	

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

		if (isInteger(constant) == True):  #Reconocemos si es entero
			typee = 15
		elif (isFloat(constant) == True): #Reconocemos si es flotante
			typee = 14
		elif ((constant[0] == string) and (constant == string)): # Reconocemos si es cadena 
			typee = 16

		token = [typee, line, 0, constant.replace('"','').replace(' ','')]
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
				token = [typee, line, 0, character.replace(' ','')]
				tokens.append(token)
#--------------------------------------------------------------------------------------------------------------------------
	if (r == 1000 or (r == 1 and variable != "")):
		if ((code >= 65 and code <= 90) or (code >= 97 and code <= 122)): # If the character is a letter
			variable += character
		else:
			is_reserved_word = False
			is_array = False 
			cont = 0

			for word in reserved_words:
				if (reserved_words[cont][1] == variable):
					is_reserved_word = True
					typee = reserved_words[cont][0]
					break
				cont += 1

			if (is_reserved_word == True): #Esto significa que es una palabra reservada
				if(typee == 6 or typee == 7 or typee == 17):
					type_var = typee
					declared = True
				else:
					type_var = 0
					declared = False

				token = [typee, line, 0, variable.replace(' ','')]
				tokens.append(token)

			elif ((is_reserved_word == False) and ((variable == "") == False)):
				if(variable != "LT" and variable != "GT" and variable != "EQ" and variable != "LE" and variable != "GE" and variable != "NE"):
					
					direction = 1
					aux_index = index
					dim_array = 0
					left = 0
					right = 0

					for var in variables_table:					
						if(var[1] == variable):
							flag = True
							token = [var[0], line, direction, variable.replace(' ','')] 
							tokens.append(token)

							dim_array = int(var[2])
							left = int(var[3])
							right = int(var[4])
							break
						direction += 1

					if(flag == False):
						dimensions = 0
						left = 0
						right = 0

						token = [type_var, line, direction, variable.replace(' ','')]
						tokens.append(token)

						if (character == ','):
							dimensions = 0
							left = 0
							right = 0
						
						elif (character == '('):
							data = aux_line[(index + 1):(index + 1 + (aux_line.index(')', index) - index - 1))]

							temp = []
							is_array = True

							#if(data.find(',') != -1): 
							if(',' in data):
								temp = data.split(',')
								dimensions = 2
								left = temp[0]
								right = temp[1]

								token = [35, line, 0, "("]
								tokens.append(token)
								token = [81, line, 0, temp[0]]
								tokens.append(token)
								token = [40, line, 0, ","]
								tokens.append(token)
								token = [81, line, 0, temp[1]]
								tokens.append(token)
								token = [36, line, 0, ")"]
								tokens.append(token)

							else:
								dimensions = 1
								left = data
								token = [35, line, 0, "("]
								tokens.append(token)
								token = [81, line, 0, data]
								tokens.append(token)
								token = [36, line, 0, ")"]
								tokens.append(token)

							index = aux_line.index(')', index)
						
						if(type_var == 96):
							var = [type_var, variable, dimensions, int(left), int(right), declared]
							variables_table.append(var)
						else:
							var = [type_var, variable, dimensions, int(left), int(right), declared, 0]
							variables_table.append(var)
					flag = False 
				else:
					cont = 4
					while(cont < 11):
						if(special_operators[cont][1] == variable):
							typee = special_operators[cont][0]
							break
						cont += 1

					token = [typee, line, 0, variable.replace(' ','')]
					tokens.append(token)
					variable = ""
#--------------------------------------------------------
			if (character != ' ' and is_array == False):
				cont = 0
				for operator in special_operators:
					if (special_operators[cont][1] == character):
						typee = special_operators[cont][0]
						flag = True
					if (flag == True):
						flag = False
						break
					cont += 1
				token = [typee, line, 0, character.replace(' ','')]
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

constant = ""
variable = ""
aux_line = ""

r = 1
line = 1
typee = 0
type_var = 0
index = 0

declared = False
vciToken =[]
pilaIf = Stack()
pilaAux = Stack()
mainPosition = 0
p = 0
auxP = 0
position = 0

#Recorremos linea por linea 
for text_line in fichero:
	#Guardamos la linea en aux_line 
	aux_line = text_line.upper()
	#mientras indice sea menor al tamao de la linea y que la linea no contenga el caracter #
	while(index < len(text_line) and text_line[index] != '#'):
		#llamamos al metodo y enviamos cada caracter
		analysis(text_line[index].upper())
		# si es el final brincamos espacio
		if(index == len(text_line)-1):
			analysis(' ')
		index +=1
	line += 1
	index = 0

	token = [0,0,0,"FINLINEA"]
	tokens.append(token)

auxStr = None
start = False 

for token in tokens:
	#if(("MAIN" in token) or ("SUB" in token)):
	if(token[3] == "MAIN" or token[3] == "SUB"):
		start = True
	#if("BEGIN" in token):
	if(token[3] == "BEGIN"):
		vciToken.append("?")
		vciToken.append("GOTO")
	if(start == True):
		if (token[3] != ' ' and token[3] != '\n' and token[3] != '\r' and token[3] != '\t'):
			arrayStr = token

			if(arrayStr[len(arrayStr) - 1] != "FINLINEA"):
				palabra = ""
				palabra = palabra + str(arrayStr[3])

				if(auxStr == None):
					auxStr = palabra
				else:
					auxStr = auxStr + " " + palabra
			else:
				IntermediateCode(auxStr)
				auxStr = None

##############################################################################################################################
######################################################## TOKENS ##############################################################
"""
print "Tokens structure = [Type, Line, Direction, Lexema]\n"
cont = 1
for token in tokens:
	if (token[3] != ' ' and token[3] != '\n' and token[3] != '\r' and token[3] != '\t' and token[3] != "FINLINEA"):
		print cont, token
		cont += 1
print '\n'
"""
##############################################################################################################################
###################################################### VARIABLES #############################################################

print "Variables structure = [Type, Variable, Dimensions, Left, Right, Declared, VCI]\n"
cont = 1
for variable in variables_table:
	print cont, variable 
	cont += 1
print '\n'

##############################################################################################################################
######################################################### VCI ################################################################
print "VCI\n"
cont = 0
for VCI in vciToken:
	print cont, VCI
	cont += 1
print '\n'

fichero.close()



