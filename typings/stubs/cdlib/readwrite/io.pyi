"""
This type stub file was generated by pyright.
"""

from cdlib import LifeCycle

__all__ = ["write_community_csv", "read_community_csv", "write_community_json", "read_community_json", "read_community_from_json_string", "write_lifecycle_json", "read_lifecycle_json"]
def write_community_csv(communities: object, path: str, delimiter: str = ..., compress: bool = ...): # -> None:
    """
    Save community structure to comma separated value (csv) file.

    :param communities: a NodeClustering object
    :param path: output filename
    :param delimiter: column delimiter
    :param compress: wheter to copress the csv, default False

    :Example:

    >>> import networkx as nx
    >>> from cdlib import algorithms, readwrite
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> readwrite.write_community_csv(coms, "communities.csv", ",")

    """
    ...

def read_community_csv(path: str, delimiter: str = ..., nodetype: type = ..., compress: bool = ...) -> object:
    """
    Read community list from comma separated value (csv) file.

    :param path: input filename
    :param delimiter: column delimiter
    :param nodetype: specify the type of node labels, default str
    :param compress: wheter the file is compressed or not, default False
    :return: NodeClustering object

    :Example:

    >>> import networkx as nx
    >>> from cdlib import algorithms, readwrite
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> readwrite.write_community_csv(coms, "communities.csv", ",")
    >>> coms = readwrite.read_community_csv(coms, "communities.csv", ",", str)

    """
    ...

def write_community_json(communities: object, path: str, compress: bool = ...): # -> None:
    """
    Generate a JSON representation of the clustering object

    :param communities: a cdlib clustering object
    :param path: output filename
    :param compress: wheter to copress the JSON, default False
    :return: a JSON formatted string representing the object

    :Example:

    >>> import networkx as nx
    >>> from cdlib import algorithms, readwrite
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> readwrite.write_community_json(coms, "communities.json")
    """
    ...

def read_community_json(path: str, compress: bool = ...) -> object:
    """
    Read community list from JSON file.

    :param path: input filename
    :param compress: wheter the file is in a copress format, default False
    :return: a Clustering object

    :Example:

    >>> import networkx as nx
    >>> from cdlib import algorithms, readwrite
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> readwrite.write_community_json(coms, "communities.json")
    >>> readwrite.read_community_json(coms, "communities.json")
    """
    ...

def read_community_from_json_string(json_repr: str) -> object:
    """
    Read community list from JSON file.

    :param json_repr: json community representation
    :return: a Clustering object

    :Example:

    >>> import networkx as nx
    >>> from cdlib import algorithms, readwrite
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> readwrite.write_community_json(coms, "communities.json")
    """
    ...

def write_lifecycle_json(lifecycle: LifeCycle, path: str, compress: bool = ...): # -> None:
    """
    Save lifecycle structure to JSON file.

    :param lifecycle: a LifeCycle object
    :param path: output filename
    :param compress: wheter to copress the JSON, default False
    :return: a JSON formatted string representing the object

    :Example:

    >>> from cdlib import LifeCycle, TemporalClustering
    >>> from cdlib import algorithms
    >>> from networkx.generators.community import LFR_benchmark_graph
    >>> from cdlib.readwrite import write_lifecycle_json, read_lifecycle_json
    >>> tc = TemporalClustering()
    >>> for t in range(0, 10):
    >>>     g = LFR_benchmark_graph(
    >>>             n=250,
    >>>             tau1=3,
    >>>             tau2=1.5,
    >>>             mu=0.1,
    >>>             average_degree=5,
    >>>             min_community=20,
    >>>             seed=10,
    >>>     )
    >>>     coms = algorithms.louvain(g)  # here any CDlib algorithm can be applied
    >>>     tc.add_clustering(coms, t)
    >>>
    >>> events = LifeCycle(tc)
    >>> events.compute_events("facets")
    >>> write_lifecycle_json(events, "lifecycle.json")
    """
    ...

def read_lifecycle_json(path: str, compress: bool = ...) -> object:
    """
    Read lifecycle from JSON file.

    :param path: input filename
    :param compress: wheter the file is in a copress format, default False
    :return: a LifeCycle object

    :Example:

    >>> from cdlib import LifeCycle, TemporalClustering
    >>> from cdlib import algorithms
    >>> from networkx.generators.community import LFR_benchmark_graph
    >>> from cdlib.readwrite import write_lifecycle_json, read_lifecycle_json
    >>> tc = TemporalClustering()
    >>> for t in range(0, 10):
    >>>     g = LFR_benchmark_graph(
    >>>             n=250,
    >>>             tau1=3,
    >>>             tau2=1.5,
    >>>             mu=0.1,
    >>>             average_degree=5,
    >>>             min_community=20,
    >>>             seed=10,
    >>>     )
    >>>     coms = algorithms.louvain(g)  # here any CDlib algorithm can be applied
    >>>     tc.add_clustering(coms, t)
    >>>
    >>> events = LifeCycle(tc)
    >>> events.compute_events("facets")
    >>> write_lifecycle_json(events, "lifecycle.json")
    >>> events = read_lifecycle_json("lifecycle.json")

    """
    ...
