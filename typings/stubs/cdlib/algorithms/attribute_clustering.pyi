"""
This type stub file was generated by pyright.
"""

from cdlib import AttrNodeClustering

__all__ = ["eva", "ilouvain"]
def eva(g_original: object, labels: dict, weight: str = ..., resolution: float = ..., alpha: float = ...) -> AttrNodeClustering:
    """
    The Eva algorithm extends the Louvain approach in order to deal with the attributes of the nodes (aka Louvain Extended to Vertex Attributes).
    It optimizes - combining them linearly - two quality functions, a structural and a clustering one, namely Newman's modularity and purity, estimated as the product of the frequencies of the most frequent labels carried by the nodes within the communities.
    A parameter alpha tunes the importance of the two functions: an high value of alpha favors the clustering criterion instead of the structural one.


    **Supported Graph Types**

    ========== ======== ======== ======== ==============
    Undirected Directed Weighted Temporal Node Attribute
    ========== ======== ======== ======== ==============
    Yes        No       No       No       Yes
    ========== ======== ======== ======== ==============

    :param g_original: a networkx/igraph object
    :param labels: dictionary specifying for each node (key) a dict (value) specifying the name attribute (key) and its value (value)
    :param weight: str, optional the key in graph to use as weight. Default to 'weight'
    :param resolution: double, optional  Will change the size of the communities, default to 1.
    :param alpha: float, assumed in [0,1], optional Will tune the importance of modularity and purity criteria, default to 0.5
    :return: AttrNodeClustering object

    :Example:

    >>> from cdlib.algorithms import eva
    >>> import networkx as nx
    >>> import random
    >>> l1 = ['A', 'B', 'C', 'D']
    >>> l2 = ["E", "F", "G"]
    >>> g_attr = nx.barabasi_albert_graph(100, 5)
    >>> labels=dict()
    >>> for node in g_attr.nodes():
    >>>    labels[node]={"l1":random.choice(l1), "l2":random.choice(l2)}
    >>> communities = eva(g_attr, labels, alpha=0.8)

    :References:

    Citraro, S., & Rossetti, G. (2019, December). Eva: Attribute-Aware Network Segmentation. In International Conference on Complex Networks and Their Applications (pp. 141-151). Springer, Cham.

    .. note:: Reference implementation: https://github.com/GiulioRossetti/Eva/tree/master/Eva
    """
    ...

def ilouvain(g_original: object, labels: dict) -> AttrNodeClustering:
    """
    The I-Louvain algorithm extends the Louvain approach in order to deal only with the scalar attributes of the nodes.
    It optimizes Newman's modularity combined with an entropy measure.


    **Supported Graph Types**

    ========== ======== ======== ======== ==============
    Undirected Directed Weighted Temporal Node Attribute
    ========== ======== ======== ======== ==============
    Yes        No       No       No       Yes
    ========== ======== ======== ======== ==============

    :param g_original: a networkx/igraph object
    :param labels: dictionary specifying for each node (key) a dict (value) specifying the name attribute (key) and its value (value)
    :return: AttrNodeClustering object

    :Example:

    >>> from cdlib.algorithms import ilouvain
    >>> import networkx as nx
    >>> import random
    >>> l1 = [0.1, 0.4, 0.5]
    >>> l2 = [34, 3, 112]
    >>> g_attr = nx.barabasi_albert_graph(100, 5)
    >>> labels=dict()
    >>> for node in g_attr.nodes():
    >>>    labels[node]={"l1":random.choice(l1), "l2":random.choice(l2)}
    >>> id = dict()
    >>> for n in g.nodes():
    >>>     id[n] = n
    >>> communities = ilouvain(g_attr, labels, id)

    :References:

    Combe D., Largeron C., Géry M., Egyed-Zsigmond E. "I-Louvain: An Attributed Graph Clustering Method". <https://link.springer.com/chapter/10.1007/978-3-319-24465-5_16> In: Fromont E., De Bie T., van Leeuwen M. (eds) Advances in Intelligent Data Analysis XIV. IDA (2015). Lecture Notes in Computer Science, vol 9385. Springer, Cham

    """
    ...
