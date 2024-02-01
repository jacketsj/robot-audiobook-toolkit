import os
import argparse
import torch
from whisperspeech.pipeline import Pipeline

if not torch.cuda.is_available():
    raise RuntimeError("CUDA is not available. Please ensure that you have a CUDA-compatible GPU and that CUDA is installed.")

pipe = Pipeline()

def process_input_file(input_file, wav_file=None):
    speaker_emb = None
    if wav_file:
        speaker_emb = pipe.extract_spk_emb(wav_file)

    os.makedirs("output", exist_ok=True)

    with open(input_file, 'r') as file:
        for i, line in enumerate(file):
            # Skip empty lines
            if line.strip():
                output_filename = f"output/output_{i+1}.wav"
                pipe.generate_to_file(output_filename, line.strip(), speaker=speaker_emb)

def main():
    parser = argparse.ArgumentParser(description='Process a text file for WhisperSpeech generation.')
    parser.add_argument('input_file', type=str, help='The input text file')
    parser.add_argument('--wav_file', type=str, help='Optional WAV file for speaker embedding', default=None)
    args = parser.parse_args()

    process_input_file(args.input_file, args.wav_file)

if __name__ == "__main__":
    main()

