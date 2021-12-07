import networkx as nx
import numpy as np
import pandas as pd

'''
The below function get_graph gives us a complete bipartite graph.
Input: number of nodes and number of clusters.
Output: complete bipartite graph.
'''

def get_graph(nodes,clusters):
	graph = {}
	for i in range(nodes):
		graph[i] = [nodes + j for j in range(clusters)]
	for j in range(clusters):
		graph[nodes + j] = [i for i in range(nodes)]
	return graph

'''
The below function depth_first gives a list of all paths from a current vertex 
Input:  graph, starting vertex, list of nodes already visited(typically []).
Output: all cycle-free paths in the graph that start with the current vertex.
'''

already_visited = []

def depth_first(graph, currentVertex, visited):
    visited.append(currentVertex)
    for vertex in graph[currentVertex]:
        if vertex not in visited:
            depth_first(graph, vertex, visited.copy())
    already_visited.append(visited)
    return already_visited
    
'''
The below function sequential_paths utilizes depth_first to find all paths starting at each vertex in the graph.
Input: graph, number of nodes, number of clusters
Output: all paths in a graph that begin at a cluster
'''


def sequential_paths(graph, nodes, clusters):
	paths = []
	for i in range(nodes, nodes+clusters):
		already_visited = []
		somePaths = depth_first(graph, i, [])
		paths += somePaths

	filter_dup_paths = list(filter(lambda c: c[0] < c[-1], paths))
	even_length_paths = list(filter(lambda c: len(c) % 2 == 1, filter_dup_paths))
	#even_length_paths = set(even_length_paths)
	return even_length_paths
	

'''
The below function sequential_circuits takes all the paths found in sequential_paths and turns them into circuits by assigning them 1 if they are entering a cluster and -1 if they are leaving a cluster.
input: number of nodes and number of clusters
output: all sequential circuits in our graph.
'''


def sequential_circuits(nodes, clusters):
	graph = get_graph(nodes, clusters)
	paths = sequential_paths(graph, nodes, clusters)

	num_paths = len(paths)
	print(num_paths)
	circuits = []
	for i in range(num_paths):
		path = paths[i]
		pos_circ = np.zeros(nodes*clusters)
		#print(path)
		#Entry (i*C <- number of clusters) + j denotes variable x_ij for i assigned to j
		odd_step = [path[i+1]*clusters + (path[i] - nodes) for i in range(0, len(path)-1, 2)]
		even_step = [path[i]*clusters + (path[i+1] - nodes) for i in range(1, len(path)-1, 2)]

		pos_circ[odd_step] = -1
		pos_circ[even_step] = 1
		neg_circ = -1*pos_circ
		circuits.append(pos_circ)
		circuits.append(neg_circ)
	#circuits=set(circuits)
	return circuits
