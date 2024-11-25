from pathlib import Path
from typing import Union


def save_fig_as_pickle(destination_path: "Union[Path,str]", fig: object) -> None:
    from pickle import dump
    import modules.globals as g

    try:
        with open(destination_path, "wb") as f:
            dump(fig, f)
        g.logger.info(f"Successfully saved pickled figure: {destination_path}")
    except Exception as e:
        g.logger.error(f"Error saving pickled figure: {e}")
