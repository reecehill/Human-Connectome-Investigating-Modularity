# NetworkX (Python package is used to calculate network properties.)
from matplotlib.pylab import plot
import numpy as np
from numpy._typing._array_like import NDArray
import numpy.typing as npt
import sklearn
from scipy.io.matlab import loadmat, savemat
from scipy.sparse import random as random_sparse, find
from scipy.sparse._matrix import spmatrix

# from scipy.stats import uniform as uniform_dist
import modules.globals as g
import config
from typing import Any, cast, Union
from networkx import from_scipy_sparse_array, Graph, draw, community as nx_community
import matplotlib.pyplot as plt
import networkx as nx
from multiprocessing import Pool
from collections import deque
from cdlib import algorithms, viz, utils
from cdlib.classes.node_clustering import NodeClustering


def calculateModularity(subjectId: str) -> bool:
    return findModularity(subjectId)


def groupModulesByLabel(x: "npt.NDArray[np.int8]") -> "list[list[np.int8]]":
    x_array = x  # Ensure input is an array of int8
    unique_values = np.unique(x_array)  # Get unique values from the array

    # Prepare the result list for storing sub-arrays
    result: "list[list[np.int8]]" = []

    # Loop through each unique value
    for value in unique_values:
        # Get 1-based indices where the value appears
        indices = np.where(x_array == value)[0].tolist()
        result.append(indices)  # Ensure indices are int8

    # Convert the list of arrays to a 2D array, ensure it's of dtype int8
    return result


