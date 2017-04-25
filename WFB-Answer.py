#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:57:18 2017

@author: paul.meunier
"""


def generateAnswerToQuestion(userInput):
    answer = "Hello World";    
    
    return answer;
    
def generateAnswerToAffirmation(userInput):
    answer = "Hello World";
    
    return answer;
    
def pickOneNonSense(userInput):
    answer = "Hello World";    
    
    return answer;
    

def generateAnswer(userInput, sentenceType):
        
    pathLexicon="/home/tp-home006/pmeunie/Desktop/TAL_S8/Projet/enlex-0.1.mlex";
    pathAnswer="/home/tp-home006/pmeunie/Desktop/TAL_S8/Projet/DatabaseAnswer.txt"; 
    pathQuestion="/home/tp-home006/pmeunie/Desktop/TAL_S8/Projet/DatabaseQuestion.txt";
    
    if sentenceType == "question":
        answer = generateAnswerToQuestion(userInput);
    elif sentenceType == "aff":
        answer = generateAnswerToAffirmation(userInput);
    elif sentenceType == "nonSense":
        answer = pickOneNonSense(userInput);
        
    return answer;
    
