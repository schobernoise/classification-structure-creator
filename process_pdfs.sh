#!/bin/bash

# Check for required arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <target_directory> <destination_directory>"
  exit 1
fi

TARGET_DIR="$1"
DEST_DIR="$2"
PYTHON_SCRIPT="/home/fabian/Projects/316 Classification Structure Creator/°~ DEV/classification-structure-creator/automatic_pdf_sorter.py"

# Verify the target directory exists
if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: Target directory '$TARGET_DIR' does not exist."
  exit 1
fi

# Verify the destination directory exists
if [ ! -d "$DEST_DIR" ]; then
  echo "Error: Destination directory '$DEST_DIR' does not exist."
  exit 1
fi

# Verify the python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "Error: Python script '$PYTHON_SCRIPT' does not exist."
  exit 1
fi

# Find all PDF files in the target directory and its subdirectories
find "$TARGET_DIR" -type f -name '*.pdf' | while IFS= read -r pdf_file; do
  echo "Processing: $pdf_file"

  # Run the python script with the PDF file as an argument
  python3 "$PYTHON_SCRIPT" -f "$pdf_file"
  
  # Use fzf to select the destination directory
  destination=$(find "$DEST_DIR" -type d | fzf --prompt="Select destination directory for $pdf_file: ")

  # Move the PDF file to the selected destination directory
  if [ -n "$destination" ]; then
    mv "$pdf_file" "$destination/"
    echo "Moved $pdf_file to $destination"
  else
    echo "No destination selected. Skipping $pdf_file."
  fi
done
