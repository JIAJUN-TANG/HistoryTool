#!/bin/bash
SCRIPT_PATH=$(dirname "$0")
cd "$SCRIPT_PATH"
source activate myenv
if [ $? -ne 0 ]; then
    echo "Could not activate conda environment. Please check if 'myenv' is the correct environment name and you have conda initialized properly."
fi
streamlit run Homepage.py