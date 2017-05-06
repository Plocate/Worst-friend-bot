# -*- coding: utf-8 -*-
"""
Created on Fri May  5 19:19:20 2017

@author: A_Tlos
"""
"""
from textblob import TextBlob
from textblob.en import parse as pattern_parse
from textblob.base import BaseParser

sentence = "The cat is dead and alive"

b = TextBlob(sentence)
print(pattern_parse(sentence, relations=True))
"""

import spacy
#noun_chunks requires the dependency parse, which requires data to be installed 
#If you haven't done so, run: 
#python -m spacy download en 
#to install the data
nlp = spacy.load('en')
sentence = "They told us to duck."
sentence = nlp(u"%s"%(sentence,))

for np in sentence.noun_chunks:
    print(np.text, np.root.text, np.root.dep_, np.root.head.text)

print()

doc = nlp(u'They told us to duck.')
for word in doc:
    print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)