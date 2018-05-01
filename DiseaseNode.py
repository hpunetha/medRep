import wiki
import pickle
import json


flist_diseaseNames = open("list_diseaseNames.pkl",'r')
list_diseaseNames = pickle.load(flist_diseaseNames)

dict_disease = {}
dict_symptoms = {}
def create_diseaseNode(uid,d_class):   
    print wiki.getEntityLabel(uid)
    _temp_diseaseAttributes = {}
    name = wiki.getEntityLabel(uid)
    description = wiki.getEntityDescription(uid)
    relationSet = wiki.getRelationSetByStatement(uid)
    caused_by={}
    symptoms={}
    synonyms = wiki.getEntitySynonyms(uid)
    treatment={}
    subclass={}
     
    if relationSet.has_key('P828'):         
        _caused_by = relationSet['P828']
        for i in range(0,len(_caused_by)):       
            caused_by[_caused_by[i]] = wiki.getEntityLabel(_caused_by[i]).lower()
            
    if relationSet.has_key('P780'):      
        symptomsId = relationSet['P780']
        for i in range(0,len(symptomsId)):       
            symptoms[symptomsId[i]] = wiki.getEntityLabel(symptomsId[i]).lower()
    
    if relationSet.has_key('P2176'):      
        _treatment = relationSet['P2176']
        for i in range(0,len(_treatment)):       
            treatment[_treatment[i]] = wiki.getEntityLabel(_treatment[i]).lower()
     
    
    if relationSet.has_key('P279'):      
        _subclass = relationSet['P279']
        for i in range(0,len(_subclass)):       
            subclass[_subclass[i]] = wiki.getEntityLabel(_subclass[i]).lower()  
            
    if relationSet.has_key('P699'):  
        doid=relationSet['P699'];
    else:
        doid = ""
    if relationSet.has_key('P2892'):  
        umls=relationSet['P2892']
    else:
        umls=""
    if relationSet.has_key('P486'):     
        mesh=relationSet['P486']
    else:
        mesh=""
    _temp_diseaseAttributes["name"]=name.lower();
    if description!=None:
        _temp_diseaseAttributes["description"]=description.lower();
    _temp_diseaseAttributes["caused_by"]=caused_by;
    _temp_diseaseAttributes["symptoms"]=symptoms;
    _temp_diseaseAttributes["synonyms"] = synonyms;
    _temp_diseaseAttributes["treatment"] = treatment;
    _temp_diseaseAttributes["subclass"] = subclass;
    _temp_diseaseAttributes["type"]="disease";
    _temp_diseaseAttributes["diseaseclass"]=d_class;
    _temp_diseaseAttributes["doid"]=doid;
    _temp_diseaseAttributes["umls"]=umls;
    _temp_diseaseAttributes["mesh"]=mesh;
    dict_disease[uid]=_temp_diseaseAttributes
    
    
def create_disease_dictonary():
    print "hello"  
    count =0 
    for i in range(0,len(list_diseaseNames)):
        count= count+1
        print count
        diseaseID = wiki.getEntityId(list_diseaseNames[i])
        if diseaseID != None:
            create_diseaseNode(diseaseID,"dclass_"+str(i))
        
    with open("dict_disease.json", 'w') as out:
        json.dump(dict_disease,out)
        
    with open('dict_symptoms.pkl', 'wb') as f:
       pickle.dump(dict_symptoms, f) 
    
#    
#diseaseid ='Q12125'
#create_diseaseNode(diseaseid)

create_disease_dictonary()


#fpickle_dict_disease = open("pickle_dict_disease.pkl",'r')
#dict_disease = pickle.load(fpickle_dict_disease)
#print dict_disease



