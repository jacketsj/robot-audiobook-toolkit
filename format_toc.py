import re
import sys

def process_input_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = []
    current_title = ''
    page_number_pattern = re.compile(r'.*\d+$')
    page_header_pattern = re.compile(r'^Page \|')

    for line in lines:
        if page_header_pattern.match(line):
            continue  # Skip lines starting with "Page | "

        stripped_line = line.strip()
        if page_number_pattern.match(stripped_line):
            title, page_number = stripped_line.rsplit(' ', 1)
            title = (current_title + " " + title).strip()
            title = re.sub(r'\s*\.\.\.*\s*', ' ', title).strip()  # Handle dots in multiline titles
            current_title = ''  # Reset for the next title
            processed_lines.append(f"{title}\n{page_number}\n")
        else:
            if stripped_line:  # Accumulate title parts if not empty
                current_title += " " + stripped_line if current_title else stripped_line

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in processed_lines:
            output_file.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <input_file_path> <output_file_path>")
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        process_input_file(input_file_path, output_file_path)

