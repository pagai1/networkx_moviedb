#!/usr/bin/python
import csv
import networkx as nx
import matplotlib.pyplot as plt
import time
import sys
import json
import os

# import own helper-modules
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),"../../networkx_modules")))
from helpers.generalStuff import *
from helpers.networkx_load_n_save import *
from algoPackage.pageRank import *

from builtins import len
from networkx.algorithms.coloring.greedy_coloring_with_interchange import Node
from networkx.classes.function import get_node_attributes
from networkx.readwrite import json_graph
from _operator import itemgetter
from xlwt.ExcelFormulaLexer import false_pattern
from cairosvg.helpers import distance


def getNodeCount(graph):
    nodecount = 0
    for node in G.nodes.items():
        nodecount = nodecount + 1
    return nodecount

def get_hits(G):
    for bums in nx.hits(G,max_iter=500,normalized=True):
        for bla in bums:
            print(str(bla) + "\n")
    
def get_column_names(filereader):
  headers = next(filereader, None)
  return headers

def remove_doubles(inputlist):
    return list(set(inputlist))

def draw_graph(Graph):
    """ Draws the graph """
    nx.draw(Graph, with_labels=True)
    #plt.plot()
    plt.show()


def all_pairs_shortest_path(G):
    actor_list=[x for x,y in G.nodes(data=True) if y['label'] == 'ACTOR']
#===============================================================================
# subgraph Returns a SubGraph view of the subgraph induced on nodes.
# The induced subgraph of the graph contains the nodes in nodes and the edges between those nodes.
#===============================================================================
    algoTime=time.time()
    subG = G.subgraph(actor_list)
    numberOfActors = len(actor_list)
    paths = nx.all_pairs_shortest_path(subG)
#    for path in paths:
#        print(path) 
    print("RUNTIME AllPairsShortestPath - " +  str(limit) + " entries - " + str(numberOfActors) + " actors : " + to_ms((time.time() - algoTime)) + "s.")

def algo_betweenness_centrality(G):
    actor_list=[x for x,y in G.nodes(data=True) if y['label'] == 'ACTOR']
    subG = G.subgraph(actor_list)
    dict_nodes = []
    algoTime = algoTime=time.time()
    dict_nodes = nx.betweenness_centrality(G,normalized=False);
    print("RUNTIME BetweennessCentrality - " +  str(limit) + " entries - " + to_ms((time.time() - algoTime)) + "s.")   
    print("Result:")
    for bums in dict(sorted(dict_nodes.items(), key=lambda item: item[1])):
        print(bums,dict_nodes[bums])
#    print("RUNTIME ClosenessCentrality - " +  str(limit) + " entries - " + str(len(actor_list)) + " actors : " + to_ms((time.time() - algoTime)) + "s.")


def algo_degree_centrality(G):
    algoTime = algoTime=time.time()
    actor_list=[x for x,y in G.nodes(data=True) if y['label'] == 'ACTOR']
    subG = G.subgraph(actor_list)
    dict_nodes = []
    dict_nodes = nx.degree_centrality(subG);
    print("Result:")
    for bums in dict(sorted(dict_nodes.items(), key=lambda item: item[1])):
        print(bums,dict_nodes[bums])
#    print("RUNTIME ClosenessCentrality - " +  str(limit) + " entries - " + str(len(actor_list)) + " actors : " + to_ms((time.time() - algoTime)) + "s.")
    print("RUNTIME ClosenessCentrality - " +  str(limit) + " entries - " + to_ms((time.time() - algoTime)) + "s.")   
   

def algo_shortest_path(G):
    actor_list=[x for x,y in G.nodes(data=True) if y['label'] == 'ACTOR']
#===============================================================================
# subgraph Returns a SubGraph view of the subgraph induced on nodes.
# The induced subgraph of the graph contains the nodes in nodes and the edges between those nodes.
#===============================================================================
    subG = G.subgraph(actor_list)
#    for actor in actor_list:
#        print(actor)
    numberOfActors = len(actor_list)
