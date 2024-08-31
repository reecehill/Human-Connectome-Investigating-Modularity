from typing import Dict
import modules.globals as g
from modules.hcp_data_manager.downloader import getFile
import config
from pathlib import Path
from modules.subprocess_caller.call import *
from ..file_directory.file_directory import createDirectories
import csv
def createTimingFiles(subjectId: str) -> bool:
  # Function not used when using fMRI pre-processed data in HCP dataset.
  g.logger.info("Ensuring timing files for functional data exists -- Run 1 (Right-Left Phase Encoding)")
  _ = [getFile(localPath=Path(config.DATA_DIR / 'subjects' / subjectId / 'unprocessed' / ('7T' if config.USE_7T_DIFFUSION else '3T') / 'tfMRI_MOTOR_RL' / 'LINKED_DATA' / 'EPRIME' / 'EVs' / f"{fmriTask}.txt")) for fmriTask in config.ALL_FMRI_TASKS]

  g.logger.info("Ensuring timing files for functional data exists -- Run 2 (Left-Right Phase Encoding)")
  _ = [getFile(localPath=Path(config.DATA_DIR / 'subjects' / subjectId / 'unprocessed' / ('7T' if config.USE_7T_DIFFUSION else '3T') / 'tfMRI_MOTOR_LR' / 'LINKED_DATA' / 'EPRIME' / 'EVs' / f"{fmriTask}.txt")) for fmriTask in config.ALL_FMRI_TASKS]
  return True

def getFmriData(subjectId: str) -> bool:
  # Function not used when using fMRI pre-processed data in HCP dataset.
  g.logger.info("Ensuring functional data results exist")
  subjectDir = config.SUBJECTS_DIR / subjectId / "MNINonLinear"
  filesToExist = [
                    (subjectDir / 'Results' / 'tfMRI_MOTOR' /'tfMRI_MOTOR_hp200_s2_level2.feat' /f'{subjectId}_tfMRI_MOTOR_level2_hp200_s2.dscalar.nii'),
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]

  g.logger.info("Ensuring surface files exist")
  filesToExist = [
                    (subjectDir / 'fsaverage_LR32k' / f'{subjectId}.L.pial.32k_fs_LR.surf.gii'),
                    (subjectDir / 'fsaverage_LR32k' / f'{subjectId}.R.pial.32k_fs_LR.surf.gii'),
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]
  return True

def runSpm(subjectId: str) -> bool:
  # Function not used when using fMRI pre-processed data in HCP dataset.
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "RunPreproc_1stLevel_job {config.matLabDriveAndPathToSubjects} {subjectId}"',
                      ],
              cwd=config.matlabScriptsFolder)

def matlabSortFmriVoxelsIntoModules(subjectId: str, binaryThreshold: float) -> bool:
  # Function not used when using fMRI pre-processed data in HCP dataset.
  # TODO: NOT USED.
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "convertIntensityToCoordinates {config.matLabDriveAndPathToSubjects} {subjectId} {binaryThreshold}"',
                      ],
              cwd=config.matlabScriptsFolder)  

