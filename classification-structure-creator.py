import wikipediaapi
from collections import defaultdict
import os
import yaml
import argparse
from deep_translator import GoogleTranslator


def get_lcc_from_wikipedia(lang):

    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent="LCC(merlin@example.com)",
        language="en",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
    )
    p_wiki = wiki_wiki.page("Library of Congress Classification")

    return_dict = {}

    if lang:
        return_dict = translate_dict(
            parse_classification_outline(trim_classification_text(p_wiki.text)), lang
        )
    else:
        return_dict = parse_classification_outline(
            trim_classification_text(p_wiki.text)
        )

    return return_dict


def translate_dict(d, lang):
    """
    Recursively translate all string values in a dictionary.

    :param d: The dictionary to translate.
    :param lang: The target language code (e.g., 'fr' for French).
    :return: A new dictionary with translated values.
    """
    translated_dict = {}
    for key, value in d.items():
        if isinstance(value, dict):
            # Recursively translate dictionaries
            translated_dict[key] = translate_dict(value, lang)
        elif isinstance(value, list):
            # Translate lists
            translated_dict[key] = [
                (
                    translate_dict(v, lang)
                    if isinstance(v, dict)
                    else translate_text(lang, v) if isinstance(v, str) else v
                )
                for v in value
            ]
        elif isinstance(value, str):
            # Translate strings
            translated_dict[key] = translate_text(lang, value)
        else:
            # Copy other types without modification
            translated_dict[key] = value
    return translated_dict


def translate_text(lang, text):
    # Helper function to split text into chunks
    def split_text_into_chunks(text, max_chunk_size=5000):
        chunks = []
        current_chunk = []
        current_length = 0

        for line in text.splitlines(keepends=True):
            line_length = len(line)
            if current_length + line_length > max_chunk_size:
                chunks.append("".join(current_chunk))
                current_chunk = [line]
                current_length = line_length
            else:
                current_chunk.append(line)
                current_length += line_length

        if current_chunk:
            chunks.append("".join(current_chunk))

        return chunks

    # Split text into manageable chunks
    chunks = split_text_into_chunks(text)

    # Translate each chunk and concatenate results
    translated_chunks = [
        GoogleTranslator(source="auto", target=lang).translate(chunk)
        for chunk in chunks
    ]
    translated_text = "".join(translated_chunks)

    return translated_text


def parse_classification_outline(text):
    classification_dict = defaultdict(dict)
    current_class = None
    current_subclass = None

    for line in text.splitlines():
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Check if the line is a Class
        if line.startswith("Class "):
            if " – " in line:
                # Split by ' – ' to separate the class code and description
                class_code, class_desc = line.split(" – ", 1)
                current_class = class_code.replace("Class", "")
                classification_dict[current_class] = {
                    "description": class_desc,
                    "subclasses": {},
                }
            else:
                # Handle cases where the line doesn't follow the expected format
                print(f"Warning: Class line not in expected format: '{line}'")

        # Check if the line is a Subclass
        elif line.startswith("Subclass ") or line.startswith("Subclasses "):
            if " – " in line:
                # Split by ' – ' to separate the subclass code and description
                subclass_code, subclass_desc = line.split(" – ", 1)
                current_subclass = subclass_code.replace("Subclasses ", "").replace(
                    "Subclass ", ""
                )
                classification_dict[current_class]["subclasses"][
                    current_subclass
                ] = subclass_desc
            else:
                # Handle cases where the line doesn't follow the expected format
                print(f"Warning: Subclass line not in expected format: '{line}'")

    return classification_dict


def trim_classification_text(text):
    # Define start and end markers
    start_marker = "Full classification outline"
    end_marker = "Subclass ZA – Information resources/materials"

    # Find the start and end positions
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)

    # Ensure both markers are found
    if start_index == -1 or end_index == -1:
        return None

    # Slice the text to include the content between the markers
    # Add the length of the end_marker to include the line with "Subclass ZA"
    trimmed_text = text[start_index : end_index + len(end_marker)]

    return trimmed_text


