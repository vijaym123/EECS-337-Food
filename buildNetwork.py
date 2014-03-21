import networkx as nx
import json
import itertools
import random
if __name__ == "__main__":
	filename = "main-dish.data"
	f = open(filename,'r')
	data = json.loads(f.read())
	f.close()
	G = nx.Graph()
	choose = random.sample(data.keys(),100)
	for item1,item2 in itertools.combinations(choose,2):
		if len(set(data[item1]['recipe']).intersection(set(data[item2]['recipe'])))>3:
			G.add_edge(item1,item2)
		else :
			G.add_node(item1)
			G.add_node(item2)
	nx.write_gml(G,"main-dish.gml")