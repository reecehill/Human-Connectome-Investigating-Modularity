import matplotlib
import hdf5storage # type: ignore
matplotlib.use('TkAgg',force=True)
from matplotlib import pyplot as plt
from scipy import sparse, io # type: ignore
print("Switched to:",matplotlib.get_backend())

from cdlib import algorithms, viz # type: ignore
import networkx as nx
g = hdf5storage.loadmat('data/subjects/100610/matrices.mat', mdict={1: "adj_matrix1"}, variable_names=["adj_matrix"]) # type: ignore
g = nx.karate_club_graph()  # type: ignore
coms = algorithms.louvain(g)  # type: ignore
viz.plot_community_graph(g, coms) # type: ignore
plt.savefig("./figure.png") # type: ignore
t = 1
# >>> [{0, 1, 2}, {3, 4, 5}]