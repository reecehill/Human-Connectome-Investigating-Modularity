"""
This type stub file was generated by pyright.
"""

import scipy.sparse as sp
import networkx as nx

__all__ = ["detect_belief_communities"]
def get_degree_vector(g: nx.Graph): # -> csr_matrix:
    ...

def init_beliefs(q: int, g: nx.Graph): # -> csr_matrix:
    ...

def init_messages(q: int, g: nx.Graph): # -> Any:
    ...

def compute_theta(beliefs: sp.csr_matrix, degrees: sp.csr_matrix): # -> _NotImplementedType | ndarray[Any, dtype[Any]] | ndarray[Any, Any] | matrix[Any, Any]:
    ...

def update_matrix(g: nx.Graph):
    ...

def belief_matrix(g: nx.Graph):
    ...

def get_external_field_beliefs(theta: sp.csr_matrix, g: nx.Graph, beta: float): # -> float | NDArray[floating[Any]] | matrix[Any, Any]:
    ...

def external_field_update_matrix(g: nx.Graph, beta: float, q: int):
    ...

def get_external_field(theta: sp.csr_matrix, ext_update: sp.csr_matrix):
    ...

def run_bp_community_detection(g: nx.Graph, q: int = ..., beta: float = ..., max_it: int = ..., eps: float = ..., reruns_if_not_conv: int = ...): # -> tuple[Any | csr_matrix, list[Any], int, Any | int, bool]:
    ...

def compute_opt_beta(q: int, c: int): # -> float:
    ...

def detect_belief_communities(g: nx.Graph, max_it: int = ..., eps: float = ..., reruns_if_not_conv: int = ..., threshold: float = ..., q_max: int = ...): # -> list[list[Any]]:
    ...

def prepare_coms(g, cms): # -> list[list[Any]]:
    ...
