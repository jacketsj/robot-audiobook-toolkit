import argparse
import subprocess

# Assumes a toc.txt formatted as:
# Chapter title
# page number
# Chapter title
# page number
# [...]
# Chapter title
# page number
# last page number

def parse_toc(toc_file):
    with open(toc_file, 'r') as file:
        lines = file.readlines()
    
    chapters = []
    for i in range(0, len(lines) - 1, 2):
        chapter_title = lines[i].strip()
        print("Read chapter title: ", chapter_title)
        start_page = int(lines[i+1].strip())
        print("Read start page: ", start_page)
        if i + 3 < len(lines):
            end_page = int(lines[i+3].strip()) - 1
        else:
            end_page = int(lines[-1].strip())
        chapters.append((chapter_title, start_page, end_page))
    return chapters

def run_conversion(chapters, input_file, output_folder):
    for i, (title, start_page, end_page) in enumerate(chapters, start=1):
        output_file = f"{output_folder}/chapter_{i}_{title.replace(' ', '_')}.txt"
        page_range = f"{start_page}-{end_page}"
        command = f"./convert_to_text.sh \"{input_file}\" \"{output_file}\" \"{page_range}\""
        print(f"Processing: {title} | Pages: {page_range}")
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process chapters from a table of contents and convert them to text.")
    parser.add_argument('--toc_file', type=str, required=True, help="Path to the table of contents (TOC) file")
    parser.add_argument('--input_file', type=str, required=True, help="Path to the input PDF/EPUB file")
    parser.add_argument('--output_folder', type=str, required=True, help="Folder to save chapter text files")

    args = parser.parse_args()

    chapters = parse_toc(args.toc_file)
    run_conversion(chapters, args.input_file, args.output_folder)
