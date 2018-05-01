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
import preprocessing
import numpy as np

#create 3 dictonary
dict_wiki_desc = {}
dict_stemmed_tokens = {}
dict_symptoms_TFIDF = {}
list_vocab = []
list_fileNames = []



with open("list_vocab.json") as json_data:
    list_vocab = json.load(json_data)
    
with open("list_fileNames.json") as json_data:
    list_fileNames = json.load(json_data)
    
    
rows, cols = len(list_vocab) , len(list_fileNames)
TFIDFMatrix = [[0 for x in range(cols)] for y in range(rows)] 

transposedTFIDF = np.transpose(TFIDFMatrix)


with open("TFIDFMatrix.json") as json_data:
    TFIDFMatrix = json.load(json_data)

def create_dict_wiki_desc():
    for files in os.walk("wikipedia_data/symptom/"):  
            for filename in files[2]:
                print filename 
                fileptr = codecs.open("wikipedia_data/symptom/"+filename,encoding= 'utf8', errors='ignore')
                content = fileptr.read();
                dict_wiki_desc[filename]=content
    with open('dict_wiki_desc.json', 'w') as out:
        json.dump(dict_wiki_desc, out)
        
        
def create_dict_stemmed_tokens():
    for files in os.walk("wikipedia_data/symptom/"):  
            for filename in files[2]:
                print filename 
                fileptr = codecs.open("wikipedia_data/symptom/"+filename,encoding= 'utf8', errors='ignore')
                content = fileptr.read();
                dict_stemmed_tokens[filename]=preprocessing.fn_preprocessingtoken(content)
    with open('dict_stemmed_tokens.json', 'w') as out:
        json.dump(dict_stemmed_tokens, out)
        

    
    
        
#create_dict_stemmed_tokens()
#create_dict_wiki_desc()
create_dict_stemmed_tokens()
