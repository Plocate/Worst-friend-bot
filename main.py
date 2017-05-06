#-*-coding:utf-8-*-


from lecture import *
#import nltk
#nltk.download()
dictionary = parseDictionary("enlex-0.1.mlex")
entree = input("You : ");
stopWords = ["then", "therefore", "at", "of", "the", "thus", "so", "consequently"]
questionWords = ["which", "what", "when", "who", "why", "where", "how", "whose", "whom", "am", "are", "is", "was", "were", "would", "can", "could", "shall", "will", "might", "must", "may", "do", "did"]


sentenceType = "affirmation"


entree = entree.lower()
tokens = tokenise(entree, "en")
for t in tokens:
	if t in stopWords:
		tokens.remove(t)			
	if t == "?":
		sentenceType = "question"

		
userInput = tagToken(tokens, dictionary)
for w in userInput:
	if w.wordType == "UKN":
		print("TEST "+w.text)
		sentenceType = "nonSense"
		
print(sentenceType);
     
sent = "the cake is a lie.";