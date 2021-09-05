#!/usr/bin/python
import csv
import networkx as nx
import matplotlib.pyplot as plt
import time
import sys
import json
import os
import gc
from _tkinter import create
from logging import _startTime

# import own helper-modules
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),"../../networkx_modules")))
from helpers.generalStuff import *
from helpers.networkx_load_n_save import *
from helpers.search_functions import *

from algoPackage.pageRank import *
from algoPackage.simRank import *
from algoPackage.hits import *
from algoPackage.shortestPath import *
from algoPackage.jaccard_coefficient import *
from algoPackage.degree_centrality import *

from builtins import len
from networkx.algorithms.coloring.greedy_coloring_with_interchange import Node
from networkx.classes.function import get_node_attributes
from networkx.readwrite import json_graph
from _operator import itemgetter
from xlwt.ExcelFormulaLexer import false_pattern
from cairosvg.helpers import distance

 
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


####def algo_shortest_path(G):
####    actor_list=[x for x,y in G.nodes(data=True) if y['labels'] == 'ACTOR']
#####===============================================================================
##### subgraph Returns a SubGraph view of the subgraph induced on nodes.
##### The induced subgraph of the graph contains the nodes in nodes and the edges between those nodes.
#####===============================================================================
####    subG = G.subgraph(actor_list)
#####    for actor in actor_list:
#####        print(actor)
####    numberOfActors = len(actor_list)
#####    print("FOUND " + str(numberOfActors) + " ACTORS." )
####    algoTime=time.time()
####    #Lahm
#####    for actor in actor_list:
#####       #print("Example: Calculating shortest paths from " + actor + " to anyone...\r")
#####        for actor2 in actor_list:
#####            if (actor != actor2):
#####                try:
#####                    path = nx.shortest_path(subG, source=(actor), target=actor2)
#####                except nx.NetworkXNoPath as e:
#####                    path = e
#####                except nx.NodeNotFound as e:
#####                    path = e
####    ### schnell
####    for i in range(numberOfActors):
####        actor = actor_list[i]
####        #print("STARTNODE: " + actor)
####        j = i + 1
####        while j < numberOfActors:
####            actor2 = actor_list[j]
####         #   print(actor2)
####            try:
####                path = nx.shortest_path(subG, source=(actor), target=actor2)
####            except nx.NetworkXNoPath as e:
####                path = e
####            except nx.NodeNotFound as e:
####                path = e
####            #print(path)
####            j = j + 1 
####    #print("RUNTIME : " + str(time.time() - start_time) )
####    #     print(path)
####    print("RUNTIME ShortestPath - " +  str(limit) + " entries - " + str(numberOfActors) + " actors : " + to_ms(time.time() - algoTime) + "s.")


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


##### MAIN ##############
### SETTINGS ############
verbose=False
doImportFromExportedCSV = False
doExport=False
doMultiExport=False
doExport=False
createByImport=False


limit=0
seclimit=1
importExportFileName = "/tmp/node_link_data_export_moviedb_" + str(limit) + ".json"

doAlgo=True
doAlgoShortestPath=False
doDegreeCentrality=False
doPageRank=True
doSimRank=False
doHITS=False

operatorFunction="eq"
algoVerbose=False
drawit=False

deleteTest=False
testGetAll=False
testSearch=False

#################################

filepath='/home/pagai/graph-data/tmdb_fixed.csv'
file = open(filepath, 'r')
if (len(sys.argv) == 1):
    if (verbose): 
        print("NOTHING WAS GIVEN, EXECUTING IMPORT FROM OTHER FILE.")
    limit = 999999999
else: 
    limit = int(sys.argv[1])
    if (verbose): 
        print("LOADING " + str(limit) + " LINES FROM " + filepath)
if limit != "all":
    cleanup = True