#    print("FOUND " + str(numberOfActors) + " ACTORS." )
    algoTime=time.time()
    #Lahm
#    for actor in actor_list:
#       #print("Example: Calculating shortest paths from " + actor + " to anyone...\r")
#        for actor2 in actor_list:
#            if (actor != actor2):
#                try:
#                    path = nx.shortest_path(subG, source=(actor), target=actor2)
#                except nx.NetworkXNoPath as e:
#                    path = e
#                except nx.NodeNotFound as e:
#                    path = e
    ### schnell
    for i in range(numberOfActors):
        actor = actor_list[i]
        #print("STARTNODE: " + actor)
        j = i + 1
        while j < numberOfActors:
            actor2 = actor_list[j]
         #   print(actor2)
            try:
                path = nx.shortest_path(subG, source=(actor), target=actor2)
            except nx.NetworkXNoPath as e:
                path = e
            except nx.NodeNotFound as e:
                path = e
            #print(path)
            j = j + 1 
    #print("RUNTIME : " + str(time.time() - start_time) )
    #     print(path)
    print("RUNTIME ShortestPath - " +  str(limit) + " entries - " + str(numberOfActors) + " actors : " + to_ms(time.time() - algoTime) + "s.")


#def algo_pagerank(G):
#   print("Calculating pagerank")
#    actor_list=[x for x,y in G.nodes(data=True) if y['type'] == 'actor']
#    subG = G.subgraph(actor_list)
#   subG = G
#   start_time = time.time()
#   #calculation = nx.pagerank(subG, alpha=0.85, weight='count', tol=1e-10)
#   calculation = nx.pagerank(subG, alpha=0.85)
#   end_time = time.time()
#   print("Result:")
#   for bums in dict(sorted(calculation.items(), key=lambda item: item[1])):
#       print(bums,calculation[bums])
#   print("RUNTIME PageRank: ", end_time - start_time)


def getNodeCount(graph):
    nodecount = 0
    for node in G.nodes.items():
        nodecount = nodecount + 1
    return nodecount

def create_graph_from_neo4j_csv(LG,filePath):
    with open(filePath,'r') as csv_file:
        reader = csv.DictReader(csv_file,quotechar = '"', delimiter=',')
        reader2 = csv.DictReader(csv_file,quotechar = '"', delimiter=',')
        for line in reader:
            if line['_id'] != "":
                LG.add_node(line['_id'], id=line['_id'], label=line['_labels'].replace(":",""), name=line['name'])
        nodeStuff = LG.nodes(data=True)
        #print(nodeStuff)
        for line in reader2:
            print("LINESTART: " + line['_start'])
            print("LINEEND  : " + line['_end'])
            startNode=str([nodeName for nodeName,nodeId in nodeStuff(data='id') if nodeId == line['_start']])
            endNode=str([nodeName for nodeName,nodeId in nodeStuff(data='id') if nodeId == line['_end']])
            print("START: " + startNode)
            print("END  : " + endNode)
            #endNode=str([nodeName for nodeName,nodeAttributes in LG.nodes(data=True) if nodeAttributes['id'] == line['_end']])
            LG.add_edge(startNode, endNode, type=line['_type'],count=int(line['count']))
            #LG.add_edge(line['_start'],line['_end'], type=line['_type'],count=int(line['count']))
            #G.add_edge(line['_end'],line['_start'],type=line['_type'],cost=float(line['cost']),count=int(line['count']),dice=line['dice']) 
    #start_time = time.time() 
    #dict_nodes = nx.closeness_centrality(G)
    #print("ZEIT: " + str(time.time() - start_time))
    #print(G.nodes(data=True)) 

    #for bums in dict(sorted(dict_nodes.items(), key=lambda item: item[1])):
    #    print(bums,dict_nodes[bums],G.nodes[bums]['name'])

##### HIER GEHTS LOS ##############

doImportFromExportedCSV = False

