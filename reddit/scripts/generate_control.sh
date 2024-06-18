#!/bin/bash

# A) No posts made in MH subreddits
# B) No mention of any MH realated term
# runs execlusion against A) and B) conditions and saves output in condition/final
# Example run: 
#     bash run_diagnosed_execlusion.sh adhd_output 20
#     runs execlusion with 20 minimum posts per user

# Check if the user provided the required arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <INPUT_FOLDER> <threshold>"
    exit 1
fi

# Input file path provided by the user
INPUT_FOLDER=$1
# Output file path provided by the user
FINAL_OUTPUT="${INPUT_FOLDER}/control/data-control.final.json"

# Threshold provided by the user
THRESHOLD="${2:-9}"

# Hardcoded paths to the Python scripts
FIND_CANDIDATES="control/get_control_candidates.py"
MATCH_CONTROLS="control/match_controls.py"

# Intermediate file
TEMP_OUTPUT="${INPUT_FOLDER}/control/candidate-controls.temp.json"

# Execute the first Python script
echo ""
echo "Finding control candidates..."
python3 "$FIND_CANDIDATES" "${INPUT_FOLDER}/diagnosed/non_mh_subreddits_summary.json" "$TEMP_OUTPUT" 
echo "Done finding candidate controls..."
echo ""

# Check if the first script executed successfully
if [ $? -eq 0 ]; then
    # Execute the second Python script
    echo "Matching found controls..."
    python3 "$MATCH_CONTROLS" "$TEMP_OUTPUT" "$FINAL_OUTPUT" --min_controls "$THRESHOLD"
    # rm $TEMP_OUTPUT
    echo "Done matching controls with ${THRESHOLD} per diagnosed user"
    echo ""
else
    echo "Error: The first Python script did not execute successfully."
    exit 1
fi
