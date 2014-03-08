import networkx as nx
import json
import itertools

if __name__ == "__main__":
	filename = "breakfast-and-brunch.data"
	f = open(filename,'r')
	data = json.loads(f.read())
	f.close()
	G = nx.Graph()
	for item1,item2 in itertools.combinations(data.keys()[:50],2):
		if set(data[item1]['recipe']).intersection(set(data[item2]['recipe'])):
			G.add_edge(item1,item2)
	nx.write_gml(G,"breakfast-and-brunch.gml")