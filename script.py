import os
import argparse
import torch
from whisperspeech.pipeline import Pipeline

if not torch.cuda.is_available():
    raise RuntimeError("CUDA is not available. Please ensure that you have a CUDA-compatible GPU and that CUDA is installed.")

pipe = Pipeline()

def process_input_file(input_file):
    os.makedirs("output", exist_ok=True)

    with open(input_file, 'r') as file:
        for i, line in enumerate(file):
            # Skip empty lines
            if line.strip():
                # Generate separate output for each line
                output_filename = f"output/output_{i+1}.wav"
                pipe.generate_to_file(output_filename, line.strip())

def main():
    parser = argparse.ArgumentParser(description='Process a text file for WhisperSpeech generation.')
    parser.add_argument('input_file', type=str, help='The input text file')
    args = parser.parse_args()

    process_input_file(args.input_file)

if __name__ == "__main__":
    main()