if not createByImport:
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
    
    actorDict = {}
    directorDict = {}
    companyDict = {}
    keywordDict = {}
    genreDict = {}
    idDict = {}
        
    # Creating graph
    G = nx.DiGraph(name="Graph of MovieDB")
    # ID Counter for unique nodes...*sigh*
    id=1
    ## opening file
    with open(filepath, 'r') as csv_file1:
        linecount = 1 
        reader1 = csv.DictReader(csv_file1, quotechar='"', delimiter=',')
    
    # Reading actors, genres, keywords, companies and directors
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
        if (verbose): 
            print("ACTORS   : " + str(len(unique_actors)))
            print("GENRES   : " + str(len(unique_genres)))
            print("KEYWORDS : " + str(len(unique_keywords)))
            print("COMPANIES: " + str(len(unique_companies)))
            print("DIRECTORS: " + str(len(unique_directors)))
            print("PERSONS  : " + str(len(unique_persons)))
    
    # creating nodes
        if (verbose): 
            print("START ADDING NODES")
        startTimeNodes= time.time()
    #    for actor in unique_actors:
    
        for person in unique_persons:
            addActorRole=False
            addDirectorRole=False
            #roleList = []
            if (person in unique_directors):
             #   roleList.append('DIRECTOR')
                addDirectorRole=True
                directorDict[person] = id
            if (person in unique_actors):
                addActorRole=True
              #  roleList.append('ACTOR')     
                actorDict[person] = id
            G.add_node(id, labels='PERSON', name=str(person), ACTOR=addActorRole, DIRECTOR=addDirectorRole)
            id+=1
        for keyword in unique_keywords:
            keywordDict[keyword] = id
            G.add_node(id, labels='KEYWORD', name=str(keyword))
            id+=1
        for genre in unique_genres:
            genreDict[genre] = id
            G.add_node(id, labels='GENRE' , name=str(genre))
            id+=1
    #    for director in unique_directors:
    #        G.add_node(id, labels='DIRECTOR' , name=str(director))
    #        id+=1
        for company in unique_companies:
            companyDict[company] = id
            G.add_node(id, labels='PRODUCTION_COMPANY', name=str(company))
            id+=1
    idDict.update(actorDict)
    idDict.update(directorDict)
    idDict.update(genreDict)
    idDict.update(keywordDict)
    idDict.update(companyDict)
    if (verbose): 
        print("ADDED NODES IN " + to_ms(time.time() - startTimeNodes) + " s")
    
    # creating movienodes and relationships
    if (verbose): 
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
                G.add_node(id, labels='MOVIE', name=row['original_title'])
                for bums in row.keys():
                    G.nodes[id][bums] = row[bums]
                for actor1 in row['cast'].split("|"):
                    idActor1 = actorDict[actor1]
                    #idActor1 = [idtemp1 for idtemp1,attributes1 in tmpGraph if ('ACTOR' in attributes1.get('roles',"None") and attributes1.get('name') == actor1)][0]
                    #idActor1 = str([idtemp1 for idtemp1,attributes1 in G.nodes(data=True) if ('ACTOR' in attributes1.get('roles',"None") and attributes1.get('name') == actor1)][0])
                    
                    for actor2 in row['cast'].split("|"):
                        idActor2 = actorDict[actor2]
                        #idActor2 = [idtemp2 for idtemp2,attributes2 in tmpGraph if ('ACTOR' in attributes2.get('roles',"None") and attributes2.get('name') == actor2)][0]
                        #idActor2 = str([idtemp2 for idtemp2,attributes2 in G.nodes(data=True) if ('ACTOR' in attributes2.get('roles',"None") and attributes2.get('name') == actor2)][0])
                        if idActor1 != idActor2:
                            G.add_edge(idActor1, idActor2 ,type='ACTED_WITH', weight=1 )
                            G.add_edge(idActor2, idActor1,type='ACTED_WITH', weight=1 )
                    G.add_edge(idActor1, id, type='ACTED_IN', weight=1 )
                for director in row['director'].split("|"):
                    #idDirector = [idtemp for idtemp,attributes in tmpGraph if ('DIRECTOR' in attributes.get('roles',"None") and attributes.get('name') == director)][0]
                    idDirector = directorDict[director]
                    G.add_edge(idDirector, id, type="DIRECTED", weight=1 )
                for company in row['production_companies'].split("|"):
                    #idCompany = [idtemp for idtemp,attributes in tmpGraph if (attributes.get('labels') == 'PRODUCTION_COMPANY' and attributes.get('name') == company)][0]
                    idCompany = companyDict[company]
                    G.add_edge(idCompany, id, type="PRODUCED", weight=1 )    
                for genre in row['genres'].split("|"):
                    #idGenre = [idtemp for idtemp,attributes in tmpGraph if (attributes.get('labels') == 'GENRE' and attributes.get('name') == genre)][0]
                    idGenre = genreDict[genre]
                    G.add_edge(id, idGenre, type="IN_GENRE", weight=1 )
                for keyword in row['keywords'].split("|"):
                    #idKeyword = [idtemp for idtemp,attributes in tmpGraph if (attributes.get('labels') == 'KEYWORD' and attributes.get('name') == keyword)][0]
                    idKeyword = keywordDict[keyword]
                    G.add_edge(id, idKeyword, type="HAS_KEYWORD", weight=1 )
                id+=1
                #print(nx.info(G))
    if (verbose): 
        print("ADDED MOVIES AND RELATIONS IN " + to_ms(time.time() - startTimeMovies))
    

