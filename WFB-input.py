# -*- coding: utf-8 -*-
"""
Created on Sat May  6 02:23:01 2017

@author: utilisateur
"""


import re
import random as rndom
import spacy
from lecture import *

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



#load spacy, to use in function call: global nlp
nlp = spacy.load('en')

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
#dico = parseDictionary("enlex-0.1.mlex")

print("Hajime!") 
while True:
    
    #Traitement de userLine: separation, tagging des différents tokens  
    userInput = input("You : ");
    if(userInput == "stop"):
        break;
    #stopWords = ["then", "therefore", "at", "of", "the", "thus", "so", "consequently"]
    questionWords = ["which", "what", "when", "who", "why", "where", "how", "whose", "whom", "am", "are", "is", "was", "were", "would", "can", "could", "shall", "will", "might", "must", "may", "do", "did"]
    
    
    sentenceType = "affirmation"
    
    
    userInput = userInput.lower()
    userInput = nlp(u"%s"%(userInput, ))
    subjects = []
    for np in userInput.noun_chunks:
        print(np.text, np.root.text, np.root.dep_, np.root.head.text)
        if np.root.dep_ == "nsubj":
            subjects.append(tokenise(np.text, "en"))
            

    for idx in range(len(userInput)):
        if(userInput[idx].pos_ == "VERB"):
            for idy in range(len(subjects)):
                if subjects[idy][0] == userInput[idx+1].text:
                    sentenceType = "question"
                    for idz in range(len(subjects[idy])):
                        if(subjects[idy][idz] != userInput[idz+idx+1].text):
                            sentenceType = "affirmation"
        print(userInput[idx].text, userInput[idx].lemma, userInput[idx].lemma_, userInput[idx].tag, userInput[idx].tag_, userInput[idx].pos, userInput[idx].pos_)
        
    if userInput[len(userInput)-1].text == "?":
        sentenceType = "question"
    print(sentenceType)
    # I I nsubj like
    # green eggs eggs dobj like
    # ham ham conj eggs
