#!/opt/anaconda3/bin/python3
#-*-coding:utf-8-*-

import re
from math import *
from random import *

class Bigram:
	def _init_(self, s1, s2):
		self.s1 = s1
		self.s2 = s2

class typeTopic:
	
	def __init__(self, text, type, subType):
		self.text = text
		self.type = type
		self.subTyle = subTyle
		


def read_paragraph_file(nomfichier):

	listPara = []
	with open(nomfichier, "r") as fichier:
		for line in fichier:
			line = line.strip()
			if line != "":
				listPara.append(line)
	fichier.close();
	return listPara;

def parseDictionary(nomFichier):
	
	dictWords = {}
	print("Parsing the library...\n");
	with open(nomFichier, "r") as fichier:
		for line in fichier:
			temp = line.split('\t')
			#print("test" + temp[0]);
			dictWords[temp[0]] = typeTopic(temp[2], temp[1], temp[3])
	fichier.close()
	print("Library parsed !");
	return dictWords;

	
def tagToken(sent, dict):
	tok = [];
	for word in sent:
		if word in dict:
			tok.append(dict[word])
		else:
			tok.append(typeTopic(word, "UKN"))
	return tok;


def write_paragraph_file(listPara, nomfichier):
	with open(nomfichier, "w") as fichier:
		for line in listPara:
			fichier.write(line + "\n")
		
def read_word_list_file(filename):
    wordlist = []
    with open(filename, "r") as filepointer:
        for line in filepointer.readlines():
            word = line.strip() # remove whitespace
            if word=="": continue # ignore blank lines
            wordlist.append(word)
    return wordlist

def write_word_list_file(wordlist, filename):
    with open(filename, "w") as filepointer:
        for word in wordlist:
            filepointer.write(word+"\n")    

def read_tab_separated_file(nomfichier):
	listMot = []
	with open(nomfichier, "r") as fichier:
		for ligne in fichier:
			ligne = ligne.strip();
			listMot.append(ligne.split("\t"));
	fichier.close()
	return listMot;
				
def write_file_tab_separated(list_word, nomfichier):
	with open(nomfichier, "w") as fichier:
		for line in list_word:
			for mot in line:
				fichier.write(mot + "\t");
			fichier.write("\n");

def segment_into_sents(paragraph):

    cannot_precede = ["M", "Prof", "Sgt", "Lt", "Ltd", "co", "etc", "[A-Z]", "[Ii].e", "[eE].g"] # non-exhaustive list
    regex_cannot_precede = "(?:(?<!"+")(?<!".join(cannot_precede)+"))"
    
    if "\n" in paragraph: exit("Error in paragraph: paragraph contains \n.")       
    newline_separated = re.sub(regex_cannot_precede+"([\.\!\?]+([\'\â€™\"\)]*( |$)| [\'\â€™\"\) ]*))", r"\1\n", paragraph)
    sents = newline_separated.strip().split("\n")
    for s, sent in enumerate(sents):
        sents[s] = sent.strip()
    return sents
    
  
def lowercase_sentence(sentence):
	chaine = [c.lower() for c in sentence]
	print("TEST : " + chaine);
	return "".join(chaine)


def normalise(sent, lang):
    sent = re.sub("\'\'", '"', sent) # two single quotes = double quotes
    sent = re.sub("[`â€˜â€™]+", r"'", sent) # normalise apostrophes/single quotes
    sent = re.sub("[â‰ªâ‰«â€œâ€]", '"', sent) # normalise double quotes

    if lang=="en":
        sent = re.sub("([a-z]{3,})or", r"\1our", sent) # replace ..or words with ..our words (American versus British)
        sent = re.sub("([a-z]{2,})iz([eai])", r"\1is\2", sent) # replace ize with ise (..ise, ...isation, ..ising)
    if lang=="fr":
        replacements = [("keske", "qu' est -ce que"), ("estke", "est -ce que"), ("bcp", "beaucoup")] # etc.
        for (original, replacement) in replacements:
            sent = re.sub("(^| )"+original+"( |$)", r"\1"+replacement+r"\2", sent)
    return sent

def tokenise_en(sent):

    # deal with apostrophes
    sent = re.sub("([^ ])\'", r"\1 '", sent) # separate apostrophe from preceding word by a space if no space to left
    sent = re.sub(" \'", r" ' ", sent) # separate apostrophe from following word if a space if left

    # separate on punctuation by first adding a space before punctuation that should not be stuck to
    # the previous word and then splitting on whitespace everywhere
    cannot_precede = ["M", "Prof", "Sgt", "Lt", "Ltd", "co", "etc", "[A-Z]", "[Ii].e", "[eE].g"] #non-exhaustive list
                                        
    # creates a regex of the form (?:(?<!M)(?<!Prof)(?<!Sgt)...), i.e. whatever follows cannot be
    # preceded by one of these words (all punctuation that is not preceded by these words is to be
    # replaced by a space plus itself
    regex_cannot_precede = "(?:(?<!"+")(?<!".join(cannot_precede)+"))" 
    
    sent = re.sub(regex_cannot_precede+"([\.\,\;\:\)\(\"\?\!]( |$))", r" \1", sent)

    # then restick several consecutive fullstops ... or several ?? or !! by removing the space
    # inbetween them
    sent = re.sub("((^| )[\.\?\!]) ([\.\?\!]( |$))", r"\1\2", sent) 

    sent = sent.split() # split on whitespace
    return sent

