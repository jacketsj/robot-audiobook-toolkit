from pydub import AudioSegment
import sys

def concatenate_wav_files(output_file, input_files):
    # Initialize an empty AudioSegment
    combined = AudioSegment.empty()

    # Loop through input files, loading and concatenating them
    for input_file in input_files:
        sound = AudioSegment.from_wav(input_file)
        combined += sound

    # Export the combined audio to a new file
    combined.export(output_file, format="wav")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py output.wav input1.wav input2.wav [input3.wav ...]")
        sys.exit(0)

    output_filename = sys.argv[1]
    input_filenames = sys.argv[2:]
    concatenate_wav_files(output_filename, input_filenames)
