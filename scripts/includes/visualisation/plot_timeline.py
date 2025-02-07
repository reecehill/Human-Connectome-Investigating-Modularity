from collections import defaultdict
from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from matplotlib.offsetbox import AnchoredText
from modules.file_directory.file_directory import createDirectories

def plotTimelines(subjectId: str, pathTo: dict[str, Path]) -> None:
    import config
    import modules.globals as g
    subjectDirectory = config.SUBJECT_DIR / "statistics"

    csv_files = glob.glob(f"{subjectDirectory}/**/*.pkl.gz", recursive=True)
    # Dictionary to store paired files
    paired_files = defaultdict(dict)

    for file in map(Path, csv_files):  # Convert all to Path objects
        if file.name.startswith(("s_", "f_")):
            paired_files[file.name[2:]][file.name[:2]] = file  # Extract core name and prefix

    paired_files = dict(paired_files)  # Convert defaultdict to dict (if needed)

    # Keep only those pairs that contain both "s_" and "f_"
    paired_files = {core: pair for core, pair in paired_files.items() if "s_" in pair and "f_" in pair}

    for coreDataName, files in paired_files.items():
        fileName = coreDataName.replace(".pkl.gz", "").translate(
            str.maketrans("", "", "aeiouAEIOU")
        )
        x = pd.read_pickle(files["s_"])
        y = pd.read_pickle(files["f_"])
        subPath = Path(*files["s_"].parts[files["s_"].parts.index("subjects") + 1 :]).parent
        g.logger.info(f"Plotting a timeline for: {subPath.resolve()}/{fileName}")
        plotTimeline(
            x,
            y,
            title=fileName,
            filePath=pathTo["figures"] / "subjects" / subPath,
        )
        pass
    pass

def plotTimeline(x: "pd.Series[Any]", y: "pd.Series[Any]", filePath: Path, title = "") -> None:
    import config

    
    if(len(config.ALL_SUBJECTS) > 5):
        import modules.globals as g
        g.logger.info("[Performance] Skipped creating timeline plot as large sample size.")
        return

    x = x.astype(str)
    y = y.astype(str)
    # Create a full index to ensure gaps are shown
    x_length = x.attrs["applied_handlers"][0]["metadata"]["pre_handler_length"]
    full_index = pd.Series(range(x_length))

    # Merge the actual data with the full index
    x_full = pd.Series(index=full_index)
    y_full = pd.Series(index=full_index)

    x_full[x.index] = x.values
    y_full[y.index] = y.values

    # Combine unique categories from x and y
    categories = np.unique(np.concatenate((x.unique(), y.unique()))).tolist()

    if x.attrs["dataset_descriptors"]["data_type"] == "int":
        categories = sorted(
            categories, key=lambda v: (not v.isdigit(), int(v) if v.isdigit() else v)
        )
    elif x.attrs["dataset_descriptors"]["data_type"] == "words":
        categories = sorted(categories)
    else:
        raise ValueError("Invalid data_type")
    # Ensure categories are in numerical/alphabetical order
    # categories = categories[categories != -1]  # Remove -1 from categories

    # Create a mapping from category values to y-axis positions
    category_to_position = {category: idx for idx, category in enumerate(categories)}

    # Create a DataFrame for easier manipulation
    df = pd.DataFrame({"x": x_full, "y": y_full, "Index": full_index})

    # Map x and y values to their corresponding positions
    jitter_strength = 0.01  # Adjust this value if needed
    x_mapped = df["x"].map(category_to_position) + np.random.uniform(
        -jitter_strength, jitter_strength, df["x"].shape
    )
    y_mapped = df["y"].map(category_to_position) + np.random.uniform(
        -jitter_strength, jitter_strength, df["y"].shape
    )

    # 3. Timeline-like 1D Scatter Plot with x and y
    plt.ioff()
    plt.switch_backend("Agg")  # Non-GUI backend (faster rendering)
    fig, ax = plt.subplots(figsize=(30, 15))

    if "-1" in categories:
        plt.axhspan(
            category_to_position["-1"] - 0.5,
            category_to_position["-1"] + 0.5,
            facecolor="darkgray",
            alpha=0.8,
        )

    # Adding zebra shaded background for each category
    for i in range(len(categories)):
        if i % 2 == 0:
            plt.axhspan(i - 0.5, i + 0.5, facecolor="lightgray", alpha=0.3)

    # Plotting x in blue and y in green, aligned with their category values
    # Plotting x in blue and y in green, aligned with their category values
    plt.scatter(
        df["Index"],
        x_mapped + 0.1,  # Align x with its category
        color="blue",
        s=5,
        label="Structural modules",
    )

    plt.scatter(
        df["Index"],
        y_mapped - 0.1,  # Align y with its category
        color="green",
        s=5,
        label="Functional modules",
    )

    # Adding horizontal grid lines between categories
    for i in range(len(categories) + 1):
        plt.axhline(y=i - 0.5, color="gray", linestyle="-", linewidth=0.5)

    # Adjusting y-axis
    plt.yticks(np.arange(len(categories)), categories)
    plt.xlim(0, x_length)  # Full index range to show gaps
    plt.xticks(np.linspace(0, x_length, num=10))  # Add evenly spaced ticks

    plt.title("Sequential Distribution of x and y Labels")
    description = f"{'-'.join(f'{key}_{value}' for key, value in x.attrs['dataset_descriptors'].items())}\nApplied handlers: {', '.join(applied_handler['name'] for applied_handler in x.attrs['applied_handlers'])}"

    plt.suptitle(title if title else "Figure")

    text_box = AnchoredText(
        description,
        loc="upper left",  # Adjust position (upper left, lower right, etc.)
        frameon=True,  # Box around text
        prop=dict(size=10),  # Font size
    )

    ax.add_artist(text_box)

    createDirectories([filePath], createParents=True, throwErrorIfExists=False)
    filename = f"{title if title else '-'.join(applied_handler['name'] for applied_handler in x.attrs['applied_handlers'])}"
    plt.legend(loc="upper right")
    plt.tight_layout()

    svgPath = filePath / f"{filename}_timeline.svg"
    plt.savefig(svgPath, format="svg", dpi=100, bbox_inches="tight")
    plt.close()
