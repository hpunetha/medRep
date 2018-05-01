#TFIDF
import preprocessing
import codecs
import math
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sys 
import pickle
from nltk.stem import PorterStemmer
import json
import numpy as np



_list_vocab=[]
list_vocab=[]
list_fileNames=[]
dict_idf = {}


    
with open("list_vocab.json") as json_data:
    list_vocab = json.load(json_data)
    

with open("list_fileNames.json") as json_data:
    list_fileNames = json.load(json_data)

rows, cols = len(list_vocab) , len(list_fileNames)
TFMatrix = [[0 for x in range(cols)] for y in range(rows)] 
TFIDFMatrix = [[0 for x in range(cols)] for y in range(rows)] 


with open("TFMatrix.json") as json_data:
    TFMatrix = json.load(json_data)


#
#for files in os.walk("wikipedia_data/symptom/"):  
#        for filename in files[2]:
#            print filename 
#            list_fileNames.append(filename)
#with open('list_fileNames.json', 'w') as out:
#        json.dump(list_fileNames, out)
#

def calculateTF(term,list_token):
    tf = list_token.count(term)
    if tf>0:
        return 1+ math.log10(tf)
    else:
        return 0

            
def fn_createListVocabulary():
    for files in os.walk("wikipedia_data/symptom/"):  
        for filename in files[2]:
            print filename 
#            list_fileNames.append(filename)
            fileptr = codecs.open("wikipedia_data/symptom/"+filename,encoding= 'utf8', errors='ignore')
            content = fileptr.read();
            list_content = preprocessing.fn_preprocessingtoken(content)
            _list_vocab.extend(list_content)
            
    for i in _list_vocab:
        if i not in list_vocab:
            list_vocab.append(i)
            
    with open('list_vocab.json', 'w') as out:
        json.dump(list_vocab, out)
    
        
def createTFIDFMatrix():
    print "in createTFIDFMatrix"
    for j in range(0,cols):
        print "*********",j
#        print "Hello"
        fileptr = codecs.open("wikipedia_data/symptom/"+list_fileNames[j],encoding= 'utf8', errors='ignore')
        content = fileptr.read();
        list_tokens = preprocessing.fn_preprocessingtoken(content)
        for i in range(0,rows):
            TFMatrix[i][j] = calculateTF(list_vocab[i],list_tokens)
    
    for i in range(0,rows):
           df = np.count_nonzero(TFMatrix[i])
           print df
           idf = math.log10(len(list_fileNames)/df)
           for j in range(0,cols):
               TFIDFMatrix[i][j] = TFMatrix[i][j] * idf;        
    with open('TFMatrix.json', 'w') as out:
        json.dump(TFMatrix, out)
    
    with open('TFIDFMatrix.json', 'w') as out:
        json.dump(TFIDFMatrix, out)


def createIDF():
    for i in range(0,rows):
           df = np.count_nonzero(TFMatrix[i])
           print df
           dict_idf[list_vocab[i]]=df
    
    with open('dict_idf.json', 'w') as out:
        json.dump(dict_idf, out)
        
#createIDF()

createTFIDFMatrix()
            
#createTFIDFMatrix()
    
        
#fn_createListVocabulary()
 