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

#Concatenate a list of string in on string
def concatStr(listStr):
    conc = ""
    for st in listStr:
        conc += st+" "
        
    return conc

#define correspondances between @SThinh and the lexicon abbrevations
def fillCorres(path):
    hTable = {}
    
    with open(path, "r") as fichier:
        for line in fichier:
            line = line.strip('\n')
            line  = line.strip()
            #line starting with '#'shall not be added to the database
            if line.find("#") != 0:
                if line != "":
                    listAt = line.split(':')
                    hTable[listAt[0]] = listAt[1]
                    
    fichier.close();
    
    return hTable

#Replace @smthing in the database sentences, we already know it contains a @
def replaceAt(answer, userInput, listWord):
    listAt = []
    count = answer.count('@')
    
    if count == 0:    #If there is no token to replace in
        return answer
    
    #we need to replace a token @
    global corresAt
    global nlp
    
    listAt = re.findall("@[A-Z][A-Z]", answer)
    
    for st in listAt:
        res = corresAt.get(st, "notFound")
        if(res != "notFound"):
            res = res.split('|')
            target = ""
            if(res[1] == "dobj"):
                for np in listWord.noun_chunks:
                    if np.root.dep_ == "dobj":
                        target = np.root.text
                        break;
            elif(res[1] == "nsubj"):
                for np in listWord.noun_chunks:
                    if np.root.dep_ == "nsubj":
                        target = np.root.text
                        break;
            elif(res[0] == "PROPN" or res[1] == "attr"):
                for np in listWord.noun_chunks:
                    #print( np.root.text + " : " + np.root.dep_)
                    if np.root.dep_ == "attr":
                        target = np.root.text
                        break;
            elif res[0] == "ADJ":
                for word in listWord:
                    if word.pos_ == "ADJ":
                        target = word.text
                        break
            elif res[0] == "VERB":
                for word in listWord:
                    if word.pos_ == "VERB":
                        target = word.text
                        break
            elif res[0] == "UKN":
                for word in listWord:
                    if word.lemma == 776980:
                        target =word.text
                        break
            """elif res[0] == GROUP:
                for word in wordList:
                    if word.pos_ == ADJ:
                        target = word.text
                        break"""      
                        
            answer =  re.sub(st, target, answer)
                    
                    
    return answer

#Cherche si un des tags de la base de donnée est inclus dans la phrase
def existTags(userInput, listWord, opTag = ""):
    sentence = concatStr(userInput)
    global dataTag
    listPoss = []
    for x in dataTag:
        for y in x.tagList:
            if opTag != "" and y in opTag:
                listPoss.append(x.line)
            elif sentence.count(y) != 0:
                listPoss.append(x.line)
                
    if len(listPoss)==0:
        return ""
    
    answer = listPoss[rndom.randrange(0, len(listPoss), 1)]
    
    return replaceAt(answer, userInput, listWord)

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

#Search a valid pronoun which could be user in an answer
def build_pronoun(listWord):

    for w in listWord:
        if w.tag_ == "PRP":
            if w.text.lower == 'you':
                return "I", 
            if w.text.lower == 'i':
                return "you"
            if w.text.lower == 'he':
                return 'he'
            if w.text.lower == 'she':
                return 'she'
            if w.text.lower == 'it':
                return 'it'
            
    for np in listWord.noun_chunks:
        if np.root.dep_ == 'nsubj':
            return np.text
    
    return ""

#Search a valid noun which could be user in an answer
def build_noun(listWord):
    
    for np in listWord.noun_chunks:
        if np.root.dep == "pobj" or np.root.dep == "dobj":
            for w in listWord:
                if np.text == w.text:
                    return np.text + np.root.head.text, w.tag_
    i=0
    for w in listWord:
        if w.pos_ == "NOUN" or w.pos_ == "PROPN":
            return w.text, w.tag_
        
    return "", ""

#Search a valid adj which could be user in an answer
def build_adj(listWord):
        
    for w in listWord:
        if w.tag_ == "JJ" or w.pos_ == "JJR" or w.pos_ == "JJS":
            #print(w.text)
            return w.text
    
    return ""