def tokenise_fr(sent):

    # deal with apostrophes
    sent = re.sub("([^ ])\'", r" \1'", sent) # separate apostrophe from preceding word by a space if no space to left
    sent = re.sub(" \'", r" ' ", sent) # separate apostrophe from following word if a space if left

    # separate on punctuation by first adding a space before punctuation that should not be stuck to
    # the previous word and then splitting on whitespace everywhere
    cannot_precede = ["M", "Prof", "Sgt", "Lt", "Ltd", "co", "etc", "[A-Z]", "[Ii].e", "[eE].g"] #non-exhaustive list
                                        
    # creates a regex of the form (?:(?<!M)(?<!Prof)(?<!Sgt)...), i.e. whatever follows cannot be
    # preceded by one of these words (all punctuation that is not preceded by these words is to be
    # replaced by a space plus itself
    regex_cannot_precede = "(?:(?<!"+")(?<!".join(cannot_precede)+"))" 
    
    sent = re.sub(regex_cannot_precede+"([\.\,\;\:\)\(\"\?\!]( |$))", r" \1", sent)

    # then restick several consecutive fullstops ... or several ?? or !! by removing the space
    # inbetween them
    sent = re.sub("((^| )[\.\?\!]) ([\.\?\!]( |$))", r"\1\2", sent) 

    sent = sent.split() # split on whitespace
    return sent
    
 

def tokenise(sent, lang):
    if lang=="en":
        return tokenise_en(sent)
    elif lang=="fr":
        return tokenise_fr(sent)
    else:
        exit("Lang: "+str(lang)+" not recognised for tokenisation.\n")
        
        
def tok2count(sent, d):
	for w in sent:
		try :
			d[w] += 1
		except KeyError:
			d[w] = 1
	d["_UKN_"] = 1
	return d
	
def tok2logprobas(d):
	somme = 0
	for occurrence in d.values():
		somme += occurrence
	dictionnary = d.copy()
	for token in dictionnary.keys():
		dictionnary[token] = log((dictionnary[token]+1)/(somme+1))
	return dictionnary

def train_lm_unigram(texte):
	
	tokens = []
	for p in texte :
		parag = segment_into_sents(p)
		for s in parag :
			sent = tokenise(s, "en")
			for t in sent:
				tokens.append(t)
		
	
	dictionnary = {}
	dictionnary = tok2count(tokens, dictionnary)
	return tok2logprobas(dictionnary)
	
def test_lm_unigram(sent, d):
	s = tokenise(sent, "en")
	logproba = 0
	for tok in s :
		if tok in d:
			logproba += d.get(tok)
		else :
			logproba += d.get("_UKN_")
	return logproba
	
	
def bigramtok2logprobas(d):
	somme = 0
	for occurrence in d.values():
		somme += occurrence
	dictionnary = d.copy()
	for token in dictionnary.keys():
		dictionnary[token] = log((dictionnary[token]+1)/(somme+1))
	return dictionnary

def train_lm_bigram(texte):
	tokens = []
	for p in texte :
		parag = segment_into_sents(p)
		for s in parag :
			sent = tokenise(s, "en")
			sent.insert(0, "_BEGIN_")
			sent.append("_END_")
			for t in sent:
				tokens.append(t)
		
		

	
	
	dictionnary = {}
	tuples = []
	if len(tokens) == 0:
		tuples.append(("_BEGIN_", "_END_"))
	else:
		for i in range(0, len(tokens)-1):
			if tokens[i] != "_END_":
				tuples.append((tokens[i], tokens[i+1]))
		
	dictionnary = tok2count(tuples, dictionnary)
	return tok2logprobas(dictionnary)


def test_lm_bigram(sent, d):
	
	tuples = []
	s = tokenise(sent, "en")
	s.insert(0, "_BEGIN_")
	s.append("_END_")
	
	for i in range(0, len(s)-1):
		if sent[i] != "_END_":
			tuples.append((s[i], s[i+1]))
	
	
	logproba = 0
	for t in tuples:
		if t in d:
			logproba += d.get(t)
		else:
			logproba += d.get("_UKN_")
			
	return logproba


def rand_unigram(dictionnaire):
	liste = []
	somme = 0.0
	for i in range(0,10):
		r= random()
		for token in dictionnaire.keys():
			if somme + exp(dictionnaire.get(token)) > r and token != "_UKN_":
				liste.append(token)
				break;
			somme += exp(dictionnaire.get(token))
		somme = 0
				
	return liste
