#!/opt/anaconda3/bin/python3
#-*-coding:utf-8-*-


from lecture import *
import nltk
nltk.download()
parags = read_paragraph_file("textaupif.paras")
stopWords = ["then", "therefore", "at", "of", "the", "thus", "so", "consequently"]
questionWords = ["which", "what", "when", "who", "why", "where", "how", "whose", "whom", "am", "are", "is", "was", "were", "would", "can", "could", "shall", "will", "might", "must", "may", "do", "did"]


question = False

tokens = []
for p in parags :
	sents = segment_into_sents(p)
	for s in sents :
		lowercase_sentence(s)
		tokens = tokenise(s, "en")
		for t in tokens:
			while t in stopWords:
				tokens.remove(t)			
			if tokens[1] in questionWords:
				question = True 
print(question)



dictionary = parseDictionary("enlex-0.1.mlex")
