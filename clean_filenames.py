import argparse
import os

__author__ = "Fabian Schober"
__version__ = "0.1.0"
__license__ = "MIT"

target_filelist = []

def target_to_filelist(target_dir):
    pdf_files = []
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            pdf_files.append(
                {
                "root": root,  
                "filepath": os.path.join(root, name), 
                "filename": name
                }
                )
    return pdf_files

def clean_filename(file):
    print(file)
    new_filename = file["filename"].replace("_"," ").replace(":"," ").replace("(auth.)","")
    os.rename(file["filepath"], os.path.join(file["root"], new_filename))


def main(args):
    target_filelist = target_to_filelist(args.target_dir)
    # print(target_filelist)

    for file in target_filelist:
        if file["filename"].endswith(".pdf") or file["filename"].endswith(".PDF"):
            print("processing file", file)
            clean_filename(file)


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
    
    args = parser.parse_args()
    main(args)
