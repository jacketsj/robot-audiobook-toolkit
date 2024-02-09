#!/bin/bash

ENV_NAME="venv"

if [ ! -d "$ENV_NAME" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv $ENV_NAME
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

source $ENV_NAME/bin/activate

pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
pip install -Uqq WhisperSpeech
pip install -Uqq pydub

# Check if at least one argument (input file) is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input_file> [wav_file] [filter_pattern]"
    deactivate
    exit 1
fi

# Check the number of arguments and call the Python script accordingly
if [ "$#" -eq 3 ]; then
    python script.py "$1" --wav_file "$2" --filter_pattern "$3"
elif [ "$#" -eq 2 ]; then
    # Determine if the second argument is a wav file or filter pattern based on its extension or format
    if [[ "$2" =~ \.wav$ ]]; then
        python script.py "$1" --wav_file "$2"
    else
        python script.py "$1" --filter_pattern "$2"
    fi
else
    python script.py "$1"
fi

deactivate