#Search a valid verb which could be user in an answer
#We will try to do a a bit of time concordance
def build_verb(listWord):
    for np in listWord.noun_chunks:
        if np.root.dep_ == 'nsubj':
            for w in listWord:
                if w.text == np.root.head.text:
                    #si un verbe est attaché au sujet, on retourne le lemma
                    return w.lemma_, w.tag_
    
    #Sinon on chercher un autre verbe dans la phrase
    for w in listWord:
        if w.pos_ =="VERB":
            return w.lemma_, w.tag_
        
    #On a pas trouvé de verbe
    return "", ""

#Is called if the useInput is recognised as a question
def generateAnswerToQuestion(userInput, listWord):
    answer=""
    sentence = concatStr(userInput)
    
    doc = nlp(u"%s" % (sentence,))
    
    #tag will make up for simple stuff like greeting or saying good bye
    if(existTags(userInput, listWord)!=""):
        return existTags(userInput, listWord)
    
    pronoun = build_pronoun(listWord)
    dual = pronoun.split(" ")
    pronoun = dual[len(dual)-1]
    noun, typeNoun = build_noun(listWord)
    adjective = build_adj(listWord)
    verb, typeVerb = build_verb(listWord)
    lemmeVerb = verb
    
    print(sentence)
    print("pronoun : " + pronoun + " | noun:typeNoun" + noun +":"+typeNoun + " | verb:typeVerb " + verb + ":" +typeVerb )
    
    #Conjugate verb and trim pronoun before attacking the interogative word switch "switch"
    #conjugate the lemme verb : https://spacy.io/docs/usage/pos-tagging#pos-tagging-english
    
    #here noly present tense, but there should be past and future
    #mustbe a way to counjugate but i don't know howto 
    """if typeVerb == "VBZ":   #3rd person - present tense
        
    elif typeVerb == "VPB"  #other persons - present tense
    
    
    global questionWords
    #Si le nom de la phrase est dans les mots interrogatifs
    if(noun !="" and noun.lower() in questionWords):
        if noun.lower() in "what":
            
        if noun.lower() in "why":
        
        if noun.lower() in "where":
            
        if noun.lower() in "which":
            
        if noun.lower() in "how":
    else:
        """
    
    return answer
    
#Is called if the userInput is not a question and is correct
#Can generate a question
def generateAnswerToAffirmation(userInput, listWord):
    
    answer=""
    sentence = concatStr(userInput)
    
    doc = nlp(u"%s" % (sentence,))
    
    #tag will make up for simple stuff like greeting or saying good bye
    if(existTags(userInput, listWord)!=""):
        return existTags(userInput, listWord)
    
    
    #We will try to build a generic answer
    pronoun = build_pronoun(listWord)
    noun, typeNoun = build_noun(listWord)
    adjective = build_adj(listWord)
    verb, typeVerb = build_verb(listWord)
    lemmeVerb = verb
        
    if verb != "":
        if verb == "be":
            if pronoun == "I":
                verb== "am "
            elif(pronoun == "he" or pronoun == "she" or pronoun == "it"):
                verb== "is "
            else:
                verb== "are "
        elif verb == "have":
            if(pronoun == "he" or pronoun == "she" or pronoun == "it"):
                verb=="has "
            else:
                verb== "have "
        elif verb == "go":
            if(pronoun == "he" or pronoun == "she" or pronoun == "it"):
                verb== "goes "
            else:
                verb+= "go "
        else:
            if(pronoun == "he" or pronoun == "she" or pronoun == "it"):
                verb= verb+"s "

    if noun != "" and typeNoun == "NN":
        if noun[0] in 'aeiou':
            noun = "an " + noun
        else:
            noun = "a " + noun
    
    # 1 of 4 times, we are gonna pick a random thingy       
    if rndom.randrange(0, 4, 1)==0:  
        listSent = getFromTag("generic")
        sent = listSent[rndom.randrange(0, len(listSent), 1)]
        
        if noun =="":
            noun = rndom.choice(("You", "Ronald Mac Donald", "cat", "unicorns"))
        
        sent = re.sub("@NOUN", noun, sent)
        sent = re.sub("@PRONOUN", pronoun, sent)
        sent = re.sub("@VERB", verb, sent)
    
        return sent

    if pronoun == "":
        pronoun = rndom.choice(("You", "I"))

    if adjective != "":
        return rndom.choice(( ("I'am " +  adjective + " too"), ("why" + verb + " "+pronoun+" "+adjective)))
    
    if verb == "":
        rndom.choice(("", "like", "kill", "eat"))
    
    if verb == "" or lemmeVerb == "be":
        if pronoun == "I" or pronoun == "i":
            answer += "am "
        elif(pronoun.lower() == "he" or pronoun.lower() == "she" or pronoun.lower() == "it"):
            answer += "is "
        else:
            answer += "are "
        answer += pronoun + " "
        
        if adjective != "":
            answer += adjective + " "
        else:
            answer += rndom.choice(("...", "fat", "stupid", "idiot", "naive", "nice", "interested in irony", "awesome"))
        answer += "?"
    else:
        answer += "Does" if (pronoun == "he" or pronoun == "she" or pronoun == "it") else "Do"
        answer += rndom.choice((" ", "n't "))
        answer += pronoun + " "
        answer += verb + " "
        if verb == "do":
            answer += rndom.choice(("exercise", "sport, you're fat", "massmurder", "your homework everyday", ))
        elif verb == "go":
            answer += rndom.choice(("to the moon", "under the sea", "on youtube", "dancing", "buy some pate en croute"))
        else:
            answer += rndom.choice(("pizza with pineapple", "Trump", "in a way comprable to Twittler", "dancing", "baguette"))
    
        
    return answer;


