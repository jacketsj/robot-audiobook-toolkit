import sys
import os
import fitz  # PyMuPDF
import ebooklib
from ebooklib import epub

def epub_to_text(epub_path):
    book = epub.read_epub(epub_path)
    text = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text.append(item.get_content().decode('utf-8'))

    return '\n\n'.join(text)

def pdf_to_text(pdf_path, page_range=None):
    doc = fitz.open(pdf_path)
    text = []
    
    if page_range:
        start_page, end_page = map(int, page_range.split('-'))
        pages = range(start_page-1, min(end_page, len(doc)))  # Adjust for 0-based index and limit to doc length
    else:
        pages = range(len(doc))

    for page_num in pages:
        page = doc.load_page(page_num)
        text.append(page.get_text())

    doc.close()
    return '\n\n'.join(text)

def convert_to_text(input_file, page_range=None):
    _, file_extension = os.path.splitext(input_file)
    if file_extension.lower() == '.epub':
        return epub_to_text(input_file)
    elif file_extension.lower() == '.pdf':
        return pdf_to_text(input_file, page_range)
    else:
        raise ValueError("Unsupported file format. Please use either a PDF or an EPUB file.")

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python convert_to_text.py input_file output.txt [page-range]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_txt = sys.argv[2]
    page_range = sys.argv[3] if len(sys.argv) == 4 else None

    try:
        text = convert_to_text(input_file, page_range)
        with open(output_txt, 'w') as f:
            f.write(text)
        print(f"Converted '{input_file}' to '{output_txt}'" + (f" for pages {page_range}" if page_range else ""))
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

