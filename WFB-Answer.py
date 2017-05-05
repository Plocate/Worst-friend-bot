#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:57:18 2017

@author: paul.meunier
"""

import re
import random

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
    

#Is called if the useInput is recognised as a question
def generateAnswerToQuestion(userInput, listWord):
    answer = "Hello World"
    
    #for x in listWord:
        
    
    return answer
    
#Is called if the userInput is not a question and is correct
#Can generate a question
def generateAnswerToAffirmation(userInput, listWord):
    answer = "Hello World"
    
    return answer;


#Function is called if there is a word that isn't well written 
#or doesn't exist in the lexicon
def pickOneNonSense(userInput, listWord):
    #this boolean is used to know if we already began to fill answer
    alreadyCompleted = False
    
    answer = ""
    
    possibilities = []
    possibilities = getFromTag("nonsense")
    possibilities.append("I did no not understand")
    
    for word in listWord:
        if word.soustype.find("UKN"):
            if len(possibilities) > 0 and not alreadyCompleted:
                alreadyCompleted = True
                answer = listWord[random.randrange(0, len(possibilities), 1)].text
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
    return 
    
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
    print("extract tag" + temp[1])
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
    


pathLexicon="enlex-0.1.mlex"
pathData="DatabaseAnswer.txt"
database = []
dataTag = []
database, dataTag = extractData(pathData);
print ("Hello World\n")