import datetime
import glob
from pathlib import Path
from typing import Any, Union
import matplotlib as mpl
from matplotlib.offsetbox import AnchoredText
import pandas as pd
import config
from includes.statistics.testVariables import Float
from includes.statistics.utils import populateModuleMetrics
from modules.file_directory.file_directory import createDirectories
import modules.globals as g
import numpy as np
import matplotlib.pyplot as plt
from includes.statistics import (
    test_ranges,
    test_functions_with_range,
)


def plotTimelines(subjectId: str, pathTo: dict[str, Path]) -> None:
    subjectDirectory = config.SUBJECT_DIR / "statistics"

    # Retrieve only "s-" and "f-" prefixed files
    files = [
        Path(f)
        for f in glob.glob(
            f"{subjectDirectory}/**/[sf]-*.pkl{'.gz' if config.COMPRESS_FILE else ''}",
            recursive=True,
        )
    ]

    # Convert file data into a DataFrame
    df = pd.DataFrame(
        [(f.parent, f.name[:2], f.name[2:], f) for f in files],
        columns=["folder", "prefix", "core_name", "file"],
    )

    # Pivot table to pair "s-" and "f-" files in the same folder
    paired_files = df.pivot(
        index=["folder", "core_name"], columns="prefix", values="file"
    ).dropna()

    # Process each matched pair using apply (vectorized processing)
    paired_files.apply(
        lambda row: plotTimeline(  # type: ignore
            pd.read_pickle(row["s-"]),
            pd.read_pickle(row["f-"]),
            title=row.name[1].replace(".pkl.gz", ""),
            filePath=pathTo["figures"]
            / "subjects"
            / Path(*row["s-"].parts[row["s-"].parts.index("subjects") + 1 :]).parent,
        ),
        axis=1,
    )
    plt.close()