filepath='/home/pagai/graph-data/tmdb_fixed.csv'
file = open(filepath, 'r')
if (len(sys.argv) == 1):
    print("NOTHING WAS GIVEN, EXECUTING IMPORT FROM OTHER FILE.")
    limit = 999999999
else: 
    limit = int(sys.argv[1])
    print("LOADING " + str(limit) + " LINES FROM " + filepath)
if limit != "all":
    cleanup = True
    

# Loading headers
header_reader = csv.reader(file)
#print("HEADERS : " + str(get_column_names(header_reader)))
#print(headers)

full_actor_list = []
full_genre_list = []
full_keyword_list = []
full_company_list = []
full_director_list = []
full_person_list = []

# Creating graph
G = nx.DiGraph(name="Graph of MovieDB")
# ID Counter for unique nodes...*sigh*
id=1
## opening file
with open(filepath, 'r') as csv_file1:
    linecount = 1 
    reader1 = csv.DictReader(csv_file1, quotechar='"', delimiter=',')

# Reading actors, genres, keywords, companies and directors
    startTime = time.time()
    for row in reader1:
        if linecount < limit:
            linecount = linecount + 1  
            for actor in row['cast'].split("|"):
                full_actor_list.append(actor)
                full_person_list.append(actor)
            for genre in row['genres'].split("|"):
                full_genre_list.append(genre)
            for keyword in row['keywords'].split("|"):
                full_keyword_list.append(keyword)
            for company in row['production_companies'].split("|"):
                full_company_list.append(company)
            for director in row['director'].split("|"):
                full_director_list.append(director)
                full_person_list.append(director)

# removing double entries        
    unique_actors = remove_doubles(full_actor_list)
    unique_genres = remove_doubles(full_genre_list)
    unique_keywords = remove_doubles(full_keyword_list)
    unique_companies = remove_doubles(full_company_list)
    unique_directors = remove_doubles(full_director_list)
    unique_persons = remove_doubles(full_person_list)
    
    print("ACTORS: " + str(len(unique_actors)))
    print("GENRES: " + str(len(unique_genres)))
    print("KEYWOR: " + str(len(unique_keywords)))
    print("COMPAN: " + str(len(unique_companies)))
    print("DIRECT: " + str(len(unique_directors)))
    print("PERSONS: " + str(len(unique_persons)))

#    print(unique_keywords)

#    print("Runtime creating unique lists : " + str((time.time() - startTime)))
    
        
# creating nodes
    print("START ADDING NODES")
    startTimeNodes= time.time()
#    for actor in unique_actors:
    actorDict = {}
    directorDict = {}
    companyDict = {}
    keywordDict = {}
    genreDict = {}
    idDict = {}
    for person in unique_persons:
        roleList = []
        if (person in unique_directors):
            roleList.append('DIRECTOR')
            directorDict[person] = id
        if (person in unique_actors):
            roleList.append('ACTOR')     
            actorDict[person] = id
        G.add_node(id, label='PERSON', name=str(person), roles=roleList)
        id+=1
    for keyword in unique_keywords:
        keywordDict[keyword] = id
        G.add_node(id, label='KEYWORD', name=str(keyword))
        id+=1
    for genre in unique_genres:
        genreDict[genre] = id
        G.add_node(id, label='GENRE' , name=str(genre))
        id+=1
#    for director in unique_directors:
#        G.add_node(id, label='DIRECTOR' , name=str(director))
#        id+=1
    for company in unique_companies:
        companyDict[company] = id
        G.add_node(id, label='PRODUCTION_COMPANY', name=str(company))
        id+=1
idDict.update(actorDict)
idDict.update(directorDict)
idDict.update(genreDict)
idDict.update(keywordDict)
idDict.update(companyDict)
print(idDict)
print("ADDED NODES IN " + to_ms(time.time() - startTimeNodes))