def findModularity(subjectId: str) -> bool:
    L_optimalGamma = np.nan
    R_optimalGamma = np.nan
    # TODO: This type is incorrect.
    L_optimalModules: (
        "Union[list[list[np.int8]],NodeClustering,npt.NDArray[np.int8]]"
    ) = []
    R_optimalModules: (
        "Union[list[list[np.int8]],NodeClustering,npt.NDArray[np.int8]]"
    ) = []

    L_graph = from_scipy_sparse_array(getComputedMatrix(subjectId, config.L_MATRIX))
    R_graph = from_scipy_sparse_array(getComputedMatrix(subjectId, config.R_MATRIX))
    g.logger.info(
        f"Running NetworkX: calculating modularity using: {config.NETWORKX_ALGORITHM}."
    )
    if config.NETWORKX_ALGORITHM == "leiden_communities":
        # Using the optimal gamma, find the modules arrangement.
        L_optimalModules = algorithms.leiden(
            g_original=L_graph, weights="weight"
        ).communities  # type: ignore
        R_optimalModules = algorithms.leiden(
            g_original=R_graph, weights="weight"
        ).communities  # type: ignore
    elif config.NETWORKX_ALGORITHM == "bayan":
        L_optimalModules = algorithms.bayan(
            g_original=L_graph, time_allowed=1, resolution=1
        )  # type: ignore
        R_optimalModules = algorithms.bayan(
            g_original=R_graph, time_allowed=1, resolution=1
        ).communities  # type: ignore
    elif config.NETWORKX_ALGORITHM == "frc_fgsn":
        L_optimalModules = algorithms.frc_fgsn(
            g_original=L_graph, theta=1, eps=0.5, r=3000
        ).communities  # type: ignore
        R_optimalModules = algorithms.frc_fgsn(
            g_original=R_graph, theta=1, eps=0.5, r=3000
        ).communities  # type: ignore
    elif config.NETWORKX_ALGORITHM == "principled_clustering":
        L_optimalModules = algorithms.principled_clustering(
            g_original=L_graph, cluster_count=5
        ).communities  # type: ignore
        R_optimalModules = algorithms.principled_clustering(
            g_original=R_graph, cluster_count=5
        ).communities  # type: ignore
    elif config.NETWORKX_ALGORITHM == "scan":
        L_optimalModules = algorithms.scan(
            g_original=L_graph, epsilon=0.2, mu=10
        ).communities  # type: ignore
        R_optimalModules = algorithms.scan(
            g_original=R_graph, epsilon=0.2, mu=10
        ).communities  # type: ignore
    elif config.NETWORKX_ALGORITHM == "louvain_communities":
        # Search parameter space for gamma that yields maximal modularity.
        L_optimalGamma = findOptimalGamma(
            subjectId=subjectId, weighted_matrix=config.L_MATRIX
        )
        R_optimalGamma = findOptimalGamma(
            subjectId=subjectId, weighted_matrix=config.R_MATRIX
        )

        # Using the optimal gamma, find the modules arrangement.
        L_optimalModules, _ = runLouvainAlgorithm(L_graph, L_optimalGamma)
        R_optimalModules, _ = runLouvainAlgorithm(R_graph, R_optimalGamma)

    elif config.NETWORKX_ALGORITHM == "spectral_clustering":
        try:
            L_adj = getComputedMatrix(subjectId, config.L_MATRIX)
            R_adj = getComputedMatrix(subjectId, config.R_MATRIX)
            L_optimalModules_list = sklearn.cluster.spectral_clustering(
                affinity=L_adj, n_clusters=5, assign_labels="discretize"
            )
            L_optimalModules = groupModulesByLabel(
                np.array(L_optimalModules_list, dtype=np.int8).transpose()
            )
            R_optimalModules_list = sklearn.cluster.spectral_clustering(
                affinity=R_adj, n_clusters=5, assign_labels="discretize"
            )
            R_optimalModules = groupModulesByLabel(
                np.array(R_optimalModules_list, dtype=np.int8)
            )

        except Exception as e:
            g.logger.error(f"Failed to run spectral clustering algorithm: {str(e)}")
    elif config.NETWORKX_ALGORITHM == "greedy_modularity_communities":
        # Search parameter space for gamma that yields maximal modularity.
        L_optimalGamma = 0.2
        # L_optimalGamma = findOptimalGamma(subjectId=subjectId, weighted_matrix=config.L_MATRIX)
        R_optimalGamma = 0.2
        # R_optimalGamma = findOptimalGamma(subjectId=subjectId, weighted_matrix=config.R_MATRIX)

        L_optimalModules = [
            list(community)
            for community in nx_community.greedy_modularity_communities(
                L_graph,
                weight="weight",
                resolution=L_optimalGamma,
                cutoff=10,
                best_n=10,
            )
        ]  # type: ignore
        R_optimalModules = [
            list(community)
            for community in nx_community.greedy_modularity_communities(
                R_graph,
                weight="weight",
                resolution=R_optimalGamma,
                cutoff=10,
                best_n=10,
            )
        ]  # type: ignore
    elif config.NETWORKX_ALGORITHM == "fast_label_propagation_communities":
        L_optimalModules_gen = nx_community.fast_label_propagation_communities(
            L_graph, weight="weight"
        )  # type: ignore
        L_optimalModules = np.array(
            [
                list(community)
                for community in deque(L_optimalModules_gen, maxlen=len(L_graph))
            ]
        )
        R_optimalModules_gen = nx_community.fast_label_propagation_communities(
            R_graph, weight="weight"
        )  # type: ignore
        R_optimalModules = np.array(
            [
                list(community)
                for community in deque(R_optimalModules_gen, maxlen=len(R_graph))
            ]
        )
    elif config.NETWORKX_ALGORITHM == "async_fluid":
        L_optimalModules = algorithms.async_fluid(L_graph, k=config.NETWORKX_FLUID_K)
        R_optimalModules = algorithms.async_fluid(R_graph, k=config.NETWORKX_FLUID_K)
    elif config.NETWORKX_ALGORITHM == "girvan_newman":
        L_optimalModules_gen = nx_community.girvan_newman(L_graph)  # type: ignore
        L_optimalModules = np.array(
            [
                list(community)
                for community in deque(L_optimalModules_gen, maxlen=len(L_graph))
            ]
        )
        R_optimalModules_gen = nx_community.girvan_newman(R_graph)  # type: ignore
        R_optimalModules = np.array(
            [
                list(community)
                for community in deque(R_optimalModules_gen, maxlen=len(R_graph))
            ]
        )
    elif config.NETWORKX_ALGORITHM == "k_clique_communities":
        L_optimalModules_gen = nx_community.k_clique_communities(
            L_graph, k=3, cliques=nx.find_cliques(L_graph)
        )  # type: ignore
        L_optimalModules = np.array(
            [
                list(community)
                for community in deque(L_optimalModules_gen, maxlen=len(L_graph))
            ]
        )
        R_optimalModules_gen = nx_community.k_clique_communities(
            R_graph, k=3, cliques=nx.find_cliques(R_graph)
        )  # type: ignore
        R_optimalModules = np.array(
            [
                list(community)
                for community in deque(R_optimalModules_gen, maxlen=len(R_graph))
            ]
        )
    else:
        g.logger.info(
            "ERROR: Running NetworkX: community detection algorithm incorrectly set."
        )
        raise ValueError("Incorrect networkx algorithm specified.")

    # Save data.
    savemat(
        config.SUBJECT_DIR / "optimal_struc_modules.mat",
        {
            "modules": {
                "left_structural": np.array(L_optimalModules, dtype=object),
                "right_structural": np.array(R_optimalModules, dtype=object),
            },
            "optimal_gamma": {
                "left_structural": L_optimalGamma,
                "right_structural": R_optimalGamma,
            },
        },
    )
    return True


def convertMatlabDataToPython(subjectId: str) -> bool:

    return True


def getComputedMatrix(subjectId: str, weighted_matrix: str) -> spmatrix:
    # Get computed adjacency matrix
    try:
        matrices = loadmat(config.SUBJECT_DIR / "matrices.mat")  # type: ignore
        matrix: spmatrix = matrices[weighted_matrix]  # variable in mat file
    except Exception as e:
        g.logger.error(f"Failed to load computed matrix: {str(e)}")
        raise ValueError("Failed to load computed matrix")
    return matrix


