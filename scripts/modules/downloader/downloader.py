import config
from .ProgressPercentage import ProgressPercentageClass
import modules.globals as g
import datalad.api as dl

def getData():
  g.logger.info("Building dataset")
  def resultFilter(ok):
    print("ok")
    print("ok")
    pass
  def resultXfm(ok):
    print("ok")
    print("ok")
    pass
  dataset = dl.install(source="https://github.com/OpenNeuroDatasets/ds002685.git", path=config.DATA_DIR,result_filter=resultFilter, result_xfm=resultXfm)