import networkx as nx
import matplotlib.pyplot as plt
import imageio as io
import random
import numpy as np

# import os

seed = 123
random.seed(seed)
np.random.seed(seed)
filename = ""
images = []

G = nx.DiGraph()
G.add_node("node 1")
G.add_node("node 2")
G.add_node("node 3")
G.add_node("node 4")

pos = nx.kamada_kawai_layout(G)

for i in range (5):
    tmp_G = G.copy() 
    node_sizes = [10, 100, 1000, i * 1000]# altering the size of node 4 over time
    nx.draw(tmp_G, pos=pos, with_labels=True, node_size = node_sizes)
    filename = "image_files/filename" + str(i) +".png"
    plt.savefig(filename)
    images.append(io.imread(filename))
    plt.clf()
    tmp_G.clear()

    # G.add_nodes_from(["node 1", "node 2", "node 3"], node_size=3)
    # G.add_nodes_from(["node 1", "node 2", "node 3"], node_size=3)
    # G.add_node("node 4", node_size=100)
    # G.add_edge("node 1", "node 2")
    # G.add_edge("node 3", "node 4")
    # node_sizes = [10, 100, 1000, i * 1000]
    # nx.draw(G, with_labels=True, node_size = node_sizes)
    # filename = "image_files/filename" + str(i) +".png"
    # plt.savefig(filename)
    # images.append(io.imread(filename))
    # plt.clf()
    # G.clear()
io.mimsave('movie.gif', images)


# with imageio.get_writer('movie.gif', mode = 'I') as writer:
#     for file in 
#         image = imageio.imread(filename)


# G.add_nodes_from(["node 1", "node 2", "node 3"], node_size=3)
# G.add_node("node 4", node_size=100)
# G.add_edge("node 1", "node 2")
# G.add_edge("node 3", "node 4")
# node_sizes = [10, 100, 1000, 4000]
# nx.draw(G, with_labels=True, node_size = node_sizes)
# plt.savefig("image_files/filename.png")
# plt.show()