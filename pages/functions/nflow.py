import networkx as nx
import matplotlib.pyplot as plt

def create_flow_network(manifest, containers):
    # Create a directed graph
    G = nx.DiGraph()

    # Adding a source and sink node
    source = 'Ledger'
    sink = 'TEU'
    G.add_node(source)
    G.add_node(sink)

    # Add item nodes and connect them to the source with their volume as capacity
    for item, volume in manifest.items():
        G.add_edge(source, item, capacity=volume)

    # Add container nodes and connect them to the sink with their capacity as edge capacity
    for container, capacity in containers.items():
        G.add_edge(container, sink, capacity=capacity)

    # Connect every item to every container with infinite capacity
    for item in manifest:
        for container in containers:
            G.add_edge(item, container, capacity=float('inf'))

    return G

def display_graph(G):
    # create matplotlibn figure
    fig, ax = plt.subplots(figsize=(10, 8))
    # calculate the position of the nodes
    pos = nx.spring_layout(G)
    # draw the network
    edge_labels = {(n1, n2): d['capacity'] for n1, n2, d in G.edges(data=True)}
    nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    return fig