def matlabMapLowToHighResFmriData(subjectId: str) -> bool:
  # Map low-resolution fMRI data to high-resolution (e.g., 32k to 164k node mesh)
  # TODO: It makes sense that this is done only with labelled data (e.g., modules).
  
  subjectFolder = config.SUBJECTS_DIR / subjectId

  fMriScalarPath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId))
  fMriModulesPath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId).replace(".dscalar.nii",".clusters.dscalar.nii"))

  fMriScalarPath_outputFolder = subjectFolder / config.IMAGES["FMRI"]["COMMON_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["COMMON_RES"]["DATA"]["SCALAR_FOLDER"].replace("$subjectId$",subjectId))
  fMriModulesPath_outputFolder = subjectFolder / config.IMAGES["FMRI"]["COMMON_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["COMMON_RES"]["DATA"]["MODULES_FOLDER"].replace("$subjectId$",subjectId))

  
  subjectLeftSurfacePath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectRightSurfacePath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)                                                                                  

  subjectLeftSurfacePath_output = subjectFolder / config.IMAGES["FMRI"]["COMMON_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["COMMON_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectRightSurfacePath_output = subjectFolder / config.IMAGES["FMRI"]["COMMON_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["COMMON_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)                                                                                  
                                                                         
  
  remoteFilesToExist: "list[Path]" = [
                    fMriScalarPath_input,
                    subjectLeftSurfacePath_input,
                    subjectRightSurfacePath_input
                    ]
  localFilesToExist: "list[Path]" = [
                    fMriModulesPath_input
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]
  _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in localFilesToExist]
  createDirectories(directoryPaths=[
    subjectFolder / config.IMAGES["FMRI"]["HIGH_RES"]["DATA"]["FOLDER"],
    subjectFolder / config.IMAGES["FMRI"]["COMMON_RES"]["DATA"]["FOLDER"],
    subjectFolder / config.IMAGES["FMRI"]["COMMON_RES"]["DATA"]["FOLDER"] / config.IMAGES["FMRI"]["COMMON_RES"]["DATA"]["SCALAR_FOLDER"],
    subjectFolder / config.IMAGES["FMRI"]["COMMON_RES"]["DATA"]["FOLDER"] / config.IMAGES["FMRI"]["COMMON_RES"]["DATA"]["MODULES_FOLDER"],
    ], createParents=True, throwErrorIfExists=False)

  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "mapFmriToHighResSurf {config.matLabDriveAndPathToSubjects} {subjectId} {config.DOWNSAMPLE_SURFACE} {config.PIAL_SURFACE_TYPE}  \'{subjectLeftSurfacePath_input}\' \'{subjectRightSurfacePath_input}\' \'{subjectLeftSurfacePath_output}\' \'{subjectRightSurfacePath_output}\' \'{fMriScalarPath_input}\' \'{fMriModulesPath_input}\' \'{fMriScalarPath_outputFolder}\' \'{fMriModulesPath_outputFolder}\'"',
                      ],
              cwd=config.matlabScriptsFolder)   

def getClusterThresholdForMap(subjectId: str, mapName: str, hemisphere: str) -> float:
  subjectFolder = config.SUBJECTS_DIR / subjectId
  percentilesCsvFile: Path = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / f"{hemisphere}.fMRI_percentiles_modified.csv"

  filesToExist = [
                    percentilesCsvFile
                    ]
  _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in filesToExist]

  
  with open(percentilesCsvFile.resolve().__str__()) as csvfile:
      csvreader = csv.reader(csvfile, dialect='excel-tab', skipinitialspace=True, strict=True)
      for row in csvreader:
        # If the map name is found in desired maps list...
        if(row[0].lower().__contains__(mapName.lower())):
          # Return its corresponding threshold.
          return float(row[-1])
  # If no map name is found in desired maps list...
  g.logger.info("Error: unable to find map's threshold by name: "+mapName)
  return float('nan')

def createRoiScalarFiles(subjectId: str) -> bool:
  subjectFolder = config.SUBJECTS_DIR / subjectId
  labelledCiftiFile = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["CIFTI_PATH"].replace("$subjectId$",subjectId))
  maskOfLLabel = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["L_MASK"]
  maskOfRLabel = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["R_MASK"]
  maskOfLRLabel = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["LR_MASK"]

  filesToExist = [
                    labelledCiftiFile
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]

  return all([
      call(cmdLabel="wb_command",
              cmd=[
                      config.WB_COMMAND,
                      '-cifti-label-to-roi',
                      labelledCiftiFile.resolve(),
                      maskOfLLabel.resolve(),
                      '-name',
                      'L_precentral',
                      '-map',
                      '100307_aparc'
                      ]),
      call(cmdLabel="wb_command",
              cmd=[
                      config.WB_COMMAND,
                      '-cifti-label-to-roi',
                      labelledCiftiFile.resolve(),
                      maskOfRLabel.resolve(),
                      '-name',
                      'R_precentral',
                      '-map',
                      '100307_aparc'
                      ]),
      call(cmdLabel="wb_command",
              cmd=[
                      config.WB_COMMAND,
                      '-cifti-merge',
                      maskOfLRLabel.resolve(),
                      # '-direction',
                      # 'ROW',
                      '-cifti',
                      maskOfLLabel.resolve(),
                      '-cifti',
                      maskOfRLabel.resolve(),                      
                      ]) 
  ])

