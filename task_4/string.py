import string

text = input("Enter a sentence: ")

result = ""

for char in text:
    if char not in string.punctuation:
        result += char

print("Without punctuation:", result)