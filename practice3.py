
# PRACTICE 3:

# Read file and convert text to uppercase
# also search the word "FOR" and "IF".

# Method to read file and modify the text
def read_file():
	fichero = open("file3", "r")
	lines = fichero.readlines()
	fichero.close()
	overwrite_file(lines)

# Method to overwrite the file and print the results
def overwrite_file(text):
	count = 0
	fichero = open("file3", "w")
	for line in text:
		new_line = line.upper()
		fichero.write(new_line)
		count += 1
		print "line:", count," IF: ", search_word(new_line, " IF "), " FOR: ", search_word(new_line," FOR ") 
	fichero.close()

# Method to search a specific word
def search_word(line, word):
	initial = -1;
	repeating_times = 0;
	line_fixed = " "+ line.strip() + " "

	try:
		while True:
			initial = line_fixed.index(word, initial+1)
			repeating_times += 1
	except ValueError:
			return repeating_times

# Call the main method
read_file()