def createRoiShapeFiles(subjectId: str) -> bool:
  subjectFolder = config.SUBJECTS_DIR / subjectId
  labelledLFile = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["L_PATH"].replace("$subjectId$",subjectId))
  labelledRFile = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["R_PATH"].replace("$subjectId$",subjectId))
  shapeLFile = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["L_SHAPE"].replace("$subjectId$",subjectId))
  shapeRFile = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["R_SHAPE"].replace("$subjectId$",subjectId))

  filesToExist = [
                    labelledLFile,
                    labelledRFile
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]
  
  return all([
    call(cmdLabel="wb_command",
              cmd=[
                      config.WB_COMMAND,
                      '-gifti-label-to-roi',
                      labelledLFile.resolve(),
                      shapeLFile.resolve(),
                      '-name',
                      'L_precentral',
                      ]),
    call(cmdLabel="wb_command",
              cmd=[
                      config.WB_COMMAND,
                      '-gifti-label-to-roi',
                      labelledRFile.resolve(),
                      shapeRFile.resolve(),
                      '-name',
                      'R_precentral',
                      ])
  ])

def createFmriDenseScalarOfRoiOnly(subjectId: str) -> bool:
  subjectFolder = config.SUBJECTS_DIR / subjectId
  fMriScalarPath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId))
  fMriScalarPath_input_cortical =  (subjectFolder / config.FMRI_SCALAR_PATH_CORTICAL).resolve().__str__().replace("$subjectId$",subjectId)

  maskOfLLabel = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["L_MASK"]
  maskOfRLabel = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["R_MASK"]

  desiredMapsCiftiFiles = {
    desiredMap
    .replace("$subjectId$", subjectId):
      fMriScalarPath_input.resolve().__str__()
      .replace(".dscalar", f"_{desiredMap}.dscalar")
      .replace("$subjectId$", subjectId)
      for desiredMap in config.DESIRED_FMRI_MAPS}
  
  localFilesToExist = [
                    maskOfLLabel,
                    maskOfRLabel
                    ]
  _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in localFilesToExist]
  remoteFilesToExist = [
                    fMriScalarPath_input
  ]
  _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]


  return all([
    all([
      # Split fMRI .dscalar file of all maps into .{map}.dscalar files that contain only one map.
      call(cmdLabel="wb_command",
                cmd=[
                        config.WB_COMMAND,
                        '-cifti-merge',
                        desiredCiftiMapPath,
                        '-cifti',
                        fMriScalarPath_input,
                        '-column',
                        desiredMap
                ]              
    ) for (desiredMap, desiredCiftiMapPath) in desiredMapsCiftiFiles.items()
        ]),
    # Discard subcortical data from fMRI (all) maps (used to generate csv of thresholds)
    call(cmdLabel="wb_command",
                cmd=[
                        config.WB_COMMAND,
                        '-cifti-create-dense-from-template',
                        maskOfLLabel.resolve(),
                        fMriScalarPath_input_cortical,
                        '-cifti',
                        fMriScalarPath_input                   
                        ]),
    
    # Discard subcortical data from fMRI ROIs
    all([
      call(cmdLabel="wb_command",
                cmd=[
                        config.WB_COMMAND,
                        '-cifti-create-dense-from-template',
                        maskOfLLabel.resolve(),
                        desiredCiftiMapPath.replace('.dscalar','_ROI.dscalar'),
                        '-cifti',
                        desiredCiftiMapPath                   
                        ]) for (_, desiredCiftiMapPath) in desiredMapsCiftiFiles.items()
      ]
        )])
  