#Function is called if there is a word that isn't well written 
#or doesn't exist in the lexicon of spacy
def pickOneNonSense(userInput, listWord):
    #this boolean is used to know if we already began to fill answer
    alreadyCompleted = False
    
    answer = ""

    possibilities = []
    possibilities = getFromTag("nonsense")
    
    for word in listWord:
        if word.lemma == 776980:
            if len(possibilities) > 0 and not alreadyCompleted:
                alreadyCompleted = True
                answer = possibilities[rndom.randrange(0, len(possibilities), 1)]
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
    lisTag = temp[0].split("|")
    tagLine = TagAndLine(lisTag, temp[1])
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
print("Loading the dictionnary...")
nlp = spacy.load('en')
print("Dictionnary loaded !")

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

#Fill the dictionnary with correspondances between @SThing and the 
#lexicon
corresAt = {}
corresAt = fillCorres("corresAt.txt")

#parseDictionary defined in lecture.py
#dico = parseDictionary("enlex-0.1.mlex")
"""
for x in dataTag:
    print("list : ")
    for y in x.tagList:    
        print(y)
    print( "line : "+x.line)
    print()
"""

print("Hajime!")

history = ""

while True:   
    userInput = input("You >> ");
    if(userInput == "stop"):
        break;
    
    if(len(userInput) == 0):
        continue;
    #stopWords = ["then", "therefore", "at", "of", "the", "thus", "so", "consequently"]
    questionWords = ["which", "what", "when", "who", "why", "where", "how", "whose", "whom", "am", "are", "is", "was", "were", "would", "can", "could", "shall", "will", "might", "must", "may", "do", "did"]
    
    
    sentenceType = "affirmation"
    
    
    userInLow = userInput.lower()
    
    userInput = nlp(u"%s"%(userInput, ))
    tokens = tokenise(userInLow,"en")
    
    
    
    subjects = []
    for np in userInput.noun_chunks:
        if np.root.dep_ == "nsubj":
            subjects.append(tokenise(np.text, "en"))
            

    for idx in range(len(userInput)):
        if(userInput[idx].pos_ == "VERB"):
            for idy in range(len(subjects)):
                if idx+1 < len(userInput) and subjects[idy][0] == userInput[idx+1].text:
                    sentenceType = "question"
                    for idz in range(len(subjects[idy])):
                        if(idz+idx+1 >= len(userInput) or subjects[idy][idz] != userInput[idz+idx+1].text):
                            sentenceType = "affirmation"
                            
    if userInput[len(userInput)-1].text == "?":
        sentenceType = "question" 
        
    for w in userInput:
        if w.lemma >= 776980:
            sentenceType = "nonsense"
    
    print(sentenceType)
    if userInLow == history:
        print("WFB << " + rndom.choice(["Repeating yourself dude","Alzeimer is watching you",
                           "stop harassin me","loosing my time...", "and again"]))
    else:
        print("WFB << " + generateAnswer(tokens, sentenceType, userInput))
    history = userInLow