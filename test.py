import argparse
import math
import pandas as pd

# read the tagged data and return a list of (tok, tag) tuples
def read_data(tagged_file):
    data = []
    with open(tagged_file, encoding="utf8", errors="ignore") as fp:
        for line in fp:
            seq = line.strip().split(" ")
            seq = [("TOKBEGIN", "TAGBEGIN")] + [tuple(t.split("|")) for t in seq] + [("TOKEND", "TAGEND")]
            data.append(seq)
    return data


# divide the data into train, dev and test w/ a 70:15:15 split
def divide_data(data):
    size = len(data)
    train = data[0:int(size*0.7)]
    dev = data[int(size*0.7)+1:int(size*0.7)+int(size*0.15)+1]
    test = data[int(size*0.7)+int(size*0.15)+2:]
    return train, dev, test


# get the tagset from training data (set of possible tags)
def get_tagset(train):
    tagset = set([])
    for example in train:
        for tok, tag in example:
            tagset.add(tag)
    return tagset


# get the vocab from training data (set of possible tokens)
def get_vocab(train):
    vocab = set([])
    for example in train:
        for tok, tag in example:
            vocab.add(tok)
    return vocab


# calculate word/tag occurrences
def calculate_occ_emission(train, vocab, tagset, smoothing):
    # initialise counts (each word appears each 1*smoothing with each tag)
    tag2tok2occs = {}
    for tag in tagset:
        tag2tok2occs[tag] = {}
        if tag=="TAGBEGIN": tag2tok2occs[tag]["TOKBEGIN"] = smoothing
        elif tag=="TAGEND": tag2tok2occs[tag]["TOKEND"] = smoothing
        else:
            for word in vocab: tag2tok2occs[tag][word] = smoothing
        
    # go through training data and count tag/tok occurrences
    for example in train:
        for token, tag in example:
            tag2tok2occs[tag][token] += 1
            
    return tag2tok2occs


# calculate log p(tok|tag) for each tok/tag pair
def calculate_logprobas_emission(train, vocab, tagset, smoothing):
    tag2tok2occs = calculate_occ_emission(train, vocab, tagset, smoothing) # get counts
    
    # calculate log probas
    tag2tok2logprobas = {}
    for tag in tag2tok2occs:
        tag2tok2logprobas[tag] = {}
        # denominator includes 1 occurrence of smoothing value for the "unknown word"
        denominator = sum([tag2tok2occs[tag][t] for t in tag2tok2occs[tag]]) + smoothing
        for token in tag2tok2occs[tag]:
            tag2tok2logprobas[tag][token] = math.log(tag2tok2occs[tag][token] / float(denominator))
        tag2tok2logprobas[tag]["$UNK$"] = math.log(1/float(denominator)) # special token for unknown words
        
    return tag2tok2logprobas


# calculate occurrence counts for each tag/previous_tag pair
def calculate_occ_transition(train, tagset, smoothing):    
    # initialise
    tag2tag2occs = {}
    for tag in tagset:
        tag2tag2occs[tag] = {}
        for nexttag in tagset:
            if nexttag=="TAGBEGIN": continue # special token can only be at beginning
            tag2tag2occs[tag][nexttag] = smoothing

    # calculate occurrences
    for example in train:
        for t, (tok, tag) in enumerate(example):
            if t == len(example)-1: break # do not go beyond end of sentence
            nexttag = example[t+1][1]
            tag2tag2occs[tag][nexttag] += 1
    return tag2tag2occs


# calculate log p(tag|previous_tag) for each tag/previous_tag pair
def calculate_logprobas_transition(train, tagset, smoothing):
    tag2tag2occs = calculate_occ_transition(train, tagset, smoothing) # get counts
    # calculate log probas
    tag2tag2logprobas = {}
    for tag in tag2tag2occs:
        tag2tag2logprobas[tag] = {}
        denominator = sum([tag2tag2occs[tag][nexttag] for nexttag in tag2tag2occs[tag]]) + smoothing
        for nexttag in tag2tag2occs[tag]:
            tag2tag2logprobas[tag][nexttag] = math.log(tag2tag2occs[tag][nexttag] / float(denominator))
    return tag2tag2logprobas