def findClustersFromFmri(subjectId: str) -> bool:
  # This function levies wb_command -cifti-to-roi to create ROI.
  # https://humanconnectome.org/software/workbench-command/-cifti-label-to-roi

  g.logger.info("Finding clusters within functional data (scalar)")
  subjectFolder = config.SUBJECTS_DIR / subjectId
  
  shapeLFile = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["L_SHAPE"].replace("$subjectId$",subjectId))
  shapeRFile = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["R_SHAPE"].replace("$subjectId$",subjectId))

  maskOfLLabel = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["L_MASK"]
  maskOfRLabel = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["R_MASK"]
  g.logger.info("Ensuring files files exist")

  fMriScalarPath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId))

  subjectLSurfacePath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectRSurfacePath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  
  g.logger.info("Ensuring files files exist")
  createDirectories(directoryPaths=[subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"]], createParents=True)
  remoteFilesToExist = [
                    fMriScalarPath_input,
                    subjectLSurfacePath_input,
                    subjectRSurfacePath_input
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]
  localFilesToExist = [
    shapeLFile,
    shapeRFile,
    maskOfLLabel,
    maskOfRLabel,
  ]
  _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in localFilesToExist]


  cmds: list[bool] = []  
  for hemisphere, roi in {"L": maskOfLLabel, "R": maskOfRLabel}.items():
    for mapName in config.DESIRED_FMRI_MAPS:
      mapName = mapName.replace("$subjectId$", subjectId)
      ciftiRoiFile = fMriScalarPath_input.resolve().__str__().replace(".dscalar", f"_{mapName}_ROI.dscalar").replace("$subjectId$", subjectId)
      
      threshold = getClusterThresholdForMap(subjectId, mapName, hemisphere)
      cmds.append(
        call(cmdLabel="wb_command",
            cmd=[
                # This function levies wb_command -cifti-find-clusters to detect fMRI clusters.
                # https://humanconnectome.org/software/workbench-command/-cifti-find-clusters
                config.WB_COMMAND,
                '-cifti-find-clusters',
                ciftiRoiFile,

                # <surface-value-threshold> - threshold for surface data values
                # '0.00001',
                str(threshold),
                
                # <surface-minimum-area> - threshold for surface cluster area, in mm^2
                str(config.CLUSTER_MIN_AREA),

                # <volume-value-threshold> - threshold for volume data values
                'inf',

                # <volume-minimum-size> - threshold for volume cluster size, in mm^3
                'inf',

                # <direction> - which dimension to use for spatial information, ROW or COLUMN
                'COLUMN',

                # <cifti-out>
                ciftiRoiFile.replace(".dscalar", f"_{hemisphere}_clusters.dscalar" ),

                # - find values less than <value-threshold>, rather than greater
                # [-less-than],

                
                '-left-surface', #- specify the left surface to use
                subjectLSurfacePath_input.resolve(), #- the left surface file
                # '-corrected-areas', #vertex areas to use instead of computing them from the surface
                # shapeLFile.resolve(),
                #<area-metric> - the corrected vertex areas, as a metric

                '-cifti-roi',
                roi,

                '-right-surface', #- specify the right surface to use
                subjectRSurfacePath_input.resolve(), #- the right surface file

                # '-corrected-areas', #- vertex areas to use instead of computing them from the surface
                #<area-metric> - the corrected vertex areas, as a metric
                # shapeRFile.resolve(),

                #ignore clusters smaller than a given fraction of the largest cluster in the structure
                '-size-ratio', 
                '0.1', #- fraction of the structure's largest cluster area
                '0', #- fraction of the structure's largest cluster volume

                # '-distance', #- ignore clusters further than a given distance from the largest cluster in the structure
                # '20',
                # '-inf',
              ])) 
  return all(cmds)


def filterFmriMapsAndWriteToCsv(subjectId: str) -> bool:
  """ 
  This function reads the fMRI dscalar, and writes an .csv of only desired maps and the value at X percentile (CLUSTER_THRESHOLD).
  Effectively, it also filters the 26 maps (or FSL contrasts) from:
    1. motor
    2. motor minus average
    3. negative motor
    4. average minus motor

  To those specified by DESIRED_FMRI_MAPS variable, such as:
    1. motor minus average

  To yield a csv of two columns for each hemisphere (L+R): map_name, fmri_value_at_percentile.
  """
  g.logger.info("Creating csv that contains only the maps we want: "+''.join([desiredMap.replace("$subjectId$", subjectId) for desiredMap in config.DESIRED_FMRI_MAPS]))

  subjectFolder = config.SUBJECTS_DIR / subjectId
  fMriScalarPath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId))
  fMriScalarPath_input_cortical =  (subjectFolder / config.FMRI_SCALAR_PATH_CORTICAL).resolve().__str__().replace("$subjectId$",subjectId)
  percentilesCsvFolder = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"]
  maskOfLLabel = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["L_MASK"]
  maskOfRLabel = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["R_MASK"]


  g.logger.info("Ensuring files files exist")
  filesToExist = [
                    fMriScalarPath_input
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]

  for hemisphere, roi in {"L": maskOfLLabel, "R": maskOfRLabel}.items():
    percentilesCsvFile: Path = percentilesCsvFolder / f"{hemisphere}.fMRI_percentiles_raw.csv"
    g.logger.info("Getting "+str(config.CLUSTER_THRESHOLD)+"th percentile from each fMRI map and saving to csv file ("+percentilesCsvFile.resolve().__str__()+")")

    # Get percentile of fMRI data.   
    call(cmdLabel="wb_command",
         cmd = [
                config.WB_COMMAND,
                "-cifti-stats",
                fMriScalarPath_input_cortical,
                "-percentile",
                str(config.CLUSTER_THRESHOLD),
                "-roi",
                roi,
                "-show-map-name"
                ],
                saveToFile=percentilesCsvFile.resolve().__str__())

    # Read the raw map .csv and write a modified version that only contains the maps we want.
    filesToExist = [
                    percentilesCsvFile
                    ]
    _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in filesToExist]
    percentileValuesPerMap: Dict[str, float] = {}

    #Read raw csv
    with open(percentilesCsvFile.resolve().__str__()) as csvfile:
      csvreader = csv.reader(csvfile, dialect="excel-tab", skipinitialspace=True, strict=True)
      desiredMapNames = [desiredFmriMap.replace("$subjectId$", subjectId) for desiredFmriMap in config.DESIRED_FMRI_MAPS]
      for row in csvreader:
        row[1] = str(row[1]).strip().strip(":") 
        # If the map name is found in desired maps list...
        if(desiredMapNames.__contains__(row[1])):
          # Store map name and its corresponding threshold.
          percentileValuesPerMap[row[1]] = float(row[-1])

    #Write modified file
    with open(percentilesCsvFile.resolve().__str__().replace("_raw", "_modified"), 'w', newline='') as csvfile:
      writer = csv.writer(csvfile, dialect='excel-tab')
      list_from_dict = [*percentileValuesPerMap.items()]
      writer.writerows(list_from_dict)

    filesToExist = [
                      Path(percentilesCsvFile.resolve().__str__().replace("_raw", "_modified"))
                      ]
    _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in filesToExist]
  return all(item for item in _) # Modified .csv files have been created.

