
# PRACTICE 2:

# Read file and display how many character "=" have each line
# Which it's line with the maximum and minimum number of characters and how were these

# Open file in read mode
fichero = open("file2", "r")

higher = []
lines = []
characters = []

# Method to search a specific character in the line 
def search_character(line,character):

	initial = -1;
	repeating_times = 0;
	
	try:
		while True:
			initial = line.index(character, initial+1)
			repeating_times += 1
	except ValueError:
			return repeating_times

# Method to get the characters
def get_characters(line):
	count = 0
	while count < len(line):
		characters.append(line[count])
		count += 1
	return list(set(characters))


# Read each line
for line in fichero:
	# Count equals
	print 'Iguales:', search_character(line, '=')
	# Count characters
	total_characters = len(line.strip()) - search_character(line,' ')
	print 'Total caracteres:', total_characters , '\n'
	# Save the number of characters in each line
	higher.append(total_characters)
	# Save the complete line 
	lines.append(line)

# Save results
max_characters = max(higher)
index_max = (higher.index(max_characters)) + 1
full_line = lines[index_max -1]

# Print results
print "La linea con mayor numero de caracteres es la linea numero: ", index_max ,", que contiene ", max_characters, " caracteres."
print "Linea: ", full_line
print "Caracteres: ", get_characters(full_line.strip()), "\n"

# Close file
fichero.close()