# use the viterbi algorithm to decode a sequence
def viterbi(logprobas_emission, logprobas_transition, tagset, toks):

    logprobas = {0: {"TAGBEGIN" : math.log(1)}} # initialise trellis
    backpointers = {} # initialise backpointers
    
    for t, tok in enumerate(toks):
        if t == 0: continue # skip first token (BEGIN)
        logprobas[t], backpointers[t] = {}, {}
        
        for tag in tagset:
            if tag == "TAGBEGIN": continue # can only appear at beginning
            elif t == len(toks)-1 and tag!="TAGEND": continue # only tag possible in last position
            elif t < len(toks)-1 and tag=="TAGEND": continue # can only appear at end
            
            for prev_tag in logprobas[t-1]:
                logp = logprobas[t-1][prev_tag] # log proba of previous sequence
                logp += logprobas_transition[prev_tag][tag] # transition proba
                if tok in logprobas_emission[tag]: logp += logprobas_emission[tag][tok] # emission proba
                else: logp += logprobas_emission[tag]["$UNK$"] # emission proba for unknown words

                # update best log proba and the previous tag giving this log proba
                if tag not in logprobas[t] or logp >logprobas[t][tag]:
                    logprobas[t][tag] = logp
                    backpointers[t][tag] = prev_tag

    # reconstruct a tag sequence using backpointers from the end to the beginning
    idx = len(toks)-1 # start at penultimate token position
    seq = ["TAGEND"] # put last token in

    # go back from sequence end until at the sequence beginning
    while "TAGBEGIN" not in seq:
        seq.append(backpointers[idx][seq[-1]]) 
        idx -= 1

    return list(reversed(seq)) # return reversed list

# decode a dataset and return lists of gold and predicted sequences
def decode_set(logprobas_emission, logprobas_transition, tagset, dataset):
    correct, total = 0, 0
    allygold, allypred = [], []
    
    for example in dataset:
        toks = [x[0] for x in example] # list of toks
        goldtags = [x[1] for x in example] # list of gold tags
        predtags = viterbi(logprobas_emission, logprobas_transition, tagset,toks) # list of pred tags

        # construct 2 lists (of gold and corresponding pred tags)
        for goldtag, predtag in zip(goldtags, predtags):
            if goldtag in ["TAGBEGIN", "TAGEND"]: continue # skip the special tags
            allygold.append(goldtag)
            allypred.append(predtag)
            
    return allygold, allypred
    
# evaluate precision of a tagger by comparing gold and pred labels        
def evaluate(ygold, ypred, show_confusion_matrix=False):
    # check that there are the same number of predictions as gold tags
    assert(len(ygold) == len(ypred))

    # calculate number correctly tagged and total number of tags
    numcorrect = len([ y for y, gold in enumerate(ygold) if ypred[y] == gold ])
    totalnum = len(ygold)

    # show the confusion matrix of predicted versus gold tags
    if show_confusion_matrix:
        cm = pd.crosstab(pd.Series(ygold), pd.Series(ypred))
        print(cm.to_string())

    return numcorrect/float(totalnum) # return precision
      
        
if __name__=="__main__":

    # Read the data, divide into three sets and get vocab and tagset
    data = read_data("sequoia.tagged")
    train, dev, test = divide_data(data)
    vocab = get_vocab(train)
    tagset = get_tagset(train)

    # Train the model, i.e. estimate the model's probabilities on the training set
    # The smoothing value for emission probas can be different from the smoothing
    # value for transition probas. Choose the values that give the highest precision
    # on the development set (manually or by an exhaustive search).
    logprobas_emission = calculate_logprobas_emission(train, vocab, tagset, 0.1)
    logprobas_transition = calculate_logprobas_transition(train, tagset, 0.15)

    # Decode the development set (to tune the 2 smoothing hyperparameters above)
    ygolds, ypreds = decode_set(logprobas_emission, logprobas_transition, tagset, dev)
    precisiondev = evaluate(ygolds, ypreds)
    print("Precision on dev set = "+str(precisiondev)+"\n")

    # Once hyperparameters are tuned test and evaluate the model on the test set
    ygolds, ypreds = decode_set(logprobas_emission, logprobas_transition, tagset, test)
    precisiontest = evaluate(ygolds, ypreds, True)
    print("Precision on test set = "+str(precisiontest)+"\n")

    
