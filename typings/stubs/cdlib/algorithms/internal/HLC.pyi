"""
This type stub file was generated by pyright.
"""

def get_sorted_edge(a, b): # -> tuple[Any, ...]:
    ...

def HLC_read_edge_list_unweighted(g): # -> tuple[dict[Any, set[Any]], set[Any]]:
    ...

def HLC_read_edge_list_weighted(g): # -> tuple[dict[Any, set[Any]], set[Any], dict[Any, Any]]:
    ...

class HLC:
    @staticmethod
    def get_sorted_pair(a, b): # -> tuple[Any, ...]:
        ...
    
    @staticmethod
    def sort_edge_pairs_by_similarity(adj_list_dict): # -> list[Any]:
        ...
    
    def __init__(self, adj_list_dict, edges) -> None:
        ...
    
    def single_linkage(self, threshold=..., w=..., dendro_flag=...): # -> tuple[dict[Any, Any], float] | tuple[dict[Any, Any] | None, float, float, list[tuple[float, float]], dict[Any, Any], list[Any]] | tuple[dict[Any, Any] | None, float, float, list[tuple[float, float]]]:
        ...
    


def sort_edge_pairs_by_similarity_weighted(adj_list_dict, edge_weight_dict): # -> list[Any]:
    ...
