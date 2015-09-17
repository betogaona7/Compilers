
# PRACTICE 4:

# Read a file and counting all the special characters and letters
# Sort highest to lowest or backwards

# Open a file in read mode
fichero = open("file4","r")

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
special_characters = ["!","@","#","$","%","&","/","(",")","=","'","+","-","*"]
results = []

# Method to count the each caracter
def count_character(text, character):
	initial = -1
	repeating_times = 0

	try:
		while True:
			initial = text.index(character, initial+1)
			repeating_times += 1
	except ValueError:
			return repeating_times

# Method to search a specific character in the text
def search_character(text, list_characters):
	for character in list_characters:
		total = count_character(text.lower(), character)
		if(total != 0):
			token = [character, total]
			results.append(token)	

# Insertion sort, the changes are in the original list too.
def sort_results(temp_list, original):
	j = 0
	count = 1

	while(count < len(temp_list)):
		key_temp = temp_list[count] 
		key_original = original[count] #KEY de la lista original

		j = count - 1
		while (j >= 0 and temp_list[j] > key_temp):
			temp_list[j + 1] = temp_list[j] 
			original[j +1] = original[j] #INTERCAMBIO en la lista original
			j = j - 1;
		temp_list[j + 1] = key_temp
		original[j + 1] = key_original  #INTERCAMBIO en la lista original
		count += 1
	return original

# Method to print the result, mode 0 is ascendent and mode 1 is descendent
def print_results(mode):
	if mode == 1:
		start = len(results) - 1
	elif mode == 0:
		start = 0

	for files in results:
		print results[start]
		if(mode == 1):
			start -= 1
		elif(mode == 0):
			start += 1


# Save the text in a variable
text = fichero.read()

# Search all characters in the text 
search_character(text, alphabet)
search_character(text, special_characters)

 # Make a temporal list with the numbers of repetitions to order 
aux = []
count = 0;
for index in results:
	aux.append(results[count][1])
	count += 1 

# Print results
sort_results(aux, results)
print_results(1)

# Close file 
fichero.close();