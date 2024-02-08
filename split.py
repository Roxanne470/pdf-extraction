"""
This script consist of:
* Collect Pdf Files from uploads folder
* Split Pdf Files page by page.
* Save Splitted pdf pages to output Folder.
"""

import os, sys
import time
from PyPDF2 import PdfReader, PdfWriter


def splitting(upload_folder, split_folder):
    '''Do collect PDF files, split pages and save them
    '''

    entries = os.listdir(upload_folder)
    path = os.path.abspath(split_folder)

    for entry in entries:

        uploaded_file = os.path.join(upload_folder, entry)
        output_file_folder = os.path.join(path, entry)

        if not os.path.isdir(output_file_folder):
            os.mkdir(output_file_folder)

        pdf = PdfReader(uploaded_file, strict=False)
        # print(len(pdf.pages))
        for page in range(len(pdf.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf.pages[page])
            output_filename = \
                os.path.join(output_file_folder, f'{page+1}.pdf')
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
            print("Usage: python3 split.py upload_folder split_folder")
            sys.exit(1)

    upload_folder = sys.argv[1]
    split_folder = sys.argv[2]

    start_time = time.time()

    splitting(upload_folder, split_folder)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

