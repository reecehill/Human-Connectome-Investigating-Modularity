from scipy.optimize import linear_sum_assignment
import numpy as np

# Shared 3D coordinates (C matrix)
C = np.array(
    [
        [0, 0, 0],  # C_1
        [1, 2, 1],  # C_2
        [3, 1, 4],  # C_3
        [5, 5, 5],  # C_4
        [2, 1, 3],  # C_5
        [1, 0, 2],  # C_6
    ]
)

# Categorical labels for X and Y
X_labels = ["A", "A", "A", "B", "A", "C"]  # Labels for X
Y_labels = ["E", "E", "F", "D", "D", "D"]  # Labels for Y

# Step 1: Compute the cost matrix (distance-based cost for relabeling)
# In this case, since the coordinates are shared, we compute the cost as zero if the point is the same
# and add a hypothetical cost if relabeling occurs.
# In this case, we assume that the cost is based on how different X and Y labels are, which we will simplify.
# We'll use a simplified version where differences between X and Y labels are penalized by 1.

# For simplicity, we are not considering coordinates because they are already matched. We use label differences instead.


def compute_cost_matrix(C):
    num_points = C.shape[0]
    cost_matrix = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            # Calculate the Euclidean distance between each pair of points
            cost_matrix[i, j] = np.linalg.norm(C[i] - C[j])
    return cost_matrix


# Calculate cost matrix
cost_matrix = compute_cost_matrix(C)

# Step 2: Apply the Hungarian algorithm to find the optimal relabeling
row_ind, col_ind = linear_sum_assignment(cost_matrix)

# Step 3: Create the new relabeled Y based on the optimal assignment
Y_relabelled = [Y_labels[j] for j in col_ind]


# Show cost matrix and optimal mapping
pass
cost_matrix, optimal_mapping
