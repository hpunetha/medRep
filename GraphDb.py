from collections import defaultdict
from neo4j.v1 import GraphDatabase
import json



import collections

dict_disease={}

dict_symptoms={}

dict_doid={}
synonymDict = defaultdict(list)

uri = 'bolt://localhost:7687'
user = "neo4j"
pass1 = "123456"


def openJson():
    global dict_disease,dict_symptoms,dict_doid
    with open("dict_disease.json") as json_data:
        dict_disease = json.load(json_data)
        json_data.close()

    with open("dict_symptoms.json") as json_data:
        dict_symptoms = json.load(json_data)
        json_data.close()

    with open("doid.json") as json_data:
        temp_dict_doid = json.load(json_data)
        dict_doid = temp_dict_doid['graphs']
        json_data.close()


def flattenlist(nonfllist):
    for val in nonfllist:
        if not isinstance(val, (str,bytes)) and isinstance(val , collections.Iterable):
            yield from flattenlist(val)
        else:
            yield val


class Neo4JClass(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Disease) "
                        "SET a.name = $message "
                        "RETURN a.name + ', from node ' + id(a)", message=message)
        return result.single()[0]

    def print_disease(self, diseasename, type, uid, description, has_cause, dclass, symptom, synonyms, drugs, doid,
                      umls, mesh,subclass_of):
        with self._driver.session() as session:
            disease = session.write_transaction(self._create_return_disease, diseasename, type, uid, description,
                                                has_cause, dclass, symptom, synonyms, drugs, doid, umls, mesh,subclass_of)
            # print(disease)

    @staticmethod
    def _create_return_disease(transaction, diseasename, type, uid, description, has_cause, dclass, symptom, synonyms,
                               drugs, doid, umls, mesh, subclass_of):
        result = transaction.run("CREATE (d:DiseaseNew) "
                                 "SET d.name = $name , d.type = $type , d.uid =$uid , d.description =$description , "
                                 "d.has_cause=$has_cause , d.dclass = $dclass , d.symptom=$symptom , d.synonyms = "
                                 "$synonyms , d.drugs=$drugs , d.doid=$doid , d.umls = $umls , d.mesh=$mesh ,"
                                 " d.subclass_of=$subclass_of "
                                 "RETURN d.name + ', from node ' + id(d)", name=diseasename, type=type, uid=uid,
                                 description=description, has_cause=has_cause, dclass=dclass, symptom=symptom,
                                 synonyms=synonyms, drugs=drugs, doid=doid, umls=umls, mesh=mesh,
                                 subclass_of=subclass_of)
        return result.single()[0]

    def print_disease_synonym(self, diseasename, dclass,dtype):
        with self._driver.session() as session:
            disease = session.write_transaction(self._create_return_disease_synonym, diseasename,dclass,dtype)
            # print(disease)

    @staticmethod
    def _create_return_disease_synonym(transaction, diseasename, dclass,dtype):
        result = transaction.run("CREATE (d:SynonymNew) "
                                 "SET d.name = $name , d.dclass = $dclass , d.type = $dtype "
                                 " RETURN d.name + ', from node ' + id(d)", name=diseasename,dclass=dclass,dtype=dtype)

        return result.single()[0]

    def print_symptom(self, name, uid,causes,desc,umls,mesh):
        with self._driver.session() as session:
            symp = session.write_transaction(self._create_return_symptom,name,uid,causes,desc,umls,mesh)
            # print(symp)

    @staticmethod
    def _create_return_symptom(transaction, name,uid,causes,desc,umls,mesh):
        result = transaction.run("CREATE (d:SymptomNew) "
                                 "SET d.name = $name , d.uid = $uid , d.causes =$causes , d.description=$desc , "
                                 "d.umls = $umls , d.mesh=$mesh "
                                 "RETURN d.name + ', from node ' + id(d)",
                                 name=name,uid=uid,causes=causes,desc=desc,umls=umls,mesh=mesh)

        return result.single()[0]

    def create_dis_sym_relation(self):
        with self._driver.session() as session:
            relations = session.write_transaction(self._create_return_relation)

            return relations

    @staticmethod
    def _create_return_relation(transaction):
        result = transaction.run("MATCH (s:SymptomNew),(d:DiseaseNew) "
                                 "where  s.name in d.symptom create (d)-[r:HAS_SYMPTOM]->(s) "
                                 "RETURN d,s")

        return result

    def create_dis_synonyms_relation(self):
        with self._driver.session() as session:
            relations = session.write_transaction(self._create_return_synonymrelation)

            return relations

    @staticmethod
    def _create_return_synonymrelation(transaction):
        result = transaction.run("MATCH (s:SynonymNew),(d:DiseaseNew) "
                                 "where  s.dclass in d.dclass create (d)-[r:HAS_SYNONYM]->(s) "
                                 "RETURN d,s")

        return result


