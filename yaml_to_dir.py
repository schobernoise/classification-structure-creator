import os
import yaml
import argparse


def create_folder_structure(base_dir, classification_dict, level=0, max_levels=10):
    if level > max_levels:
        return

    # Process the current level of the dictionary
    for key, value in classification_dict.items():
        if value is None:
            continue  # Skip if value is None

        # Check if the value is a dictionary, which means we have a class with subclasses
        if isinstance(value, dict):
            # Retrieve the 'name' key if present, otherwise use an empty string
            dir_name = f"{key} {value.get('name', '')}".strip()
            current_dir = os.path.join(base_dir, dir_name)
            os.makedirs(current_dir, exist_ok=True)
            print(f"Created directory: {current_dir}")

            # If there are subclasses, recursively process them
            subclasses = value.get('subclasses', [])
            for subclass in subclasses:
                # Each subclass should be a dictionary with a single key-value pair
                if isinstance(subclass, dict):
                    create_folder_structure(current_dir, subclass, level + 1, max_levels)

        # If the value is a string, we have a subclass entry
        elif isinstance(value, str):
            dir_name = f"{key} {value}".strip()
            current_dir = os.path.join(base_dir, dir_name)
            os.makedirs(current_dir, exist_ok=True)
            print(f"Created directory: {current_dir}")           

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Create folder structure from a YAML file."
    )
    parser.add_argument("yaml_file", type=str, help="Path to the YAML file")
    parser.add_argument(
        "output_dir",
        type=str,
        help="Base output directory where folders will be created",
    )

    # Parse arguments
    args = parser.parse_args()

    # Read YAML file
    with open(args.yaml_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # Create the folder structure
    create_folder_structure(args.output_dir, data)


if __name__ == "__main__":
    main()
