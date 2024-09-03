import argparse
import os
from pypdf import PdfReader
import re
import urllib.request
import json

__author__ = "Fabian Schober"
__version__ = "0.1.0"
__license__ = "MIT"

target_filelist = []
dest_dirlist = []


def target_to_filelist(target_dir):
    pdf_files = []
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            pdf_files.append(
                {
                "filepath": os.path.join(root, name), 
                "filename": clean_filename(name)
                }
                )
    return pdf_files

def dest_to_dirlist(dirlist_dir):
    dirs = []
    for root, dirs, files in os.walk(dirlist_dir, topdown=False):
        for name in dirs:
            # print(os.path.join(root, name))
            dirs.append(os.path.join(root, name))
    return dirs

def clean_filename(filename):
    return filename.replace("_", " ").replace("-", " ")

def pdf_existing_metadata_extractor(pdf_file):
    reader = PdfReader(pdf_file["filepath"])
    pdf_meta = reader.metadata
    
    pdf_file["title" ]= pdf_meta.title
    pdf_file["author"] = pdf_meta.author
    pdf_file["subject"] = pdf_meta.subject
    pdf_file["isbn"] = extract_isbns(reader)

    # print(pdf_file)

def extract_isbns(reader):

    text = ""
    number_of_pages = len(reader.pages)
    for i in range(9):
        page = reader.pages[i]
        text += page.extract_text()
   
    # print(text[100:])
    # Define a regex pattern to match ISBNs
    isbn_pattern = r"((978[-– ])?[0-9][0-9-– ]{10}[-– ][0-9xX])|((978)?[0-9]{9}[0-9Xx])"

    # Find all matches of the ISBN pattern in the text
    isbns = re.findall(isbn_pattern, text)
    # print(isbns)

    # Extract only the portions with numbers and dashes
    isbns_cleaned = [isbn[0] for isbn in isbns if isbn != '']

    return isbns_cleaned

def pdf_metadata_completion(pdf_file):

    basic_infos_obj = fetch_basic_infos(pdf_file["isbn"])
    # extended_infos_obj = open_library_search(pdf_file)
    # print(basic_infos_obj)

    pdf_file["title" ]= basic_infos_obj["title"]
    pdf_file["author"] = basic_infos_obj["authors"]
    pdf_file["subject"] = basic_infos_obj["subject"]
    pdf_file["categories"] = basic_infos_obj["categories"],

def write_to_pdf(pdf_file):

     # ! This Function writes to file !

    reader = PdfReader(pdf_file["filepath"])
    writer = PdfWriter()

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # If you want to add the old metadata, include these two lines
    if reader.metadata is not None:
        writer.add_metadata(reader.metadata)

    writer.add_metadata(
    {
        "/Author": pdf_file["author"],
        "/Title": pdf_file["title"],
        "/Subject": pdf_file["categories"],
        "/Isbn-10": pdf_file["ISBN_10"], # TODO: Split ISBN Object into 10 and 13
        "/Isbn-13": pdf_file["ISBN_13"],

    }
    )

    # Save the new PDF to a file
    with open(pdf_file["filepath"], "wb") as f:
        writer.write(f)

def fetch_basic_infos(isbn):
    base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    with urllib.request.urlopen(base_api_link + isbn[1]) as f:
        text = f.read()

    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text) # deserializes decoded_text to a Python object
    # print(obj["items"])
    return obj["items"]

def open_library_search(pdf_file):
    # https://openlibrary.org/dev/docs/api/books

    openlibrary_api_link = "https://openlibrary.org/search.json?q="

    with urllib.request.urlopen(openlibrary_api_link + isbn[1]) as f:
        text = f.read()

    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text) # deserializes decoded_text to a Python object
    # print(obj["items"])
    return obj["docs"][0]

def create_markdown_file(pdf_file):
    # Write isbn and all additional infos in there
    pass

def main(args):
    """ Main entry point of the app """

    target_filelist = target_to_filelist(args.target_dir)
    # dest_dirlist = dest_to_dirlist(args.dest_dir)

    for file in target_filelist:
        if file["filepath"].endswith(".pdf"):
            print("processing file", file)
            pdf_existing_metadata_extractor(file)
            pdf_metadata_completion(file)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()


    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    
    parser.add_argument(
        "-t",
        "--target_dir",
        default="./sorted",
        help="Target dir with files to be sorted.", action="store", dest="target_dir")
    
    parser.add_argument(
        "-d",
        "--dest_dir",
        help="Destination Dir, in which the files get sorted.", action="store", dest="dest_dir")
    
    
    args = parser.parse_args()
    main(args)
