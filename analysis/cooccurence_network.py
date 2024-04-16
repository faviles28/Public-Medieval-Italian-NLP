import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import ast
import numpy as np
import community as community_louvain
from matplotlib.colors import LinearSegmentedColormap, to_rgba

def create_cooccurrence_network(csv_filename, top_n=100, target_words=None):
    df = pd.read_csv(csv_filename)
    
    # If a list of target words is specified, filter the DataFrame to include only the rows
    # where any of the target words appears in the 'Word Pair' column.
    if target_words:
        def filter_by_target_words(row):
            word_pair = ast.literal_eval(row['Word Pair'])
            return any(word in word_pair for word in target_words)
        
        df = df[df.apply(filter_by_target_words, axis=1)]
    
    sorted_df = df.sort_values(by='Count', ascending=False).head(top_n)
    
    G = nx.Graph()
    for _, row in sorted_df.iterrows():
        word_pair = ast.literal_eval(row['Word Pair'])
        weight = row['Count']
        G.add_edge(word_pair[0], word_pair[1], weight=weight)
    
    # Community detection
    partition = community_louvain.best_partition(G)
    
    # Node sizes based on the sum of counts for edges connected to each node
    node_weights = {node: sum(weight for _, _, weight in G.edges(node, data='weight')) for node in G.nodes()}
    
    # Normalize node sizes for visualization purposes
    min_size = 100
    max_size = 5000
    min_weight = min(node_weights.values())
    max_weight = max(node_weights.values())
    node_sizes = [((node_weights[node] - min_weight) / (max_weight - min_weight) * (max_size - min_size) + min_size) for node in G.nodes()]
    
    fig, ax = plt.subplots()
    pos = nx.kamada_kawai_layout(G)
    
    light_gray = '#e0e0e0'
    original_cmap = plt.cm.viridis
    light_cmap = LinearSegmentedColormap.from_list("lighter_viridis", [
        to_rgba(light_gray, alpha=0.8),
        original_cmap(0.5),
        original_cmap(1.0)
    ])
    
    # Draw the network
    community_colors = [partition[node] for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=community_colors, cmap=light_cmap, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='blue', alpha=0.5)
    
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=12)
    
    plt.axis('off')
    cmap = light_cmap
    norm = plt.Normalize(vmin=min(community_colors), vmax=max(community_colors))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.5, aspect=5, label='Community')
    
    plt.show()

targets = [
    'amore',
    'affetto',
    'letizia',
    'vita',
    'raggiare',
    'stella',
    'virtù',
    'notte',
    'creatura',
    'raggio'
]

targets2 = [
    'amore',
    'Beatrice',
    'core',
    'amare',
    'affetto',
    'dolce',
    'bello',
    'bellezza',
    'donna',
    'sposa',
    'disio',
    'carne'
]

targets = [
    'amore',
    'affetto',
    'letizia',
    'vita',
    'raggiare',
    'stella',
    'virtù',
    'notte',
    'creatura',
    'raggio'
]

csv_file_path = '../texts/Decameron/analysis/cooccurrence_matrix_X.csv'
create_cooccurrence_network(csv_file_path, top_n=150, target_words=None)
