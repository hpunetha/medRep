import wiki
import pickle
import json

dict_symptoms = {}


flist_diseaseNames = open("list_diseaseNames.pkl",'r')
list_diseaseNames = pickle.load(flist_diseaseNames)


def create_symptomNode(uid,d_class):
    relationSet = wiki.getRelationSetByStatement(uid)
    if relationSet.has_key('P780'):      
        symptomsId = relationSet['P780']
        for i in symptomsId:
            if dict_symptoms.has_key(i):
                dict_symptoms[i]["d_class"].append(d_class)
            else:
                dict_symptoms[i]={}
                dict_symptoms[i]["name"]=wiki.getEntityLabel(i).lower()
                if wiki.getEntityDescription(i)!=None:
                    dict_symptoms[i]["description"]=wiki.getEntityDescription(i).lower()
                else:
                    dict_symptoms[i]["description"]=""
                dict_symptoms[i]["d_class"]=[d_class]
                
                if relationSet.has_key('P2892'):  
                    umls=relationSet['P2892']
                else:
                    umls=""
                if relationSet.has_key('P486'):     
                    mesh=relationSet['P486']
                else:
                    mesh=""
                dict_symptoms[i]["umls"]=umls
                dict_symptoms[i]["mesh"]=mesh
    



def create_symptom_dictonary():
    print "hello"  
    count=0
    for i in range(0,len(list_diseaseNames)):
        count= count+1
        print count
        diseaseID = wiki.getEntityId(list_diseaseNames[i])
        if diseaseID != None:
            create_symptomNode(diseaseID,"dclass_"+str(i))
        
    with open("dict_symptoms.json", 'w') as out:
        json.dump(dict_symptoms,out)
        
create_symptom_dictonary()
       
       
       
#create_symptom_dictonary()
    