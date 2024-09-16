# Pipeline

This repo includes scripts for data generation and analysis for the research paper. You can use these scripts to regenerate same version of the dataset (user default values for paramters) or to generate your own custom version of the dataset by manipulating parameters in /config/global.json. This pipeline expects subreddit posts and comments obtained via the arctic shift api (https://arctic-shift.photon-reddit.com/download-tool). Support for adittional apis will be provided in the future.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)


## Installation
After cloning this project, you need to create a new py environment at the root folder of the cloned project with: 
```bash
python3 -m venv venv
source venv/bin/activate

#install needed packages:
pip3 install -r requirements.txt
```

## Usage
Now you're all set to start experimenting with labeled data creation.
Ex:

```bash
#generate new daignosed dataset
cd reddit/scripts/arctic-pipeline/diagnosed
bash generate_diagnosed.sh /pat/to/raw-data
```



