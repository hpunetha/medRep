import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sys 
import codecs 
import pickle
from nltk.stem import PorterStemmer
import json
import string
import re
import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

def lemmaFunc(tokens):
    lemmaToks = []
    lemtr = WordNetLemmatizer()
    for val in tokens:
        stoken = lemtr.lemmatize(val)
        lemmaToks.append(stoken)

    return lemmaToks

def fn_preprocessingtoken(text): #Normalize with lowercase, stemming, tokonization , remove combinations of words and numbers, remove punctuations, remove header
    porterstemmer = PorterStemmer()
    text = text.lower()
    text = re.sub("\d","",text);
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    synonyms = []
    
    for token in word_tokens:
        for syn in wordnet.synsets(token):
            	for l in syn.lemmas():
            		synonyms.append(l.name())
                
    word_tokens.extend(synonyms)            
    filtered_text = []
    for w in word_tokens:
        if w not in stop_words:
                if w.isalnum():
                    filtered_text.append(w)  #porterstemmer.stem(w))
    return lemmaFunc(filtered_text)

def preprocessvocab(text): #Normalize with lowercase, stemming, tokonization , remove combinations of words and numbers, remove punctuations, remove header
    porterstemmer = PorterStemmer()
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    synonyms = []
    
    for token in word_tokens:
        for syn in wordnet.synsets(token):
            	for l in syn.lemmas():
            		synonyms.append(l.name())
                
    word_tokens.extend(synonyms)           
    filtered_text = set()
    for w in word_tokens:
        if w not in stop_words:
                if w.isalnum():
                    filtered_text.add(w)#porterstemmer.stem(w))
    return lemmaFunc(filtered_text)
