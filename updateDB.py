from collections import defaultdict
from neo4j.v1 import GraphDatabase
import json



import collections

dict_symtokens={}

dict_wikides={}

dict_doid={}
synonymDict = defaultdict(list)

uri = 'bolt://localhost:7687'
user = "neo4j"
pass1 = "123456"


def openJson():
    global dict_symtokens,dict_wikides,dict_doid
    with open("dict_stemmed_tokens.json") as json_data:
        dict_symtokens = json.load(json_data)
        json_data.close()

    with open("dict_wiki_desc.json") as json_data:
        dict_wikides = json.load(json_data)
        json_data.close()

    # with open("doid.json") as json_data:
    #     temp_dict_doid = json.load(json_data)
    #     dict_doid = temp_dict_doid['graphs']
    #     json_data.close()


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


    def add_symptom_description(self, uid, wikidesc, wikitokens):
        with self._driver.session() as session:
            symp = session.write_transaction(self._add_symptom_description, uid, wikidesc, wikitokens)
            # print(symp)

    @staticmethod
    def _add_symptom_description(transaction, uid, wikidesc, wikitokens):
        result = transaction.run("Match (s:SymptomNew) "
                                 "where s.uid=$uid "
                                 "SET s.wikidescription=$wikidesc , s.wikitokens =$wikitokens "
                                 "RETURN s.name ",
                                 uid=uid,wikidesc=wikidesc,wikitokens=wikitokens)

        return result.single()[0]


def startProcessingSymptoms(dbObj):
    global dict_symtokens, dict_wikides

    for uid in dict_symtokens:
        print(uid,dict_symtokens[uid],dict_wikides[uid])

        dbObj.add_symptom_description(uid, dict_wikides[uid], dict_symtokens[uid])

    pass


def startAllNeoProcessing(dbObj):

    # startProcessingSymptoms(dbObj)

    pass




openJson()
dbObj = Neo4JClass(uri, user, pass1)
startAllNeoProcessing(dbObj)


