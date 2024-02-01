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

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input_file> [wav_file]"
    deactivate
    exit 1
fi

if [ "$#" -eq 2 ]; then
    python script.py "$1" --wav_file "$2"
else
    python script.py "$1"
fi

deactivate

