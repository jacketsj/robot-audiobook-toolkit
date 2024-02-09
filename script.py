import os
import re
import argparse
import torch
from pydub import AudioSegment
from whisperspeech.pipeline import Pipeline

if not torch.cuda.is_available():
    raise RuntimeError("CUDA is not available. Please ensure that you have a CUDA-compatible GPU and that CUDA is installed.")

pipe = Pipeline()

def split_into_sentences(text):
    sentences = re.split(r'(?<=\w\.)\s+(?=[A-Z])', text)
    return sentences

def concatenate_audio_files(files, output_path):
    combined = AudioSegment.empty()
    for file in files:
        audio = AudioSegment.from_wav(file)
        combined += audio
    combined.export(output_path, format="wav")

def process_input_file(input_file, voice=None, filter_pattern=None, final_output=None):
    speaker_emb = None
    if voice:
        speaker_emb = pipe.extract_spk_emb(voice)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    accumulated_text = ""
    with open(input_file, 'r') as file:
        for line in file:
            if filter_pattern is None or not re.search(filter_pattern, line):
                if not accumulated_text.endswith(' '):
                    accumulated_text += " "
                accumulated_text += line.strip()

    sentences = split_into_sentences(accumulated_text)
    generated_files = []

    for i, sentence in enumerate(sentences):
        if sentence:
            output_filename = f"{output_dir}/output_sentence_{i+1}.wav"
            pipe.generate_to_file(output_filename, sentence.strip(), speaker=speaker_emb)
            generated_files.append(output_filename)

    if generated_files:
        if not final_output:
            final_output = f"{output_dir}/output_combined.wav"
        concatenate_audio_files(generated_files, final_output)
        print(f"All sentences concatenated into: {final_output}")
    else:
        print("No sentences generated.")

def main():
    parser = argparse.ArgumentParser(description='Process a text file for WhisperSpeech generation, splitting by more accurate sentence end, and concatenate into a single WAV.')
    parser.add_argument('input_file', type=str, help='The input text file')
    parser.add_argument('--voice', type=str, help='Optional WAV file for speaker embedding', default=None)
    parser.add_argument('--filter_pattern', type=str, help='Regex pattern to filter lines from the text file', default=None)
    parser.add_argument('--final_output', type=str, help='Optional final output WAV file name', default=None)
    args = parser.parse_args()

    process_input_file(args.input_file, args.voice, args.filter_pattern, args.final_output)

if __name__ == "__main__":
    main()

