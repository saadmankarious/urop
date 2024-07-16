# Lovelace

Centrla repository for Lovelace: a labeled-data collection tool from Reddit. 
Currently the tool supports generating labeled data for diagnosed and control classes
from mental health related subreddits. Nine subbreddits are currently available:
- [Bipolar]
- [Depression]
- [ADHD]
- [...]


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

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

## Features


