# pyright: reportUndefinedVariable=false,reportUnusedImport=false,reportMissingTypeStubs=false,reportUnknownMemberType=false,reportUnknownVariableType=false,reportUnknownArgumentType=false

# NetworkX (Python package is used to calculate network properties.)
import numpy as np
import numpy.typing as np_typing
from scipy.io import loadmat, savemat
from scipy.sparse import random as random_sparse, spmatrix
from scipy.stats import uniform as uniform_dist
import modules.globals as g
import config
from typing import Literal, cast
from networkx import from_scipy_sparse_array, Graph, community as nx_community
from multiprocessing import Pool
def convertMatlabDataToPython(subjectId: str) -> bool:
  
  return True
def process_iteration(args: 'tuple[np.float64,int,Graph,str,list[np.float64]]') -> None:
    gamma, iteration_index, graph, graph_type, Q_store = args
    g.logger.info(f'Sorting {graph_type} (ROI) into modules: gamma={gamma}, iteration #{iteration_index}/{config.NETWORKX_ITERATION_COUNT}')
    gamma: np.float64 = np.float64(gamma)
    # initialize modularity values
    q0 = np.float64(-1)
    q1 = np.float64(0)
    while q1 - q0 > 1e-5: # while modularity increases, perform community detection
        q0 = q1
        _, q1 = runLouvainAlgorithm(graph, gamma)
    # store the modularity score into either Q_corts or Q_rands.
    Q_store[iteration_index-1] = q1 

def getComputedMatrix(subjectId: str, weighted_matrix: str) -> spmatrix:
   # Get computed adjacency matrix
  subjectFolder = config.DATA_DIR / 'subjects' / subjectId
  matrices = loadmat(subjectFolder / 'matrices.mat') # type: ignore
  matrix: spmatrix = matrices[weighted_matrix]  # variable in mat file 
  return matrix
  
def findOptimalGamma(subjectId: str, weighted_matrix: str) -> np.float64:
  g.logger.info("Running NetworkX: finding optimal gamma.")
  all_gammas = cast('list[np.float64]',np.arange(config.NETWORKX_GAMMA_START, config.NETWORKX_GAMMA_END, config.NETWORKX_GAMMA_STEP))
  all_iterations = range(1, config.NETWORKX_ITERATION_COUNT)

  Q_corts = cast('list[np.float64]', np.zeros(max(all_iterations)))
  Q_rands = cast('list[np.float64]',np.zeros(max(all_iterations)))
  Q_max = cast('list[np.float64]',np.zeros(len(all_gammas)))

 # Get computed adjacency matrix
  computed_matrix: spmatrix = getComputedMatrix(subjectId, weighted_matrix)
  G_corts: Graph = cast(Graph, from_scipy_sparse_array(computed_matrix))


  # Create random adjacency matrix
  number_of_edges_to_create: np.int32 = computed_matrix.nnz
  numel_adj_matrix: np.int32 = computed_matrix.shape[0]*computed_matrix.shape[1]
  density_of_random_matrix = np.float64(number_of_edges_to_create / numel_adj_matrix)
  random_matrix: spmatrix = random_sparse(
    m=computed_matrix.shape[0],
    n=computed_matrix.shape[1],
    density=density_of_random_matrix,
    format='csr',
    random_state=np.random.default_rng(),
    data_rvs=np.ones,
    dtype='int8')  #TODO: The random matrix is sampled from a uniform distribution to produce only binary matrix.
  G_rand: Graph = cast(Graph, from_scipy_sparse_array(random_matrix))
 
  # Trial all iterations for cortical data...
  with Pool() as pool:
      for gamma in all_gammas:
          pool.map(process_iteration, [(gamma, iteration_index, G_corts, 'cortical', Q_corts) for iteration_index in all_iterations])
          pool.map(process_iteration, [(gamma, iteration_index, G_rand, 'random', Q_rands) for iteration_index in all_iterations])

          Q_corts_mean: np.float64 = np.mean(Q_corts)
          Q_rand_mean: np.float64 = np.mean(Q_rands)
          gamma_index: np.int32 = np.where(np.array(all_gammas) == gamma)[0][0]
          Q_max[gamma_index] = Q_corts_mean - Q_rand_mean

  # Gamma that returned the largest modularity
  optimal_gamma = all_gammas[np.argmax(Q_max)]

  return optimal_gamma

def runLouvainAlgorithm(graph: Graph, gamma: np.float64) -> 'tuple[list[list[int]], np.float64]':
  g.logger.info("Running NetworkX: calculating modularity using Louvain algorithm.")
  communities: 'list[set[int]]' = nx_community.louvain_communities(graph, resolution=gamma, seed=123) # type: ignore
  communities_list: 'ndarray[list[int]]' = np.array([list(community) for community in communities], dtype=object)
  modularity = nx_community.modularity(graph, communities) # type: ignore
  return communities_list, modularity

def findModularity(subjectId: str) -> bool:
  # Search parameter space for gamma that yields maximal modularity.
  L_optimalGamma = findOptimalGamma(subjectId=subjectId, weighted_matrix="adj_matrix_wei_roiL")
  R_optimalGamma = findOptimalGamma(subjectId=subjectId, weighted_matrix="adj_matrix_wei_roiR")

  # Using the optimal gamma, find the modules arrangement.
  L_optimalModules, _ = runLouvainAlgorithm(
    from_scipy_sparse_array(
      getComputedMatrix(subjectId,"adj_matrix_wei_roiL")
      ),
    L_optimalGamma)
  R_optimalModules, _ = runLouvainAlgorithm(
    from_scipy_sparse_array(
      getComputedMatrix(subjectId,"adj_matrix_wei_roiR")
      ),
    R_optimalGamma)

  # Save data.
  subjectFolder = config.DATA_DIR / 'subjects' / subjectId
  savemat(subjectFolder / "optimal_modules.mat", {
    'modules': {
      'left_structural': L_optimalModules,
      'right_structural': R_optimalModules,
    },
    'optimal_gamma': {
      'left_structural': L_optimalGamma,
      'right_structural': R_optimalGamma,
    }
  }
          )
  
  return True

def main()  -> bool:
  return findModularity('100307')