def findFmriExtrema(subjectId: str) -> bool:
  subjectFolder = config.SUBJECTS_DIR / subjectId
  labelledLFile = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["L_PATH"].replace("$subjectId$",subjectId))
  labelledRFile = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["R_PATH"].replace("$subjectId$",subjectId))
  g.logger.info("Ensuring files files exist")
  filesToExist = [
                    labelledLFile,
                    labelledRFile,
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]
  createDirectories(directoryPaths=[subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["LABEL"]["FOLDER"]], createParents=True)
  fMriScalarPath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId))
  fMriModulesPath_output = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId).replace(".dscalar.nii",".extrema_clusters.dscalar.nii"))

  subjectLSurfacePath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectRSurfacePath_input = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  
  g.logger.info("Ensuring files files exist")
  filesToExist = [
                    fMriScalarPath_input,
                    subjectLSurfacePath_input,
                    subjectRSurfacePath_input
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]
  
  return call(cmdLabel="wb_command",
              cmd=[
                config.WB_COMMAND,
                 '-cifti-extrema',
                # <cifti> - the input cifti
                fMriScalarPath_input.resolve(),

                #<surface-distance> - the minimum distance between extrema of the same type, for surface components
                '10',
                
                #<volume-distance> - the minimum distance between extrema of the same type, for volume components
                '1',
                
                #<direction> - which dimension to find extrema along, ROW or COLUMN
                'COLUMN',
                
                #<cifti-out> - output - the output cifti
                fMriModulesPath_output.resolve(),
                
                '-left-surface', #- specify the left surface to use
                subjectLSurfacePath_input.resolve(), #- the left surface file

                '-right-surface', # - specify the right surface to use
                subjectRSurfacePath_input.resolve(), #- the left surface file

                #[-cerebellum-surface] - specify the cerebellum surface to use
                  #<surface> - the cerebellum surface file

                #[-surface-presmooth] - smooth on the surface before finding extrema
                  #<surface-kernel> - the size of the gaussian surface smoothing kernel in mm, as sigma by default

                #[-volume-presmooth] - smooth volume components before finding extrema
                  #<volume-kernel> - the size of the gaussian volume smoothing kernel in mm, as sigma by default

                #[-presmooth-fwhm] - smoothing kernel distances are FWHM, not sigma

                #[-threshold] - ignore small extrema
                  #<low> - the largest value to consider for being a minimum
                  #<high> - the smallest value to consider for being a maximum

                #[-merged-volume] - treat volume components as if they were a single component

                #[-sum-maps] - output the sum of the extrema maps instead of each map separately

                #[-consolidate-mode] - use consolidation of local minima instead of a large neighborhood

                '-only-maxima', #- only find the maxima

                #[-only-minima] - only find the minima
              ])
  return True

