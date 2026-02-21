sentence = input("Enter a sentence: ")

words = sentence.split()

words.sort()

print("Sorted sentence:")
print(" ".join(words))