def process_iteration(args: "tuple[np.float64,int,Graph,str]") -> "np.float64":
    gamma, iteration_index, graph, graph_type = args
    g.logger.info(
        f"Sorting {graph_type} (ROI) into modules: gamma={gamma}, iteration #{iteration_index}/{config.NETWORKX_ITERATION_COUNT}"
    )
    # initialize modularity values
    q0 = np.float64(-1)
    q1 = np.float64(0)
    while q1 - q0 > 1e-5:  # while modularity increases, perform community detection
        q0 = q1
        _, q1 = runLouvainAlgorithm(graph, gamma)
    # return the modularity score for storage into either Q_corts or Q_rands.
    return q1


def findOptimalGamma(subjectId: str, weighted_matrix: str) -> np.float64:
    g.logger.info("Running NetworkX: finding optimal gamma.")
    all_gammas = cast(
        "npt.NDArray[np.float64]",
        np.arange(
            config.NETWORKX_GAMMA_START,
            config.NETWORKX_GAMMA_END,
            config.NETWORKX_GAMMA_STEP,
        ),
    )
    all_iterations = range(1, config.NETWORKX_ITERATION_COUNT)

    # Q_corts: np_typing.NDArray[np.float64] = np.zeros((max(all_iterations),1), dtype=np.float64)
    # Q_rands = cast('list[np.float64]', np.zeros((max(all_iterations),1)))
    Q_max = cast("list[np.float64]", np.zeros(len(all_gammas)))

    # Get computed adjacency matrix
    computed_matrix: spmatrix = getComputedMatrix(subjectId, weighted_matrix)
    G_corts: Graph = cast(Graph, from_scipy_sparse_array(computed_matrix))

    # Create random adjacency matrix
    number_of_edges_to_create: np.int32 = computed_matrix.getnnz()
    # number_of_edges_to_create: np.int32 = computed_matrix.nnz
    numel_adj_matrix: np.int32 = computed_matrix.shape[0] * computed_matrix.shape[1]
    density_of_random_matrix = float(number_of_edges_to_create / numel_adj_matrix)
    random_matrix: spmatrix = random_sparse(
        m=computed_matrix.shape[0],
        n=computed_matrix.shape[1],
        density=density_of_random_matrix,
        random_state=np.random.default_rng(),
        data_rvs=np.ones,
        dtype="int8",
    )  # TODO: The random matrix is sampled from a uniform distribution to produce only binary matrix.
    G_rand: Graph = from_scipy_sparse_array(random_matrix)

    # Trial all iterations for cortical data...
    with Pool() as pool:
        for gamma in all_gammas:
            gamma = cast(np.float64, gamma)
            # TODO: The Q_corts are not being stored correctly.
            Q_corts = pool.map(
                process_iteration,
                [
                    (gamma, iteration_index, G_corts, "cortical")
                    for iteration_index in all_iterations
                ],
            )
            Q_rands = pool.map(
                process_iteration,
                [
                    (gamma, iteration_index, G_rand, "random")
                    for iteration_index in all_iterations
                ],
            )

            Q_corts_mean: np.float64 = np.mean(Q_corts)
            Q_rand_mean: np.float64 = np.mean(Q_rands)
            gamma_index: np.int32 = np.where(all_gammas == gamma)[0][0]
            Q_max[gamma_index] = Q_corts_mean - Q_rand_mean

    # Gamma that returned the largest modularity
    optimal_gamma = all_gammas[np.argmax(Q_max)]

    return optimal_gamma


def runLouvainAlgorithm(
    graph: Graph, gamma: np.float64
) -> "tuple[npt.NDArray[np.int8] | NodeClustering, np.float64]":
    if config.NETWORKX_ALGORITHM == "louvain_communities":
        communities: "list[set[int]]" = nx_community.louvain_communities(
            graph, weight="weight", resolution=gamma
        )  # type: ignore
    elif config.NETWORKX_ALGORITHM == "greedy_modularity_communities":
        communities: "list[set[int]]" = nx_community.greedy_modularity_communities(
            graph, weight="weight", resolution=gamma
        )  # type: ignore
    else:
        g.logger.error(
            f"Invalid NetworkX algorithm: {config.NETWORKX_ALGORITHM}. Expected 'louvain_communities' or 'greedy_modularity_communities'."
        )
        raise ValueError("Incorrect networkx algorithm specified.")
    communities_list: "npt.NDArray[np.int8]" = np.array(
        [list(community) for community in communities], dtype=object
    )
    modularity = nx_community.modularity(graph, communities)  # type: ignore
    return communities_list, modularity


def main() -> bool:
    g.logger.warn("Calculating modularity for subject 100307 only.")
    return calculateModularity("100307")
