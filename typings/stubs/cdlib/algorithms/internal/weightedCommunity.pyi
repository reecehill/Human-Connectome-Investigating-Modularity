"""
This type stub file was generated by pyright.
"""

__authors__ = ...
class weightedCommunity:
    def __init__(self, G, min_bel_degree, threshold_bel_degree, weightName=..., save=..., outfile_name=...) -> None:
        """
        Constructor

        :param G: an igraph.Graph object
        :param min_bel_degree: the tolerance, in terms of beloging degree, required in order to add a node in a community
        :param threshold_bel_degree: the tolerance, in terms of beloging degree, required in order to add a node in a 'NLU' community
        :param weightName: Name of the attribute containing the weights
        """
        ...
    
    def strength(self, node): # -> Literal[0]:
        ...
    
    def belonging_degree(self, node, community): # -> float:
        ...
    
    def modularity(self): # -> float:
        ...
    
    def allStrengths(self): # -> None:
        ...
    
    def strongestNotLabeled(self):
        ...
    
    def nodesRemotion(self, c, min_bel_degree):
        ...
    
    def initialCommunityDetection(self): # -> set[Any]:
        ...
    
    def find_initial_community_neighbors(self, c): # -> set[Any]:
        ...
    
    def define_nu_nlu(self, c, c_neighbors): # -> tuple[set[Any], set[Any]]:
        """### Find Nu (b > 0.5) and Nlu (0.4 < b < 0.5) starting from the set of neighbors"""
        ...
    
    def add_nlu_to_community(self, c, nlu):
        ...
    
    def expandCommunity(self, c): # -> Literal[-1]:
        """##  Expanding the community"""
        ...
    
    def getCommunities(self): # -> list[Any]:
        ...
    
    def computeCommunity(self): # -> None:
        ...
    
    def computeCommunities(self): # -> list[Any]:
        ...
    

