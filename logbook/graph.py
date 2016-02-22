import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

def graph_from_triples(triples, name="Logbook Activity"):
    """
    Returns a NetworkX graph from a collection of SPOs.
    Expects that a triple is a Triple namedtuple, and that the entity, action
    and detail objects are all hashable. Will add properties to the edge and
    entity as well.
    """
    G = nx.Graph(name=name)
    for triple in triples:
        if not G.has_node(triple.entity):
            G.add_node(triple.entity, name=triple.entity.name, email=triple.entity.email, entity='person')

        if not G.has_node(triple.detail):
            G.add_node(triple.detail, name=triple.detail.detail, entity='entity')

        G.add_edge(
            triple.entity, triple.detail,
            action=triple.action, date=triple.action.date, label=triple.action.action
        )

    return G


def draw_activity_graph(G, layout='spring', **kwargs):
    """
    Helper function for drawing a DDL activity graph.
    """
    if kwargs.pop('connected', False):
        G = max(nx.connected_component_subgraphs(G), key=len)
    
    cmap = {
        'person': '#67C5C2',
        'entity': '#C84127',
    }

    draw = {
        'circular': nx.draw_circular,
        'random': nx.draw_random,
        'spectral': nx.draw_spectral,
        'spring': nx.draw_spring,
        'shell': nx.draw_shell,
        'graphviz': nx.draw_graphviz,
    }[layout]

    sizes  = [50 if n[1]['entity'] == 'entity' else 20 for n in G.nodes_iter(data=True)]
    colors = [cmap[n[1]['entity']] for n in G.nodes_iter(data=True)]

    defaults = {
        'with_labels':False,
        'node_size':sizes, 'node_color':colors,
        'edge_cmap': "#222222",
        'alpha': 0.75,
    }
    defaults.update(kwargs)

    fig = plt.figure(figsize=(16,16))
    plt.title(G.name)
    return draw(G, **defaults)


def info(G):
    """
    Wrapper for nx.info with some other helpers.
    """
    actions = Counter()
    for src, dst, data in G.edges_iter(data=True):
        actions[data['label']] += 1

    output  = [""]
    output.append("Number of Actions: {}".format(len(actions)))
    output.append("Number of Pairwise Comparisons: {}".format(nx.number_of_nodes(G) ** 2))
    output.extend(["", "Action Counts", "-------------"])

    for action, count in actions.most_common():
        output.append("{}: {}".format(action, count))

    return nx.info(G) + "\n".join(output)

if __name__ == '__main__':
    import os
    from reader import LogReader
    fixture = os.path.join(os.path.dirname(__file__), "..", "fixtures", "activity.csv")
    G = graph_from_triples(LogReader(fixture))
    print nx.info(G)
