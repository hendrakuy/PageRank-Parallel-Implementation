import networkx as nx
import matplotlib.pyplot as plt
import json

def load_graph_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def visualize_graph(adjacency_list):
    G = nx.DiGraph()    
    for page, links in adjacency_list.items():
        for link in links:
            G.add_edge(page, link)

    plt.figure(figsize=(12, 12))
    nx.draw(G, with_labels=True, node_size=700, node_color='lightblue', edge_color='gray', font_size=8)
    plt.title("Graph Keterhubungan Web")
    plt.show()

if __name__ == "__main__":
    adjacency_list = load_graph_from_json('crawled_site_data.json')
    visualize_graph(adjacency_list)
