
# PRACTICE 1:
# Read file and display how many lines have it.

# Open file in read mode
fichero = open("file2", "r")
count = 0;

# Count lines
for line in fichero:
	count += 1

# Display number of lines
print count

# Close file
fichero.close()
