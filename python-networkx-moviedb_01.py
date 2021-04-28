#!/usr/bin/python
import csv
import networkx as nx
import matplotlib.pyplot as plt
import time
import sys
import json

from builtins import len
from networkx.algorithms.coloring.greedy_coloring_with_interchange import Node
from networkx.classes.function import get_node_attributes
from networkx.readwrite import json_graph
from _operator import itemgetter
from xlwt.ExcelFormulaLexer import false_pattern
from cairosvg.helpers import distance


def to_ms(time):
    return ("%.3f" % time)

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

def import_node_link_data_to_graph(inputfile):
    file_to_read = open(inputfile, 'r')
    json_data = json.loads(file_to_read.read())    
    return json_graph.node_link_graph(json_data, directed=True, multigraph=False)

def export_graph_to_node_link_data(G,outputfile):
    print("Exporting graph to node_link_data-file")
    file_to_write = open(outputfile, 'w')
    file_to_write.write(json.dumps(json_graph.node_link_data(G)))


def all_pairs_shortest_path(G):
    actor_list=[x for x,y in G.nodes(data=True) if y['type'] == 'actor']
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
    actor_list=[x for x,y in G.nodes(data=True) if y['type'] == 'actor']
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
    actor_list=[x for x,y in G.nodes(data=True) if y['type'] == 'actor']
    subG = G.subgraph(actor_list)
    dict_nodes = []
    dict_nodes = nx.degree_centrality(subG);
    print("Result:")
    for bums in dict(sorted(dict_nodes.items(), key=lambda item: item[1])):
        print(bums,dict_nodes[bums])
#    print("RUNTIME ClosenessCentrality - " +  str(limit) + " entries - " + str(len(actor_list)) + " actors : " + to_ms((time.time() - algoTime)) + "s.")
    print("RUNTIME ClosenessCentrality - " +  str(limit) + " entries - " + to_ms((time.time() - algoTime)) + "s.")   
   

def algo_shortest_path(G):
    actor_list=[x for x,y in G.nodes(data=True) if y['type'] == 'actor']
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


def algo_pagerank(G):
    print("Calculating pagerank")
    actor_list=[x for x,y in G.nodes(data=True) if y['type'] == 'actor']
    subG = G.subgraph(actor_list)
    start_time = time.time()
    calculation = nx.pagerank(subG, alpha=0.85, weight='count', tol=1e-10)
    end_time = time.time()
    print("Result:")
    for bums in dict(sorted(calculation.items(), key=lambda item: item[1])):
        print(bums,calculation[bums])
    print("RUNTIME PageRank: ", end_time - start_time)


##### HIER GEHTS LOS ##############
filepath='/home/pagai/graph-data/tmdb.csv'
file = open(filepath, 'r')
limit = int(sys.argv[1])
if limit == None:
    limit = 100000
    

# Loading headers
header_reader = csv.reader(file)
#print("HEADERS : " + str(get_column_names(header_reader)))
#print(headers)

full_actor_list = []
full_genre_list = []
full_keyword_list = []
full_company_list = []
full_director_list = []

# Creating graph
G = nx.DiGraph()

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
            for genre in row['genres'].split("|"):
                full_genre_list.append(genre)
            for keyword in row['keywords'].split("|"):
                full_keyword_list.append(keyword)
            for company in row['production_companies'].split("|"):
                full_company_list.append(company)
            for director in row['director'].split("|"):
                full_director_list.append(director)
    
# removing double entries        
    unique_actors = remove_doubles(full_actor_list)
    unique_genres = remove_doubles(full_genre_list)
    unique_keywords = remove_doubles(full_keyword_list)
    unique_companies = remove_doubles(full_company_list)
    unique_directors = remove_doubles(full_director_list)

#    print("Runtime creating unique lists : " + str((time.time() - startTime)))
    
    
# creating nodes
    startTime= time.time()
    for actor in unique_actors:
        G.add_node(actor, type='actor', name=str(actor))
    for keyword in unique_keywords:
        G.add_node(keyword, type='keyword', name=str(keyword))
    for genre in unique_genres:
        G.add_node(genre, type='genre' , name=str(genre))
    for director in unique_directors:
        G.add_node(director, type='director' , name=str(director))
    for company in unique_companies:
        G.add_node(company, type='production_company', name=str(company))
#    print("Runtime adding single nodes : " + str((time.time() - startTime)))

# creating movienodes and relationships
startTime = (time.time())  
with open(filepath, 'r') as csv_file1:
    reader1 = csv.DictReader(csv_file1, quotechar='"', delimiter=',')
    linecount=1
# Reading actors, genres, keywords, companies and directors for every movie
    edgelist_to_import = []
    for row in reader1:
        if linecount < limit:
            linecount = linecount + 1 
            G.add_node(row['original_title'], type='movie', attr_dict=row)
            for actor1 in row['cast'].split("|"):
                for actor2 in row['cast'].split("|"):
                    if actor2 != actor:
                        G.add_edge(actor1, actor2,type='ACTED_WITH',count=1.0)
                        G.add_edge(actor2, actor1,type='ACTED_WITH',count=1.0)
                G.add_edges_from([(actor1, row['original_title'])], type='ACTED_IN' )
            for director in row['director'].split("|"):
                G.add_edges_from([(director, row['original_title'])], type="DIRECTED" )
            for company in row['production_companies'].split("|"):
                G.add_edges_from([(company, row['original_title'])], type="PRODUCED" )    
            for genre in row['genres'].split("|"):
                G.add_edges_from([(row['original_title'], genre)], type="IN_GENRE" )
            for keyword in row['keywords'].split("|"):
                G.add_edges_from([(row['original_title'], keyword)], type="HAS_KEYWORD" )

def getNodeCount(graph):
    nodecount = 0
    for node in G.nodes.items():
        nodecount = nodecount + 1
    return nodecount



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

# ALGOS

#algo_shortest_path(G)
#all_pairs_shortest_path(G)
#algo_pagerank(G)
#algo_degree_centrality(G)
algo_betweenness_centrality(G)
#get_hits(G)


#print(pagerank_scipy(subG))
#if limit < 100:
#    draw_graph(G)

#print("FERTIG")
