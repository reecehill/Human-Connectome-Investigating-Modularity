from includes.visualisation.graphs import plotRoiRegion
from modules.pipeline.stepper import prepStep


if __name__ == "__main__":
    from modules.visualisation.__main__ import run

    run()
else:
    raise Exception("This file is not meant to be imported.")