########## TESTING BEGINS HERE ################
#### TEST GET ALL
if (testGetAll):
    startTime=time.time()
    #startTime=time.time_ns()
    nodes = G.nodes(data=True)
    #edges = G.edges(data=True)
    endTime=time.time()



        
#endTime=time.time_ns()
#print(edges)    
# LG is the graph loaded from the CSV.         
if (doImportFromExportedCSV):
    LG = nx.DiGraph(name="Graph loaded from neo4j CSV")
    filePath='/home/pagai/graph-data/owndb01/moviedb.csv'
    if (verbose): 
        print("STARTING LOAD FROM " + filePath)
    LG = create_graph_from_neo4j_csv(filePath, inputDirectedData=True, outputDirectedGraph=True)
    if (verbose): 
        print("LOAD DONE")

############ Export/Import ##########
if createByImport:
    importFile='/tmp/node_link_data_export_moviedb_'+str(limit)+'.json'
    if verbose:
        print("IMPORTING " + importFile)
    startTime = time.time()
    G = import_node_link_data_to_graph(importFile, verbose=verbose)
    if (verbose): 
        print("IMPORTED FILE: " + importFile)
        print(nx.info(G))
    endTime=time.time()
if doExport:
    export_graph_to_node_link_data(G, '/tmp/node_link_data_export_moviedb_'+str(limit)+'.json', verbose=verbose)

#### TEST SEARCH MOVIES FROM 2015 ##############
if (testSearch):
    entrycount=0
    startTime=time.time()
    #resultList = [movie for movie,attributes in G.nodes(data=True) if ((attributes.get('labels') == 'MOVIE') & (attributes.get('release_year') == '2015'))]
    resultList = [movie for movie,attributes in G.nodes(data=True) if (attributes.get('labels') == 'PERSON')]
    endTime=time.time()
    if verbose:
        for entry in resultList:
            entrycount+=1
        print("FOUND:",entrycount,"RESULTS")        
    print(limit,G.number_of_nodes(),G.number_of_edges(),to_ms(endTime - startTime),sep=",")




# MULTI EXPORT FILE
if (doMultiExport):
    start_time = time.time()
    export_graph_to_node_link_data(LG, '/tmp/node_link_data_export.json', verbose=False)
    print("NodeLinkData export finished in : " + str(time.time() - start_time))
    start_time = time.time()
    export_graph_to_graphML_data(LG,'/tmp/graphML_export.json')
    print("GraphML export finished in : " + str(time.time() - start_time))
    start_time = time.time()
    export_graph_to_adjlist_data(LG,'/tmp/adjlist_export.json')
    print("ADJ export finished in : " + str(time.time() - start_time))
    start_time = time.time()
    export_graph_to_multiline_adjlist_data(LG,'/tmp/multilineadjlist_export.json')
    print("MultiADJ export finished in : " + str(time.time() - start_time))
    start_time = time.time()
    export_graph_to_yaml_data(LG,'/tmp/yaml_data_export.yaml')
    print("YAML export finished in : " + str(time.time() - start_time))
    start_time = time.time()
    export_graph_to_gml_data(LG,'/tmp/gml_data_export.gml')
    print("GML export finished in : " + str(time.time() - start_time))

if (doImportFromExportedCSV):
    if (verbose): 
        print("######## INFO LG:")
        print(nx.info(LG))
    person_list_LG=[nodeName for nodeName,nodeAttributes in LG.nodes(data=True) if (nodeAttributes.get('labels') == "PERSON")]
    subLG = LG.subgraph(person_list_LG)
    if (verbose): 
        print("######## INFO SubLG:")
        print(nx.info(SubLG))


#########################################################################

if (verbose and not createByImport): 
    print("######## INFO G:")
    print(nx.info(G))
    print("########### G ###############")
    print("########### A ###############")
    print(len(sorted(unique_actors)))
    print("########## D ###############")
    print(len(sorted(unique_directors)))
    print("########## P ###############")
    print(len(sorted(unique_persons)))
    print("########## KW ###############")
    print(len(sorted(unique_keywords)))
    print("########## G ###############")
    print(len(sorted(unique_genres)))
    print("########## C ###############")
    print(len(sorted(unique_companies)))


