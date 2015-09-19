
# PRACTICE 5

# Read a file, and count number of integers and real numbers
# and print how many are greater than 100 and wich are less equal to 100

# Open a file in read mode
fichero = open("file5","r")

#Save the text in a variable
text = fichero.read()

tokens = []
errors = []


# Method to clean the text 
def edit_text(original_text):
	clean_text = "";
	for character in original_text:
		if(character == '\n'):
			clean_text = clean_text + " "
		elif(character != '\r' and character != '\t' and character != '\b' and character != '\f'):
			clean_text = clean_text + character
	return clean_text

# Method to know what type of variable is
def text_analysis(clean_text):
	state = 0
	index = 0
	lexema = ""
	error = "Sintaxis error: "

	for character in clean_text:
		letter = clean_text[index]
		code = ord(letter) #Convert to ASCII code
#..................................................................................
		if state == 0:
			
			if code == 34: #The character is a " and change a STATE 1 (String)
				state = 1
			elif code >= 48 and code <= 57: #The character is a number and change a STATE 2 (Integer)
				lexema = lexema + letter
				state = 2
			elif code == 32: #The character is a space, not do anything.
				state = 0
			else: #Is a incorrect character
				errors.append(error + letter)
				state = 0
#..................................................................................
		elif state == 1: #STRING
			
			if (code >= 65 and code <= 90) or (code >= 97 and code <= 122) or (code >= 48 and code <= 57) or (code == 32):  #The character is a letter upper or low, or the character was number or space
				lexema = lexema + letter
				state = 1
			elif code == 34: #The character is a ", Save the token and reload the state. 
				token = [13, lexema]
				tokens.append(token)
				lexema = ""
				state = 0
			else: #Is a incorrect character
				errors.append(error + letter)
				state = 0
#..................................................................................
		elif state == 2: #INTEGER
			
			if  code >= 48 and code <= 57: #The character is a number
				lexema = lexema + letter
				state = 2
			elif code == 46: #The character is a point and change to STATE 3 (Double)
				lexema = lexema + letter
				state = 3
			elif code == 32: #The character is a space, save the token and reload the state
				token = [11, lexema]
				tokens.append(token)
				lexema = ""
				state = 0
			else:
				errors.append(error + letter)
				state = 0
##..................................................................................
		elif state == 3: #DOUBLE

			if code >= 48 and code <= 57: #The character is a number 
				lexema = lexema + letter
				state = 3
			elif code == 32: #The character is a space, save the token and reload the state
				token = [12, lexema]
				tokens.append(token)
				lexema = "" 
				state = 0
			else:
				errors.append(error + letter)
				state = 0

		index += 1

#Method to count each type of variable
def count_types(result_list):
	count = 0
	integer = 0
	greater = 0
	smaller = 0
	double = 0

	for row in result_list:
		if result_list[count][0] == 12:     # Are reals?
			double += 1
		elif result_list[count][0] == 11:   # Are Integers?
			integer += 1
			if result_list[count][1] > 100: # Higher than 100?
				greater += 1
			else:
				smaller += 1 

		count += 1

	print "\nEnteros: ", integer, "\nReales: ", double, "\nMayores a 100: ", greater, "\nMenores iguales a 100: ", smaller


# Call the method to know what type of variable is
text = edit_text(text)
text_analysis(text + " ")

# Print tokens
for row in tokens:
	print row

# Count how many are higher than 100 and how many are less equal to 100, also count integers and real numbers
count_types(tokens)

# Close file 
fichero.close()
