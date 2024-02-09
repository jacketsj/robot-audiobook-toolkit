#!/bin/bash

ENV_NAME="venv"

# Activate the virtual environment
source $ENV_NAME/bin/activate

# Install EbookLib and PyMuPDF if not already installed
pip install -Uqq ebooklib
pip install -Uqq pymupdf

# Check if at least two arguments (input and output files) are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <input.epub/input.pdf> <output.txt> [page-range]"
    deactivate
    exit 1
fi

# Check if the optional page range argument is provided
if [ "$#" -eq 3 ]; then
    PAGE_RANGE="$3"
    # Run the Python script with the input file, output text file, and page range as arguments
    python convert_to_text.py "$1" "$2" "$PAGE_RANGE"
else
    # Run the Python script with just the input file and output text file as arguments
    python convert_to_text.py "$1" "$2"
fi

# Deactivate the virtual environment
deactivate

