#!/bin/bash

# Initialize optional arguments with empty values
voice=""
filter_pattern=""

# Parse named arguments, except for input files
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --voice) voice="$2"; shift 2 ;;
        --filter_pattern) filter_pattern="$2"; shift 2 ;;
        *) break ;;  # Break the loop if no recognized named arguments are left
    esac
done

# Remaining arguments are considered input files
input_files=("$@")

# Check if at least one input file is provided
if [ ${#input_files[@]} -eq 0 ]; then
    echo "Usage: $0 [--voice <voice_sample.wav>] [--filter_pattern <filter_pattern>] <input_file1> <input_file2> [...]"
    exit 1
fi

# Process each input file
for input_file in "${input_files[@]}"; do
    # Construct the output file name by replacing the input file extension with .wav
    final_output="${input_file%.*}.wav"

    # Construct the command to call run.sh with the current input file
    CMD="./run.sh --input_file \"$input_file\" --final_output \"$final_output\""
    
    # Add optional arguments if they were provided
    if [ ! -z "$voice" ]; then
        echo "Applying custom voice"
        CMD+=" --voice \"$voice\""
    fi
    if [ ! -z "$filter_pattern" ]; then
        echo "Applying filter pattern"
        CMD+=" --filter_pattern \"$filter_pattern\""
    fi

    # Execute the constructed command
    echo "Processing $input_file..."
    echo "Running $CMD"
    eval $CMD
done

echo "Processing completed."
