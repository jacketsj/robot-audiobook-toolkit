#!/bin/bash

ENV_NAME="venv"

# Check if the virtual environment exists, create it if it doesn't
if [ ! -d "$ENV_NAME" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv $ENV_NAME
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source $ENV_NAME/bin/activate

pip install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
pip install -Uqq WhisperSpeech

# Check if an input file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    deactivate
    exit 1
fi

# Run the Python script with the input file as an argument
python script.py "$1"

# Deactivate the virtual environment
deactivate