#print("===== #onenode ========")
#print(list(subG.nodes.data())[1])
#if (doImportFromExportedCSV):
#    print(list(subLG.nodes.data())[1])
if (verbose): 
    print("===== Number of nodes ==========")
    if (doImportFromExportedCSV):
        print("subLG: " + str(subLG.number_of_nodes()))
        print("subG:  " + str(subG.number_of_nodes()))
        print("LG: " + str(LG.number_of_nodes()))
        print("G    : " + str(G.number_of_nodes()))
    
########## DELETE-test Clear ################
if deleteTest:
    numberOfNodes = G.number_of_nodes()
    numberOfEdges = G.number_of_edges()
    start_time_clear=time.time()
    G.clear()
    export_graph_to_node_link_data(G, importExportFileName, verbose=verbose)
    end_time_clear=time.time()
    print(numberOfNodes, numberOfEdges, to_ms(end_time_clear - start_time_clear), sep=",")

########### ALGO TESTS ################
if doAlgo:
    #### SHORTEST PATH
    if doAlgoShortestPath:
        
        startTime=time.time()
        nodeList=[x for x,y in G.nodes(data=True) if (y.get('ACTOR') == True)]
        subG = G.subgraph(nodeList)
        algo_shortest_path(subG,verbose=False)
        
        #algo_all_pairs_dijkstra(G,verbose=False,inputWeight='weight')
        #algo_all_pairs_bellman_ford_path(G,verbose=True,inputWeight='weight')
        
        #all_pairs_shortest_path(G)
        
        #algo_all_pairs_shortest_path(G,verbose=False,inputWeight='weight')
        #draw_all_shortest_path_for_single_node(G,"1")
        #all_shortest_path_for_single_node(G,"12")
        
        
        #### SHORTESTPATH ASTAR
        #algo_all_pairs_shortest_path_astar(G,verbose=verbose)
        endTime=time.time()
        print(limit,G.number_of_nodes(), G.number_of_edges(), to_ms(endTime - startTime), sep=",")
        
    #### PAGERANK    
    if doPageRank:   
        start_time = time.time()
        #actor_list_G=[x for x,y in G.nodes(data=True) if (y.get('roles',"None")).count('ACTOR') > 0]
        #keyword_list_G=[x for x,y in G.nodes(data=True) if (y.get('labels') == 'KEYWORD')]
        #director_list_G=[x for x,y in G.nodes(data=True) if (y.get('roles',"None")).count('DIRECTOR') > 0]
        person_list_G=[x for x,y in G.nodes(data=True) if (y.get('ACTOR') == True)]
        #company_list_G=[x for x,y in G.nodes(data=True) if (y.get('labels') == 'PRODUCTION_COMPANY')]
        #genre_list_G=[x for x,y in G.nodes(data=True) if (y.get('labels') == 'GENRE')]
        subG = G.subgraph(person_list_G)
        if verbose: 
            print(nx.info(subG))
            #print(nx.info(G))
        #weightInputForAlgos="weight"
        weightInputForAlgos=None
        if (algoVerbose):
            print("==============================")
        algo_pagerank(subG, "default",  weightInput=weightInputForAlgos, verbose=algoVerbose, maxLineOutput=0)
        ###### NUMPY IS OBSOLETE
        #### DO NOT USE #####algo_pagerank(subG, "numpy", weightInput=weightInputForAlgos, verbose=algoVerbose, maxLineOutput=0)
        #algo_pagerank(subG, "scipy", weightInput=weightInputForAlgos, verbose=algoVerbose, maxLineOutput=0)
        if (algoVerbose):
            print("==============================")
        print(limit,subG.number_of_nodes(),subG.number_of_edges(),to_ms(time.time() - start_time),sep=",")
    
    #### SIMRANK
    if doSimRank:
        algo_simRank(G,verbose=True,max_iterations=1)

    #### DEGREE CENTRALITY
    if doDegreeCentrality:
        # Degree Centrality - own
        verbose=True
        #peng = sorted(G.degree, key=lambda x: x[1], reverse=True)
        #if (verbose):
        #    for bums in peng:
        #        print(bums)
        
        # Degree Centrality - native
        #algo_degree_centrality(G, verbose=False)
    
    #### HITS
    if doHITS:
        get_hits(G)

if (drawit):
    draw_graph(G)

