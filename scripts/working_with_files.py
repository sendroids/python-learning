# This script writes to and reads from a file
filename = "sample.txt"
with open(filename, "w") as file:
    file.write("This is a sample file.\nLearning Python is fun!")

with open(filename, "r") as file:
    content = file.read()
    print("File content:", content)