# creating movienodes and relationships
print("START ADDING MOVIES AND RELATIONS")
startTimeMovies = (time.time())
tmpGraph = G.nodes(data=True)  
with open(filepath, 'r') as csv_file1:
    reader1 = csv.DictReader(csv_file1, quotechar='"', delimiter=',')
    linecount=1
# Reading actors, genres, keywords, companies and directors for every movie
    for row in reader1:
        if linecount < limit:
            linecount = linecount + 1
            G.add_node(id, name=row['original_title'], label='MOVIE', attr_dict=row)
            for actor1 in row['cast'].split("|"):
                idActor1 = actorDict[actor1]
                #idActor1 = [idtemp1 for idtemp1,attributes1 in tmpGraph if ('ACTOR' in attributes1.get('roles',"None") and attributes1.get('name') == actor1)][0]
                #idActor1 = str([idtemp1 for idtemp1,attributes1 in G.nodes(data=True) if ('ACTOR' in attributes1.get('roles',"None") and attributes1.get('name') == actor1)][0])
                
                for actor2 in row['cast'].split("|"):
                    idActor2 = actorDict[actor2]
                    #idActor2 = [idtemp2 for idtemp2,attributes2 in tmpGraph if ('ACTOR' in attributes2.get('roles',"None") and attributes2.get('name') == actor2)][0]
                    #idActor2 = str([idtemp2 for idtemp2,attributes2 in G.nodes(data=True) if ('ACTOR' in attributes2.get('roles',"None") and attributes2.get('name') == actor2)][0])
                    if idActor1 != idActor2:
                        G.add_edge(idActor1, idActor2 ,type='ACTED_WITH',count=1.0)
                        #G.add_edge(idActor2, idActor1,type='ACTED_WITH',count=1.0)
                G.add_edge(idActor1, id, type='ACTED_IN' )
            for director in row['director'].split("|"):
                #idDirector = [idtemp for idtemp,attributes in tmpGraph if ('DIRECTOR' in attributes.get('roles',"None") and attributes.get('name') == director)][0]
                idDirector = directorDict[director]
                G.add_edge(idDirector, id, type="DIRECTED" )
            for company in row['production_companies'].split("|"):
                #idCompany = [idtemp for idtemp,attributes in tmpGraph if (attributes.get('label') == 'PRODUCTION_COMPANY' and attributes.get('name') == company)][0]
                idCompany = companyDict[company]
                G.add_edge(idCompany, id, type="PRODUCED" )    
            for genre in row['genres'].split("|"):
                #idGenre = [idtemp for idtemp,attributes in tmpGraph if (attributes.get('label') == 'GENRE' and attributes.get('name') == genre)][0]
                idGenre = genreDict[genre]
                G.add_edge(id, idGenre, type="IN_GENRE" )
            for keyword in row['keywords'].split("|"):
                #idKeyword = [idtemp for idtemp,attributes in tmpGraph if (attributes.get('label') == 'KEYWORD' and attributes.get('name') == keyword)][0]
                idKeyword = keywordDict[keyword]
                G.add_edge(id, idKeyword, type="HAS_KEYWORD" )
            id+=1
            #print(nx.info(G))
print("ADDED MOVIES AND RELATIONS IN " + to_ms(time.time() - startTimeMovies))

#peng = (unique_actors, unique_genres, unique_keywords, unique_companies, unique_directors)
#for bums in peng:
#    print(bums.len(bums))
#print(G.nodes(data="name"))

#export_graph_to_node_link_data(G,"/home/pagai/graph-data/moviedb_export_node_link_data.json")



# LG is the graph loaded from the CSV.         
if (doImportFromExportedCSV):
    LG = nx.DiGraph(name="Graph loaded from neo4j CSV")
    filePath='/home/pagai/graph-data/owndb01/moviedb.csv'
    print("STARTING LOAD FROM " + filePath)
    create_graph_from_neo4j_csv(LG, filePath)
    print("LOAD DONE")

#### IMPORT FILE
#start_time = time.time()
#G = import_node_link_data_to_graph('/var/tmp/node_link_data_5000.json')
#print("File load finished in " + str(time.time() - start_time))

