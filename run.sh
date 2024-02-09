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

# Initialize variables for arguments
input_file=""
voice=""
filter_pattern=""
final_output=""

# Parse named arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --input_file) input_file="$2"; shift ;;
        --voice) voice="$2"; shift ;;
        --filter_pattern) filter_pattern="$2"; shift ;;
        --final_output) final_output="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$input_file" ]; then
    echo "Usage: $0 --input_file <input_file> [--voice <voice_sample.wav>] [--filter_pattern <filter_pattern>] [--final_output <final_output>]"
    deactivate
    exit 1
fi

# Construct the command to call the Python script
CMD="python script.py \"$input_file\""

# Add optional arguments if they were provided
if [ ! -z "$voice" ]; then
    CMD+=" --voice \"$voice\""
fi

if [ ! -z "$filter_pattern" ]; then
    CMD+=" --filter_pattern \"$filter_pattern\""
fi

if [ ! -z "$final_output" ]; then
    CMD+=" --final_output \"$final_output\""
fi

# Execute the constructed command
eval $CMD

deactivate