def transformFmriIntoDiffusionSpace(subjectId: str) -> bool:
  # Function uses non-linear spatial transforms to move fMRI data from fMRI to a common space.
  # For HCP data, this moves fMRI from MNI space to T1w space.

  g.logger.info("Transforming fMRI surface to a different space.")
  subjectFolder = config.SUBJECTS_DIR / subjectId

  subjectLSurfacePath_input = subjectFolder / config.IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectRSurfacePath_input = subjectFolder / config.IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  
  outputSurfFolder = subjectFolder / config.IMAGES["FMRI"]["COMMON_RES"]["SURFACE"]["FOLDER"]
  subjectLSurfacePath_output = outputSurfFolder / config.IMAGES["FMRI"]["COMMON_RES"]["SURFACE"]["L_HEMISPHERE_PATH"]
  subjectRSurfacePath_output = outputSurfFolder / config.IMAGES["FMRI"]["COMMON_RES"]["SURFACE"]["R_HEMISPHERE_PATH"]
  acpcdc2StandardTransform = subjectFolder / config.TRANSFORMS["INTRA_SUBJECT"]["FOLDER"] / config.TRANSFORMS["INTRA_SUBJECT"]["ACPC_DC2STANDARD"]
  standard2AcpcdcTransform = subjectFolder / config.TRANSFORMS["INTRA_SUBJECT"]["FOLDER"] / config.TRANSFORMS["INTRA_SUBJECT"]["STANDARD2ACPC_DC"]
  g.logger.info("Ensuring files files exist")
  filesToExist = [
                    subjectLSurfacePath_input,
                    subjectRSurfacePath_input,
                    acpcdc2StandardTransform,
                    standard2AcpcdcTransform,
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]
  createDirectories([outputSurfFolder], createParents=True, throwErrorIfExists=False)
  warpLeftHemisphereSuccess = call(cmdLabel="wb_command",
              cmd=[
                      config.WB_COMMAND,
                      '-surface-apply-warpfield',
                      subjectLSurfacePath_input.resolve(),
                      acpcdc2StandardTransform.resolve(),
                      subjectLSurfacePath_output.resolve(),
                      '-fnirt',
                      standard2AcpcdcTransform.resolve(),
                      ],
              )
  warpRightHemisphereSuccess = call(cmdLabel="wb_command",
              cmd=[
                      config.WB_COMMAND,
                      '-surface-apply-warpfield',
                      subjectRSurfacePath_input.resolve(),
                      acpcdc2StandardTransform.resolve(),
                      subjectRSurfacePath_output.resolve(),
                      '-fnirt',
                      standard2AcpcdcTransform.resolve(),
                      ],
              )
  return warpLeftHemisphereSuccess and warpRightHemisphereSuccess


def matlabProcessFunctional(subjectId: str) -> bool:
  # This function takes fMRI data and returns a binarised surface.
  # TODO: Folder naming scheme is remnant of SPM.
  
  return (
          createRoiShapeFiles(subjectId=subjectId) and \
          createRoiScalarFiles(subjectId=subjectId) and \
          createFmriDenseScalarOfRoiOnly(subjectId=subjectId) and \
          filterFmriMapsAndWriteToCsv(subjectId=subjectId) and \
          findFmriExtrema(subjectId=subjectId) and \
          findClustersFromFmri(subjectId=subjectId)
          # matlabMapLowToHighResFmriData(subjectId=subjectId) and
          # transformFmriIntoDiffusionSpace(subjectId=subjectId)
  )
  return (matlabMapLowToHighResFmriData(subjectId=subjectId))
  firstLevelFolder =  config.SUBJECTS_DIR / subjectId / "1stlevel"
  createDirectories(directoryPaths=[firstLevelFolder], createParents=True, throwErrorIfExists=False)
    
  return (
    convertFmriToModules(subjectId=subjectId) and
    createTimingFiles(subjectId=subjectId) and
    getFmriData(subjectId=subjectId) and
    matlabSortFmriVoxelsIntoModules(subjectId=subjectId, binaryThreshold=config.FMRI_THRESHOLD_TO_BINARISE)
    )
  # runSpm() is not needed if we intend to use the processed data.
  # runSpm(subjectId=subjectId)
  


