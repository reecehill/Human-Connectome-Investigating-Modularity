# About
This repo is part of a dissertation project at the University of Nottingham, under the supervision of Prof. Marcus Kaiser.

# Dataset provided by HCP
The "Participants" folder is to be populated with MRI data provided by the Human Connectome Project (https://www.humanconnectome.org/study/hcp-young-adult). They will be downloaded automatically, using the subject IDs supplied in Participants/file_list_HCP_all_subset.txt.

# Changes
The original code scripts were provided and used by Taylor et al. (2017) [DOI: 10.1038/srep39859]. Changes have since been made. An overview of pertinent changes are listed below. For more detail, please review the repo changes on Github. Some details are also provided as comments in-code. 

1. **Filepaths/Filenames** At the time of writing the server that stores the HCP dataset (ConnectomeDB) is undergoing maintenance. Therefore, data is retrieved by AWS S3 (https://aws.amazon.com/s3/). Either because of this or due to changes over time, the folder hierarchy is different to that proposed by Taylor et al. This codebase has been modified to correct all filepaths, and some filenames have been changed for clarity.

2. **OS** Originally, the code was designed for Linux/iOS. Parts have been rewritten to run on a Windows machine with a Windows Subsystem for Linux (WSL, https://docs.microsoft.com/en-us/windows/wsl/install).

3. **Latest software** The code is now compatible with latest software versions. For example, many DSI Studio CLI arguments were deprecated (e.g., --csf_calibration=1).
	1. DSI Studio no longer allows random sampling of tracts (--random-seed, --seed-plan are deprecated). Whilst the original code took ten 1 million random tracts (? possible loss of uniqueness), this is no longer supported. Instead, we just take 10 million tracts in a single pass; the updated codebase demands more memory.  

# Overview of codebase
To supplement the "Instructions" section below, here we include a brief overview of the code, its pipeline, and the environment.

## Machine specification
The minimum machine requirements to run this code are not known. For a ballpark, we include the specification of the machine on which this code runs.

- OS: Windows 10 Education
- CPU: 6 cores (3.6GHz)
- RAM: 16Gb
- Storage: The amount is dependent on the number of subjects retrieved.
- GPU: Nvidia Geforce GTX 980 Ti
  - ? Unsure how useful this is at all. 