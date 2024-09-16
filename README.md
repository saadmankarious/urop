# Pipeline

This repo includes scripts for data generation and analysis for the research paper. You can use these scripts to regenerate same version of the dataset (user default values for paramters) or to generate your own custom version by manipulating parameters in /config/global.json. This pipeline expects subreddit posts and comments obtained via the arctic shift api (https://arctic-shift.photon-reddit.com/download-tool). Support for adittional apis will be provided in the future.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Utils](#utils)


## Installation
After cloning this project, you need to create a new py environment at the root folder of the cloned project with: 
```bash
python3 -m venv venv
source venv/bin/activate

#install needed packages:
pip3 install -r requirements.txt
```

## Usage
project-root-dir/reddit/scripts/arctic-pipeline is the main package for data cleaning and collection. Here is an example of how to generate a dataset for biopolar disorder: 

```bash
#generate new daignosed dataset
cd reddit/scripts/arctic-pipeline/diagnosed
bash generate_diagnosed.sh ~/Downloads/bipolar_june_2024.jsonl bipolar 50
```
<path_to_raw_data_from_arctic_api>  <condition_name> <minimum_posts_for_user>
Generates a diagnosed dataset for condition condition_name at location project-root-dir/reddit/data/condition_name_output/diagnosed

```bash
#generate new control dataset
cd reddit/scripts/arctic-pipeline/diagnosed
bash generate_control.sh ../../../data/bipolar_output 9
```
<condition_generated_folder> <threshold>
Generates a control dataset for the obtained diagnosed dataset at location project-root-dir/reddit/data/condition_name_output/control. Has to be ran after diagnosed generation is complete.


## Utils
project-root-dir/reddit/scripts/utils includes some useful utility scripts that help monitoring and facilitating data collection and analysis. Here is some examples:

```bash
#Monitoring control generation
cd reddit/scripts/utils
bash matched_counter.sh ../../../data/bipolar_output/control
```

This will provide a summary of how many contorl users were collected per batch of diagnosed users. Ideally this should be 90 for every file since files are configured with 10 diagnosed users, paired with 9 controls each. You can manipulate all those values at config/global.json!