def create_folder_structure(base_dir, classification_dict, level=0, max_levels=10):
    """
    Recursively creates a folder structure based on a nested classification dictionary.

    Args:
        base_dir (str): The base directory where the folder structure will be created.
        classification_dict (dict): The classification dictionary to convert into folders.
        level (int): The current recursion level.
        max_levels (int): The maximum recursion levels allowed (default is 10).
    """
    if level > max_levels:
        return

    for code, details in classification_dict.items():
        # Determine directory name
        if isinstance(details, dict) and "description" in details:
            dir_name = f"{code} - {details['description'][:150]}"
        else:
            dir_name = f"{code} - {str(details)[:150]}"

        # Create the directory
        current_dir = os.path.join(base_dir, dir_name)
        os.makedirs(current_dir, exist_ok=True)

        # Recursively create subdirectories if 'subclasses' exist
        if isinstance(details, dict):
            if "subclasses" in details:
                create_folder_structure(
                    current_dir, details["subclasses"], level + 1, max_levels
                )
            else:
                # Recursively process any further nested dictionaries
                for sub_key, sub_value in details.items():
                    if isinstance(sub_value, dict):
                        create_folder_structure(
                            current_dir, {sub_key: sub_value}, level + 1, max_levels
                        )


def create_external_folder_structure(
    base_dir, classification_dict, level=0, max_levels=10
):
    """
    Recursively creates a folder structure based on a nested classification dictionary.

    Args:
        base_dir (str): The base directory where the folder structure will be created.
        classification_dict (dict): The classification dictionary to convert into folders.
        level (int): The current recursion level.
        max_levels (int): The maximum recursion levels allowed (default is 10).
    """
    if level > max_levels:
        return

    for code, details in classification_dict.items():
        # Determine directory name
        if isinstance(details, dict) and "description" in details:
            dir_name = f"{code} - {details['description'][:150]}"
        else:
            dir_name = f"{code} - {str(details)[:150]}"

        # Create the directory
        current_dir = os.path.join(base_dir, dir_name)
        os.makedirs(current_dir, exist_ok=True)

        # Recursively create subdirectories if 'subclasses' exist
        if isinstance(details, dict):
            if "subclasses" in details:
                create_folder_structure(
                    current_dir, details["subclasses"], level + 1, max_levels
                )
            else:
                # Recursively process any further nested dictionaries
                for sub_key, sub_value in details.items():
                    if isinstance(sub_value, dict):
                        create_folder_structure(
                            current_dir, {sub_key: sub_value}, level + 1, max_levels
                        )


def load_yaml_file(file_path):
    """
    Loads a YAML file into a dictionary.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The loaded YAML as a dictionary.
    """
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def dict_to_yaml_hierarchy(classification_dict):
    # Convert the classification dictionary to a YAML string with indentation
    yaml_str = yaml.dump(
        dict(classification_dict),
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )
    return yaml_str


def pretty_print_hierarchy(classification_dict):
    yaml_str = dict_to_yaml_hierarchy(classification_dict)
    print(yaml_str)


def save_yaml_to_file(classification_dict, file_path):
    """
    Saves the classification dictionary as a YAML file.

    Args:
        classification_dict (dict): The classification dictionary to save.
        file_path (str): The path to the output YAML file.
    """
    os.makedirs(file_path.replace("classification.yaml", ""), exist_ok=True)
    with open(file_path, "w") as file:
        yaml.dump(
            dict(classification_dict),
            file,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
        )
    print(f"YAML file saved to {file_path}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Library of Congress Classification (LCC)"
    )
    parser.add_argument(
        "action",
        choices=["create_folders", "print_yaml", "save_yaml", "yaml_to_dir"],
        help="Action to perform: save_yaml, create_folders, yaml_to_dir or print_yaml",
    )
    parser.add_argument(
        "--dir",
        default="./lcc/",
        help="Base directory, defaults to CWD/lcc",
    )
    parser.add_argument(
        "--file",
        default="./lcc/classification.yaml",
        help="Base YAML File to work with, defaults to CWD/lcc/classification.yaml",
    )
    parser.add_argument(
        "--lang",
        help="Language in which to fetch the Standard LCC. En and De are implemented. Defaults to En.",
        default="en",
    )

    args = parser.parse_args()

    if args.action == "create_folders":
        lcc_dict = get_lcc_from_wikipedia(args.lang)
        create_folder_structure(args.dir, lcc_dict)

    elif args.action == "print_yaml":
        lcc_dict = get_lcc_from_wikipedia(args.lang)
        pretty_print_hierarchy(lcc_dict)

    elif args.action == "save_yaml":
        lcc_dict = get_lcc_from_wikipedia(args.lang)
        save_yaml_to_file(lcc_dict, args.file)

    elif args.action == "yaml_to_dir":
        create_external_folder_structure(args.dir, load_yaml_file(args.file))