def startProcessingDiseases(dbObj):
    global dict_disease
    global synonymDict

    for uid in dict_disease:
        try:
            # print(uid,dict_disease[uid])

            # for keys in dict_disease[uid]:
            #     print(keys)
            # print( dict_disease[uid]['name'])
            diseasename = dict_disease[uid]['name']
            dtype = dict_disease[uid]['type']
            if 'description' in dict_disease[uid]:
                description = dict_disease[uid]['description']
            else:
                description=""
            has_cause = dict_disease[uid]['caused_by']  #dict
            dclass = dict_disease[uid]['diseaseclass']
            symptom = dict_disease[uid]['symptoms']   #dict
            synonyms = dict_disease[uid]['synonyms']  #list
            drugs = dict_disease[uid]['treatment']  #dict
            doid = dict_disease[uid]['doid']
            umls =dict_disease[uid]['umls']
            mesh = dict_disease[uid]['mesh']
            subclass_of = dict_disease[uid]['subclass']
            newhas_cause=[]
            if not bool(has_cause):
                pass
            else:
                for viruskey in has_cause:
                    newhas_cause.append(has_cause[viruskey])

            newsymptom = []
            if not bool(symptom):
                pass
            else:
                for sympkey in symptom:
                    newsymptom.append([symptom[sympkey]])

            newdrugs = []
            if not bool(drugs):
                pass
            else:
                for dkey in drugs:
                    newdrugs.append([drugs[dkey]])

            newsubclassof =[]
            if not bool(subclass_of):
                pass
            else:
                for dkey in subclass_of:
                    newsubclassof.append([subclass_of[dkey]])

            # print(has_cause,dclass,symptom,synonyms,drugs,doid,umls,mesh)
            # flatten all lists
            flatsubclassof = list(flattenlist(newsubclassof))
            flathas_cause = list(flattenlist(newhas_cause))
            flatnewsymptom = list(flattenlist(newsymptom))
            flatsynonyms = list(flattenlist(synonyms))
            flatnewdrugs = list(flattenlist(newdrugs))

            # Create Disease Nodes
            # dbObj.print_disease(diseasename, dtype, uid, description, flathas_cause, dclass, flatnewsymptom, flatsynonyms,
            #                     flatnewdrugs, doid,
            #                     umls, mesh, flatsubclassof)



            # print(uid,synonyms)


            for a in synonyms:
                dtype="synonym"
                # print(a,dclass,dtype)
                synonymDict[a].append(dclass)




        ###############OLD CODE
            ##in string form
            # # Convert flat lists to string
            # strhas_cause = ', '.join(flathas_cause)
            # strnew_symptom = ', '.join(flatnewsymptom)
            # strsynonyms = ', '.join(flatsynonyms)
            # strnewdrugs = ', '.join(flatnewdrugs)
            # strnewsubclassof = ', '.join(flatsubclassof)
            # dbObj.print_disease(diseasename, dtype, uid, description, strhas_cause, dclass, strnew_symptom, strsynonyms, strnewdrugs, doid,
            #               umls, mesh,strnewsubclassof)
        ###########################

        except:
            import traceback

            # traceback.print_exc()
            print("Error Occured for =>",uid)
            continue

    print(synonymDict)


def startProcessingSymptoms(dbObj):
    global dict_symptoms

    for uid in dict_symptoms:
        print(uid,dict_symptoms[uid])
        name = dict_symptoms[uid]['name']
        causes = dict_symptoms[uid]['d_class']
        description=dict_symptoms[uid]['description']
        umls =dict_symptoms[uid]['umls']
        mesh = dict_symptoms[uid]['mesh']
        dbObj. print_symptom(name, uid,causes,description,umls,mesh)

    pass


def startProcessingSynonyms(dbObj):
    global synonymDict
    for a in synonymDict:
        print(a,synonymDict[a])

        dbObj.print_disease_synonym(a,synonymDict[a],"synonym")

    dbObj.create_dis_synonyms_relation()

    pass


def startAllNeoProcessing(dbObj):
    startProcessingDiseases(dbObj)
    # startProcessingSymptoms(dbObj)
    # boltObj = dbObj.create_dis_sym_relation()
    # print(boltObj)
    startProcessingSynonyms(dbObj)

    pass



def startDoidProcessing(dbObj):
    global dict_doid


    for nodeslist in dict_doid:


        pass



openJson()
dbObj = Neo4JClass(uri, user, pass1)
# startAllNeoProcessing(dbObj)





#print(dict_doid)
#startDoidProcessing(dbObj)
