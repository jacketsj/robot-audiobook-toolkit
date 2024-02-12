This toolkit is for generating robot-audiobooks from PDFs, by making use of [WhisperSpeech](https://github.com/collabora/WhisperSpeech).

Usage guidelines:
1. Use a PDF file for a book.
2. Use 'convert_to_text.sh' to read the table of contents (e.g., on pages 2-3):
```sh
./convert_to_text.sh example.pdf toc-unformatted.txt 2-3
```
3. Format the outputted text as follows:
```
Chapter title
page number
Chapter title
page number
[...repeat]
Chapter title
page number
last page number
```
You may be able to use or modify the `format_toc.py` tool for this purpose, depending on the initial format:
```sh
python3 format_toc.py toc-unformatted.txt toc.txt
```
4. Use your TOC to parse each chapter into text:
```sh
python3 parse_toc.py --toc_file toc.txt --input_file example.pdf --output_folder chapter_texts
```
This should result in a txt file for each chapter in `chapter_texts/` (or somewhere else if you specified differently).
5. Get a custom voice sample. It should be the voice only, wav format, and ideally about ~30 seconds.
6. Use the `run_many.sh` script to generate audio for each chapter into `output/`:
```sh
./run_many.sh --voice voice_sample.wav --filter_pattern "Page \| .*" chapter_texts/*.txt
```
The `--filter_pattern` argument is for filtering out lines of text containing things like page numbers. It can be omitted, or replaced with a different pattern.
7. Use the `concatenate_wav_files.py` script to generate a single, large, audio file:
```sh
python3 concatenate_wav_files.py output.wav output/chapter*.wav
```
8. Convert to an mp3 (or other compressed format) with a different program of your choice, and start listening.