# EXPORT FILE
#start_time = time.time()
#export_graph_to_node_link_data(G, '/var/tmp/node_link_data_5000.json')
#print("File export finished in : " + str(time.time() - start_time))

#actor_list=[x for x,y in G.nodes(data=True) if y['type'] == 'actor']
#print("ACTORS: " + str(len(actor_list)));

print("######## INFO G:")
print(nx.info(G))
if (doImportFromExportedCSV):
    print("INFO LG:")
    print(nx.info(LG))
    actor_list_LG=[nodeName for nodeName,nodeAttributes in G.nodes(data=True) if nodeAttributes['label'] == 'ACTOR']
    subLG = LG.subgraph(actor_list_LG)
# ALGOS
#algo_shortest_path(G)
#all_pairs_shortest_path(G)
#print(list(G.nodes.data())[1])
#print(list(LG.nodes.data())[1])
 


#print(G.nodes(data=True))
#print("BUMS" + str(G.nodes[]['label']))

#for node in G.nodes(data=True)['name']:
#    print(node)
    

actor_list_G=[x for x,y in G.nodes(data=True) if (y.get('roles',"None")).count('ACTOR') > 0]
keyword_list_G=[x for x,y in G.nodes(data=True) if (y.get('label') == 'KEYWORD')]
director_list_G=[x for x,y in G.nodes(data=True) if (y.get('roles',"None")).count('DIRECTOR') > 0]
person_list_G=[x for x,y in G.nodes(data=True) if (y.get('label') == 'PERSON')]
company_list_G=[x for x,y in G.nodes(data=True) if (y.get('label') == 'PRODUCTION_COMPANY')]
genre_list_G=[x for x,y in G.nodes(data=True) if (y.get('label') == 'GENRE')]



#print([y for x,y in G.nodes(data=True) if (y.get('name') == 'dna')])
#
print("########### A ###############")
print(len(sorted(actor_list_G)))
print(len(sorted(unique_actors)))
print("########## D ###############")
print(len(sorted(director_list_G)))
print(len(sorted(unique_directors)))
print("########## P ###############")
print(len(sorted(person_list_G)))
print(len(sorted(unique_persons)))
print("########## KW ###############")
print(len(sorted(keyword_list_G)))
print(len(sorted(unique_keywords)))
print("########## G ###############")
print(len(sorted(genre_list_G)))
print(len(sorted(unique_genres)))
print("########## C ###############")
print(len(sorted(company_list_G)))
print(len(sorted(unique_companies)))


subG = G.subgraph(actor_list_G)
print(nx.info(subG))
#print("===== #onenode ========")
#print(list(subG.nodes.data())[1])
#if (doImportFromExportedCSV):
#    print(list(subLG.nodes.data())[1])
print("===== Number of nodes ==========")
if (doImportFromExportedCSV):
    print("subLG: " + str(subLG.number_of_nodes()))
    print("subG:  " + str(subG.number_of_nodes()))
    print("LG: " + str(LG.number_of_nodes()))
print("G    : " + str(G.number_of_nodes()))
print("subG : " + str(subG.number_of_nodes()))

if (doImportFromExportedCSV):
    print("========= ALGO SUBLG")
    algo_pagerank(subLG,None,"default", False)
    algo_pagerank(LG, None, "default", False)
 #   algo_pagerank(LG, None, "numpy", False)
    algo_pagerank(LG, None, "scipy", False)

print("========= ALGO FULL G ==========")
algo_pagerank(G,None, "default", True, idDict)
algo_pagerank(G,None, "scipy", True, idDict)

print("========= ALGO SUBG ==========")
algo_pagerank(subG,None,"default", True, idDict)
algo_pagerank(subG, None, "scipy", True, idDict)

#algo_degree_centrality(G)
#algo_betweenness_centrality(G)
#get_hits(G)


#print(pagerank_scipy(subG))
#if limit < 100:
#    draw_graph(G)

#print("FERTIG")
