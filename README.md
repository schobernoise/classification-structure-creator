# classification-structure-creator

> A tool to create and customize classification schemes like the Library of Congress Classification.

!This tool is stil under heavy development!

## Description

For years I have been fiddling around with organizing my personal collections of books and notes. Folder Structures emerged but were not consistent through media, due to time and the sheer amount of data. This was until I stumbled across the field of Libray Sciences and the science of classification.

There are several classifications with different approaches how to handle *stuff*. And with stuff I literally mean everything: physical objects, persons, animals, insects, everything that is touchable. But also notions, ideas, abstractions. The goal is to make our reality at least *this much* quantifiable, so it can be catalogued and conquered by mankind all over again.

This is why I came up with this script. By default it fetches the current [Library of Congress Classification](https://en.wikipedia.org/wiki/Library_of_Congress_Classification) from Wikipedia, parses it and either way pretty prints it to the console, saves it as yaml or creates a folder structure with it.

e.g. save standard LCC to a yaml file: `python3 ./classification-structure-creator.py save_yaml`

Actions to perform: save_yaml, create_folders, yaml_to_dir or print_yaml

options:
  -h, --help            show this help message and exit
  --dir DIR             Base directory, defaults to CWD/lcc
  --file FILE           Base YAML File to work with, defaults to CWD/lcc/classification.yaml
  --lang LANG           Language in which to fetch the Standard LCC. En and De are implemented. Defaults to En.

`create_folders` - Is taking in any yaml file with the given structure, defaults to max 10 levels of recursion.


## Recommended Workflow

1. Save existing Standard LCC to yaml file.
2. Work on it, customize it, add more levels.
3. Create a folder structure with the customized yaml.

You can also start with a blank yaml, just keep the following structure:

```yaml
'A':  allgemeine Arbeiten
    AC: Sammlungen. Serien. Gesammelte Werke
    AE: Enzyklopädien
        AE01: Allgemeine Enzyklopädien
    AG: Wörterbücher und andere allgemeine Nachschlagewerke
    AI: Indizes
```

## Dependencies

- https://pypi.org/project/Wikipedia-API/
- https://pypi.org/project/deep-translator/

Created with Python 3.10.12.