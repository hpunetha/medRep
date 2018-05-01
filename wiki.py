# -*- coding: utf-8 -*-
#Reference: Code is taken from Prateek Rawat
import requests

def getEntityLabel(entityId):
    #print(entityId)
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&props=labels&ids="+entityId+"&languages=en&format=json"
    r = requests.get(url)
    retrieved_data = r.json()
    if 'en' in retrieved_data['entities'][entityId]['labels']:
        return retrieved_data['entities'][entityId]['labels']['en']['value']
   

def getEntityDescription(entityId):
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+entityId+"&languages=en&format=json"
    r = requests.get(url)
    retrieved_data = r.json()
    if retrieved_data['entities'][entityId]['descriptions'].has_key('en'):
        return retrieved_data['entities'][entityId]['descriptions']['en']['value']

def getEntityDOID(entityId):
    #print(entityId)
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&props=labels&ids="+entityId+"&languages=en&format=json"
    r = requests.get(url)
    retrieved_data = r.json()
    return retrieved_data['entities'][entityId]['labels']['en']['value']


def getEntitySynonyms(entityId):
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+entityId+"&languages=en&format=json"
#    print url
    r = requests.get(url)
#    print "*********************************************"
    retrieved_data = r.json()
    if retrieved_data['entities'][entityId]['aliases'].has_key('en'):
        list_synonyms =  retrieved_data['entities'][entityId]['aliases']['en']
    else:
        list_synonyms=[]
#    print retrieved_data['entities'][entityId]['aliases']['en']['value']
#    print  [list_synonyms[i]['value'] for i in range(0,len(list_synonyms))]
    if not list_synonyms:
        return []
    else:
        return [list_synonyms[i]['value'].lower() for i in range(0,len(list_synonyms))]




def getRelationSetByStatement(entityId):
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+entityId+"&languages=en&format=json"
    r = requests.get(url)
#    print url
    retrieved_data = r.json()
    retrived_data_entities = retrieved_data['entities']
    main_entity = retrived_data_entities[entityId]
    claims = main_entity['claims']
    relation_dictionary = {}
    for claim in claims:
        claim_list = []
        for i in range(len(claims[claim])):
            try:
                if claim == "P486" or claim == "P2892" or claim=="P699":
                     claim_list.append(claims[claim][i]['mainsnak']['datavalue']['value'])
                else:
                    claim_list.append(claims[claim][i]['mainsnak']['datavalue']['value']['id'])
            except:
                pass
                #print('error')
        
        relation_dictionary[claim] = claim_list
        
        #get relation and values for the relations
        relation_dictionary = {k:v for k,v in relation_dictionary.items() if v != []}
    return relation_dictionary



def getRelationSetByOntologyName(entityId):
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+entityId+"&languages=en&format=json"
#    print url
    r = requests.get(url)
    retrieved_data = r.json()
    retrived_data_entities = retrieved_data['entities']
    main_entity = retrived_data_entities[entityId]
    print (main_entity['claims'])
    claims = main_entity['identifiers']
    
    relation_dictionary = {}
    for claim in claims:
        claim_list = []
        for i in range(len(claims[claim])):
            try:
                claim_list.append(claims[claim][i]['mainsnak']['datavalue']['value']['id'])
            except:
                pass
                #print('error')
        relation_dictionary[claim] = claim_list
        
        #get relation and values for the relations
        relation_dictionary = {k:v for k,v in relation_dictionary.items() if v != []}
    return relation_dictionary




def getEntityId(entityName):
    try:
        entityName = entityName.replace("_","+")
        url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+entityName+"&language=en&format=json"
        r = requests.get(url)
        prelimnary_data = r.json()
        
        #search results
        search_data = prelimnary_data['search']
        
        #taking first result
        entity = search_data[0]
        
        #getting basic data
        entityId = entity['id']
        return entityId
    except:
        return None
    
#    



#symptomsLabels = [getEntityLabel(_id) for _id in symptomsId]
#symptomsDesc = [getEntityDescription(_id) for _id in symptomsId]

#uid = 'Q755524'
#    name = getEntityLabel(uid)
#print getEntityDescription(uid)
#    relationSet = getRelationSetByStatement(uid)
#    has_cause = relationSet['P828']
#    symptomsId = relationSet['P780']
#    synonyms = getEntitySynonyms(uid)
#    treatment = relationSet['P2176']
#    subclass = relationSet['P279']
#    relationSet = getRelationSetByOntologyName(uid)

#print getEntityLabel("Q12125")
#
#uid = 'Q12125'
#relationSet = getRelationSetByStatement(uid)

#print getEntityLabel('Q194041')



