"""
This type stub file was generated by pyright.
"""

class FuncTag:
    def __init__(self) -> None:
        ...
    
    exp_inv_mul_tag = ...
    mul_tag = ...
    min_tag = ...
    max_tag = ...


def get_coefficient_func(tag: str) -> float:
    ...

def cal_modularity(input_graph, comm_result): # -> float:
    ...

class LinkBelongModularity:
    PRECISION = ...
    def __init__(self, input_graph, comm_result, coefficient_func) -> None:
        """
        :type input_graph: nx.Graph
        """
        ...
    
    def init_belong_weight_dict(self): # -> None:
        ...
    
    def init_degree_dicts(self): # -> None:
        ...
    
    def calculate_modularity(self) -> float:
        ...
    