def plotTimeline(
    x: "pd.Series[Any]", y: "pd.Series[Any]", filePath: Path, title=""
) -> None:
    if len(config.ALL_SUBJECTS) > 5:
        g.logger.info(
            "[Performance] Skipped creating timeline plot as large sample size."
        )
        return

    g.logger.info(f"Plotting a timeline for: {filePath.resolve()}")
    x = x.astype(str)
    y = y.astype(str)
    # Create a full index to ensure gaps are shown
    x_length = x.attrs["applied_handlers"][0]["metadata"]["pre_handler_length"]
    full_index = pd.Series(range(x_length))

    # Merge the actual data with the full index
    x_full = pd.Series(index=full_index)
    y_full = pd.Series(index=full_index)
    x_full.attrs, y_full.attrs = x.attrs, y.attrs

    x_full[x.index] = x.to_numpy()
    y_full[y.index] = y.to_numpy()

    x_full = x_full.fillna("-1")
    y_full = y_full.fillna("-1")

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

    plt.ioff()
    plt.switch_backend("Agg")  # Non-GUI backend (faster rendering)
    mpl.rcParams["path.simplify"] = True  # Enable path simplification
    mpl.rcParams["path.simplify_threshold"] = 0.1  # Adjust simplification level
    mpl.rcParams["svg.hashsalt"] = ""  # Remove unnecessary hashes
    mpl.rcParams["svg.fonttype"] = "none"  # Avoid embedding fonts

    plt.rcParams["svg.fonttype"] = "none"
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 15))
    fig.suptitle(title if title else "Figure")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add the timestamp as a footer using figtext
    plt.figtext(
        0.5,
        -0.05,
        f"Generated on: {timestamp}",
        ha="center",
        fontsize=10,
        style="italic",
    )

    for subplottitle, x1, y1, ax in [
        ("Full Sequence (Soft Mask)", x_full, y_full, ax1),
        ("Module only sequence (Hard Mask)", x, y, ax2),
    ]:
        results: "list[Any]" = []

        for test_name, test_func in test_functions_with_range:
            try:
                score_x_defined: "Union[Float,str]" = test_func(x1, y1)
                results.append(
                    (
                        test_name,
                        score_x_defined,
                        test_ranges[test_name],
                    )
                )
            except Exception as e:
                g.logger.error(f"Error running {test_name} with x as truth: {e}")
                raise Exception(f"Error running {test_name} with x as truth: {e}")

        # Create a DataFrame for easier manipulation
        df = pd.DataFrame({"x": x1, "y": y1, "Index": x1.index})

        # Map x and y values to their corresponding positions
        jitter_strength = 0.01  # Adjust this value if needed
        x_mapped = df["x"].map(category_to_position) + np.random.uniform(
            -jitter_strength, jitter_strength, df["x"].shape
        )
        y_mapped = df["y"].map(category_to_position) + np.random.uniform(
            -jitter_strength, jitter_strength, df["y"].shape
        )

        if "-1" in categories:
            ax.axhspan(
                category_to_position["-1"] - 0.5,
                category_to_position["-1"] + 0.5,
                facecolor="darkgray",
                alpha=0.8,
            )

        # Adding zebra shaded background for each category
        for i in range(len(categories)):
            if i % 2 == 0:
                ax.axhspan(i - 0.5, i + 0.5, facecolor="lightgray", alpha=0.3)

        # Plotting x in blue and y in green, aligned with their category values
        # Plotting x in blue and y in green, aligned with their category values
        ax.scatter(
            df["Index"],
            x_mapped + 0.1,  # Align x with its category
            color="blue",
            s=5,
            label="Structural modules",
            marker="^",
        )

        ax.scatter(
            df["Index"],
            y_mapped - 0.1,  # Align y with its category
            color="green",
            s=5,
            label="Functional modules",
            marker="^",
        )

        # Adding horizontal grid lines between categories
        for i in range(len(categories) + 1):
            ax.axhline(y=i - 0.5, color="gray", linestyle="-", linewidth=0.5)

        # Adjusting y-axis
        newline = "\n"
        y_fn_module_distances = x1.attrs.get(
            "metrics", populateModuleMetrics(x1, x1.attrs["centroid_coords"])
        )
        y_labels = {}
        for i, val in enumerate(categories):
            y_labels[val] = f"Module {val}{newline}"
            # Find dictionary where x_module_id is 'val'
            matching_roi = next(
                (item for item in y_fn_module_distances if item["x_module_id"] == val),
                None,
            )
            # Extract first roi value (i.e., the closest by distance) if found
            first_roi_value = (
                next(iter(matching_roi["rois"].values())) if matching_roi else None
            )

            if first_roi_value and matching_roi:
                y_labels[
                    val
                ] += f"{first_roi_value['name']} ({first_roi_value['distance']:.2f}mm)"
                y_labels[
                    val
                ] += f"{newline}{np.array2string(matching_roi['module_centroid'], precision=2, separator=', ')[1:-1]}"
                y_labels[
                    val
                ] += f"{newline}{first_roi_value['hemi']}"
                y_labels[
                    val
                ] += f"{newline}"
            else:
                y_labels[val] += "No closest ROI found"

        ax.set_yticks(np.arange(len(categories)))
        ax.set_yticklabels(list(y_labels.values()))
        ax.set_xlim(min(x1.index), max(x1.index))  # Full index range to show gaps
        ax.set_xticks(
            np.linspace(min(x1.index), max(x1.index), num=10)
        )  # Add evenly spaced ticks

        ax.set_title(subplottitle)
        newline = "\n"
        description = f'{"-".join(f"{key}_{value}" for key, value in x1.attrs["dataset_descriptors"].items())}\nApplied handlers: {", "+newline.join(applied_handler["name"] for applied_handler in x1.attrs["applied_handlers"])}'

        text_box = AnchoredText(
            description,
            loc="upper left",  # Adjust position (upper left, lower right, etc.)
            frameon=True,  # Box around text
            prop=dict(
                size=10,
            ),  # Font size
        )
        text_box.patch.set_alpha(
            0.9
        )  # Set background transparency (0 = fully transparent, 1 = solid)

        results_content = (
            "MASK RESULTS:\n"
            + f"Struc Faces: {len(x1)}"
            + "\n"
            + f"Func Faces: {len(y1)}"
            + "\n"
            + "\n".join(
                [f"{name}: {value} ({bounds})" for name, value, bounds in results]
            )
        )
        stats_box = AnchoredText(
            results_content, loc="lower right", prop=dict(size=10), frameon=True
        )
        stats_box.patch.set_alpha(
            0.8
        )  # Set background transparency (0 = fully transparent, 1 = solid)
        stats_box.set_zorder(level=20)  # Higher value brings it to the front

        ax.add_artist(text_box)
        ax.add_artist(stats_box)
        ax.legend(loc="upper right")
        fig.canvas.draw()

    createDirectories([filePath], createParents=True, throwErrorIfExists=False)
    filename = f"{title if title else '-'.join(applied_handler['name'] for applied_handler in x.attrs['applied_handlers'])}"
    svgPath = filePath / f"{filename}_timeline.svg"
    plt.tight_layout()
    # buffer = io.BytesIO()
    plt.savefig(
        svgPath,
        format="svg",
        dpi=72,
        bbox_inches="tight",
        backend="cairo",
    )
    # with gzip.open(f"{svgPath}.gz", "wb") as f_out:
    #     f_out.write(buffer.getvalue())
    plt.close()
