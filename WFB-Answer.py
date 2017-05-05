#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:57:18 2017

@author: paul.meunier
"""

import re
import random as rndom
import spacy
from lecture import *

class typeTopic:
	def _init_(self, text, soustype):
		self.text = text
		self.soustype = soustype

#Contains a sentence from the database and its associated topics/tags
class TagAndLine:
    def __init__(self, tag, lineT):
        self.tagList = tag
        self.line = lineT


#Return a list of sentences which are correlated with the tag passed as topic
def getFromTag(topic):
    global dataTag
    listSent = []
    for x in dataTag:
        if topic in x.tagList:
            listSent.append(x.line)
            
    return listSent

#Uses spacy dependency parse to give a role to word in user input
#Not every word needs to have a role, primary goal is to search for
#the subject and the object of the sentence  
def setWordRole(listWord):
    global nlp
    sentence =""
    for x in listWord:
        sentence += x.text
    
    doc = nlp(u"%s"% (sentence,))
    for np in doc.noun_chunks:
        for word in listWord:
            if word.text == np.root.text:
                word.parseType = np.root.dep_ + "|" + np.root.head.text
            

    return listWord

#Is called if the useInput is recognised as a question
def generateAnswerToQuestion(userInput, listWord):
    sentence=""
    for x in userInput:
         sentence += x+" "
    
    sentence = nlp(u"%s" % (sentence,))
    
    #for np in sentence.noun_chunks:
        #print(np.text, np.root.text, np.root.dep_, np.root.head.text)
    

    return answer
    
#Is called if the userInput is not a question and is correct
#Can generate a question
def generateAnswerToAffirmation(userInput, listWord):
    
    
    
    return answer;


#Function is called if there is a word that isn't well written 
#or doesn't exist in the lexicon
def pickOneNonSense(userInput, listWord):
    #this boolean is used to know if we already began to fill answer
    alreadyCompleted = False
    
    answer = ""
    
    possibilities = []
    possibilities = getFromTag("nonsense")
    
    for word in listWord:
        if word.soustype.find("UKN"):
            if len(possibilities) > 0 and not alreadyCompleted:
                alreadyCompleted = True
                answer = listWord[rndom.randrange(0, len(possibilities), 1)].text
                answer = re.sub("@UT", word.text, answer)
            elif not alreadyCompleted:
                alreadyCompleted = True
                answer = "I did not understand" + word.text
            else:
                answer += " and " + word.text
                
    #Default answer if the database was empty, to be replaced by a generated
    #answer            
    if not alreadyCompleted:
        answer = "I did not understand your jibberish"
    
    return answer

#Function that replies a random anwser, pick a random word in the input 
def randomAnswer(userInput):
    global database
    global dataTag
    for l in database:
        for x in userInput:
            if len(x) >3 and x.lower() in l:
                return l
        
    return database[rndom.randrange(0, len(database), 1)]
    
#Function to extract premade sentences from a file and add them to the good 
#list. Datatag is a list of sentences which contains a list of tag
def extractData(path):
    database = []
    dataTag = []
    with open(path, "r") as fichier:
        for line in fichier:
            line = line.strip('\n')
            line  = line.strip()
            #line starting with '#'shall not be added to the database
            if line.find("#") != 0:
                if line != "":
                    #this line of the database has tags
                    if line.find("/>") != -1:
                        dataTag.append(extractTagFromLine(line))
                    else:
                        database.append(line)
                
    fichier.close();

    return database, dataTag


#Function which parse a line from the database eand separate the tags and the 
#actual text
def extractTagFromLine(line):
    
    temp =[]
    temp = line.split("/>")
    temp[0] = temp[0].replace("<", "", 1)
    temp[0] = temp[0].split("|")
    tagLine = TagAndLine(temp[0], temp[1])
    return tagLine



#Call other function to generate an answer depending on the input
def generateAnswer(userInput, sentenceType, listWord):

    if sentenceType == "question":
        answer = generateAnswerToQuestion(userInput, listWord)
    elif sentenceType == "affirmation":
        answer = generateAnswerToAffirmation(userInput, listWord)
    elif sentenceType == "nonsense":
        answer = pickOneNonSense(userInput, listWord)
        
    return answer
    

#load spacy, to use in function call: global nlp
nlp = spacy.load('en')

#Chemin vers le lexicon
pathLexicon="enlex-0.1.mlex"

#Chemin vers le fichier txt contenant toutes les phrases préconstruites
pathData="DatabaseAnswer.txt"

#Liste contenant toutes les lignes de la bases de données sans tag
database = []

#Liste contenant toutes les lignes de la bases de données ayant un tag
dataTag = []

#On remplit les deux listes précédentes avec le contenu du fichier texte
database, dataTag = extractData(pathData);

#Main Plocate
#parseDictionary defined in lecture.py
dico = parseDictionary("enlex-0.1.mlex")

print("Hajime!") 
while True:
    
    #Traitement de userLine: separation, tagging des différents tokens    
    userInput = input("You : ");
    
    stopWords = ["then", "therefore", "at", "of", "the", "thus", "so", "consequently"]
    questionWords = ["which", "what", "when", "who", "why", "where", "how", "whose", "whom", "am", "are", "is", "was", "were", "would", "can", "could", "shall", "will", "might", "must", "may", "do", "did"]
    
    
    sentenceType = "affirmation"
    
    
    userInput = userInput.lower()
    tokens = tokenise(userInput, "en")
    for t in tokens:
    	if t in stopWords:
    		tokens.remove(t)			
    	if t == "?":
    		sentenceType = "question"
    
    		
    listWord = tagToken(tokens, dico)
    listWord = setWordRole(listWord)
    
    #If the bot doesn't know one of the words, it will send a premade answer
    for w in listWord:
    	if w.wordType == "UKN":
    		#print("TEST "+w.text)
    		sentenceType = "nonSense"    
        
    print(rndom.randrange(0, 10, 2))    
    print("WFB << " + generateAnswer(userInput, sentenceType, wordList))
    if "stop" in tokens:
        break

print ("Hello World\n")