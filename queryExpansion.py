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
import nltk
from nltk.corpus import wordnet
from autocorrect import spell
import wiki
diseaseToSymptomDict={}

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
neodbRest = GraphDatabase("http://localhost:7474", username="neo4j", password="123456")

symptomDescriptions ={}

dict_symptoms ={}

with open("dict_symptoms.json") as json_data:
    dict_symptoms = json.load(json_data)
    json_data.close()

with open("list_vocab.json") as json_data:
    list_vocab = json.load(json_data)
    
with open("list_fileNames.json") as json_data:
    list_fileNames = json.load(json_data)


with open("dict_wiki_desc.json") as json_data:
    symptomDescriptions = json.load(json_data)
    
    
rows, cols = len(list_vocab) , len(list_fileNames)
TFIDFMatrix = [[0 for x in range(cols)] for y in range(rows)] 


with open("TFIDFMatrix.json") as json_data:
    TFIDFMatrix = json.load(json_data)
    
QueryVector = [0]*len(list_vocab)


    
def cos_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)
    




def queryNeoDb(neodbRest):

    ###creating labels and nodes
    # user = neodbRest.labels.create("User")
    # u1 = neodbRest.nodes.create(name="Himanshu",age=28)
    # user.add(u1)


    ### matching symptoms with disease and returning
    # q = 'MATCH (d:DiseaseNew)-[:HAS_SYMPTOM]->(SymptomNew) RETURN d,SymptomNew'
    # # "db" as defined above
    # results = neodbRest.query(q, returns=(client.Node, client.Node))
    # print(results)
    # for r in results:
    #     # print(r)
    #     print("(%s)-[%s]->(%s)" % (r[0]["name"]," Has_Symptom ", r[1]["name"]))

    var1 ="'nausea'"
    q = 'MATCH (d:DiseaseNew)-[:HAS_SYMPTOM]->(SymptomNew) WHERE  SymptomNew.name = ' + var1 + ' RETURN d,SymptomNew'
    # "db" as defined above
    results = neodbRest.query(q, returns=(client.Node, client.Node))
    print(results)

    listDisease =[]
    for res1 in results:
        # print(r)
        print("(%s)-[%s]->(%s)" % (res1[0]["name"]," Has_Symptom ", res1[1]["name"]))

        listDisease.append(res1[0]["name"])



    print(listDisease)

    for dis in listDisease:
        var2 = "'"+ dis +"'"
        q2 = 'MATCH (d:DiseaseNew)-[:HAS_SYMPTOM]->(SymptomNew) WHERE  d.name = ' + var2 + ' AND SymptomNew.name <> '+ var1 + ' RETURN d,SymptomNew'
        results2 = neodbRest.query(q2, returns=(client.Node, client.Node))

        for res2 in results2:
            # print(r)
            print("(%s)-[%s]->(%s),  (%s)" % (res2[0]["name"], " Has_Symptom ", res2[1]["name"] , res2[1]["description"]))



def getRelatedDiseases(neodbRest,symp):
    var1 = "'" + symp + "'"

    print(var1)
    q = 'MATCH (d:DiseaseNew)-[:HAS_SYMPTOM]->(SymptomNew) WHERE  SymptomNew.uid = ' + var1 + ' RETURN d,SymptomNew'
    # "db" as defined above
    results = neodbRest.query(q, returns=(client.Node, client.Node))
    # print(results)

    listDisease = []
    for res1 in results:
        # print(r)
        print("(%s)-[%s]->(%s)" % (res1[0]["name"], " Has_Symptom ", res1[1]["name"]))

        listDisease.append(res1[0]["uid"])

    return listDisease


def getRelatedSymptoms(neodbRest,symp,listDisease):
    global diseaseToSymptomDict
    var1 = "'" + symp + "'"

    for dis in listDisease:
        var2 = "'"+ dis +"'"
        q2 = 'MATCH (d:DiseaseNew)-[:HAS_SYMPTOM]->(SymptomNew) WHERE  d.uid = ' + var2 + ' AND SymptomNew.uid <> '+ var1 + ' RETURN d,SymptomNew'
        results2 = neodbRest.query(q2, returns=(client.Node, client.Node))

        listSymp =[]
        for res2 in results2:
            # print(r)
            print("(%s)-[%s]->(%s, %s),  (%s)" % (res2[0]["name"], " Has_Symptom ", res2[1]["uid"] , res2[1]["name"],res2[1]["description"]))
            listSymp.append(res2[1]["uid"])

        if dis not in diseaseToSymptomDict:
            diseaseToSymptomDict[dis]=listSymp







