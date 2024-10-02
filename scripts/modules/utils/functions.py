import config
def prepStep(subjectId: str):
  # Called at every new step in pipeline. 
  subjectDir = config.SUBJECTS_DIR / subjectId
  config.setSubjectDir(subjectDir)