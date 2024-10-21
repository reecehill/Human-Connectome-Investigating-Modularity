from types import FunctionType
from typing import Any, Callable, Optional, Union
from sklearn.metrics import mutual_info_score, normalized_mutual_info_score, adjusted_mutual_info_score
from sklearn.metrics import v_measure_score, homogeneity_score, adjusted_rand_score, fowlkes_mallows_score
import numpy as np
import numpy.typing as npt
import pandas as pd
Float = Union[float, np.float16, np.float32, np.float64]
ResultRowSubjectWide = tuple[
    str,
    str,
    Optional[bool],
    str,
    str,
    str,
    Float,
    Float,
    Float,
    str,
    str
]
ResultRowModuleWide = tuple[
    str,
    str,
    Optional[bool],
    str,
    str,
    str,
    str,
    Float,
    Float,
    Float,
    str,
    Float,
    Float,
    Float,
    str,
    str
]

# Define range information for each test
test_ranges: "dict[str, str]" = {
    "Mutual Information Score": "Unbounded (non-negative)",
    "Normalized Mutual Information": "[0, 1]",
    "Adjusted Mutual Information": "[-1, 1]",
    "V-measure Cluster Labeling": "[0, 1]",
    "Homogeneity Score": "[0, 1]",
    "Adjusted Random Score": "[-1, 1]",
    "Fowlkes-Mallows Index": "[0, 1]",
    "Purity Score": "[0, 1]"
}
# Define list of test functions and their names
test_functions_with_range: "list[tuple[str, Callable[[pd.Series[str],pd.Series[str]], Float]]]" = [
    ("Mutual Information Score", mutual_info_score),
    ("Normalized Mutual Information", normalized_mutual_info_score),
    ("Adjusted Mutual Information", adjusted_mutual_info_score),
    ("V-measure Cluster Labeling", v_measure_score),
    ("Homogeneity Score", homogeneity_score),
    ("Adjusted Random Score", adjusted_rand_score),
    ("Fowlkes-Mallows Index", fowlkes_mallows_score)
]