def generateTFIDFforUserQuery(userQuery):
   corrected_list = []
   set_expandQuery = set()
   word_tokens = word_tokenize(userQuery)
   
   for token in word_tokens:
       corrected_list.append(spell(token))
       
   # print " ".join(corrected_list)
   set_expandQuery = set(preprocessing.fn_preprocessingtoken(" ".join(corrected_list)))
   
   for item in set_expandQuery:
       if item in list_vocab:
          QueryVector[list_vocab.index(item)]=1
   
   return QueryVector

    
    
def UserQuery(neodbRest):
    global diseaseToSymptomDict,symptomDescriptions
    ageGroup = ""
    age = input("Please enter your age group:(1:less than 10, 2: 10-50 , 3: 50 & above): ")
    if age=="1":
        ageGroup="child"
    if age=="2":
        ageGroup="adult"
    if age=="3":
        ageGroup="old"
        
    # print ("ageGroup",ageGroup  )
    gender = input("Please enter your gender(m/f): ")
    # print (gender)
    symptoms = input("Please enter the list of symptoms you are facing: ")
    queryVector = generateTFIDFforUserQuery(symptoms+" "+ageGroup+" "+gender)
    
    transposedTFIDF = np.transpose(TFIDFMatrix)
    list_cosineval = []
    
    for i in range(0,len(list_fileNames)):
        list_cosineval.append(cos_similarity(queryVector, transposedTFIDF[i]))

    listSymptoms =[]

    for index in range(2):
        ind = index +1
        listSymptoms.append(list_fileNames[list_cosineval.index(sorted(list_cosineval)[-ind])])
    
    item_index_1 = list_cosineval.index(sorted(list_cosineval)[-1])
    item_index_2 = list_cosineval.index(sorted(list_cosineval)[-2])
    item_index_3 = list_cosineval.index(sorted(list_cosineval)[-3])
    print (list_fileNames[item_index_1],wiki.getEntityLabel(list_fileNames[item_index_1]))
    print (list_fileNames[item_index_2],wiki.getEntityLabel(list_fileNames[item_index_2]))
    print (list_fileNames[item_index_3],wiki.getEntityLabel(list_fileNames[item_index_3]))


    print(listSymptoms)

    askedSympToDiseaseMapping ={}



    for symp in listSymptoms:
        listAllDisease =getRelatedDiseases(neodbRest,symp)
        askedSympToDiseaseMapping[symp]=listAllDisease
        print("===============================================================")
        getRelatedSymptoms(neodbRest,symp,listAllDisease)
        pass

    # print(askedSympToDiseaseMapping)
    print(diseaseToSymptomDict)

    import operator


    score = {}
    for key in diseaseToSymptomDict.keys():
        score[key] = 0

    # print("Are you having any symptoms similar to below:-")

    print("     ======================================================           ")
    print("     ======================================================           ")
    print("     ======================================================           ")
    for key in diseaseToSymptomDict.keys():
        count=0
        for val in diseaseToSymptomDict[key]:

            data = (symptomDescriptions[val])

            if (len(data.split(".")) < 2):
                print("Are you feeling somethinig like " + data.split(".")[0])
            else:

                fl = data.split(".")[0]
                toask = fl
                if "is " in data:
                    loc = fl.find("is ")
                    toask = (fl[loc + 3:])
                print("")
                val = input("Are you feeling something like " + dict_symptoms[diseaseToSymptomDict[key][count]]["name"] +" - " + toask + ". Answer 1 if yes, 0 if no.")
                if (val == "1"):
                    score[key] += 1
            count+=1
    score = sorted(score.items(), key=operator.itemgetter(1))
    print("You might be suffering from " + wiki.getEntityLabel(str(score[-2][0]))+ " or " + wiki.getEntityLabel(str(score[-1][0])))
          
UserQuery(neodbRest)

#generateTFIDFforUserQuery("diclonac soium salt nose child male")

