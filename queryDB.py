
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
neodbRest = GraphDatabase("http://localhost:7474", username="neo4j", password="123456")




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


queryNeoDb(neodbRest)