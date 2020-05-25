import os
import click
from os import listdir
from helpers import files


@click.command()
@click.option('--root', default=None, help='Root folder of the TypeScript project.')
@click.option('--calling-class', default=None, help='The class accessing other classes.')
@click.option('--called-class', default=None, help='The class being called other classes.')
@click.option('--output-name', default=None, help='The class being called other classes.')
def main(root, calling_class, called_class, output_name):
    if root is None:
        root = "/Users/robertkozik/sites/php2/api/get/ts/"

    typescript_class_calls = get_typescript_class_calls(root)

    dotFile = open("dotFile.dot", "w")
    dotFile.write("digraph {\n")
    dotFile.write('\trankdir="LR"\n')

    for the_class_called in typescript_class_calls:
        for the_calling_class in typescript_class_calls[the_class_called]:

            if calling_class is not None and called_class is not None:
                if the_calling_class == calling_class or the_class_called == called_class:
                    dotFile.write("\t" + the_calling_class + " -> " + the_class_called + ";\n")
            elif calling_class is not None:
                if the_calling_class == calling_class:
                    dotFile.write("\t" + the_calling_class + " -> " + the_class_called + ";\n")
            elif called_class is not None:
                if the_class_called == called_class:
                    dotFile.write("\t" + the_calling_class + " -> " + the_class_called + ";\n")
            else:
                dotFile.write("\t" + the_calling_class + " -> " + the_class_called + ";\n")

    dotFile.write("}\n")
    dotFile.close()

    output_image = output_name if output_name is not None else "class.png"
    os.system("dot -T png -o "+output_image+" dotFile.dot")


def get_typescript_class_calls(root):
    typescript_files = get_typescript_files(root)
    typescript_classes = get_typescript_classes(root)

    for typescript_class in typescript_classes:
        for typescript_file in typescript_files:
            # Because multiple classes can exist in 1 file we need to keep track
            # of which file we're looking at
            with open(typescript_file) as theFile:
                current_class = ""
                for line in theFile:
                    if files.extract_class_name(line) is not None:
                        current_class = files.extract_class_name(line)

                    if "new " + typescript_class in line or "<" + typescript_class + ">" in line or ": " + typescript_class in line:
                        # Using a dictionary to prevent multiple arrows for multiple calls
                        if current_class is not "":
                            typescript_classes[typescript_class].update({current_class: 0})

            theFile.close()
    return typescript_classes


def get_typescript_classes(root):
    typescript_files = get_typescript_files(root)

    typescript_classes = {}
    for file in typescript_files:
        with open(file) as theFile:
            for line in theFile:
                class_name = files.extract_class_name(line)
                if class_name:
                    typescript_classes.update({class_name: {}})

        theFile.close()
    return typescript_classes


def get_typescript_files(root):
    directories = get_directories(root)

    type_script_files = []
    for directory in directories:
        for file in listdir(directory):
            # Extract TypeScript files only
            if file[-3:] == ".ts" and file[-5:] != ".d.ts":
                type_script_files.append(directory+file)

    return type_script_files


def get_directories(root):
    directories = [root]
    directories_unchecked = {root: [f for f in listdir(root)]}

    while bool(directories_unchecked) is True:
        current_parent = list(directories_unchecked)[0]
        files = directories_unchecked[current_parent]
        for file in files:

            if os.path.isdir(current_parent+file):
                directories_unchecked[current_parent+file+"/"] = [f for f in listdir(current_parent+file+"/")]
                directories.append(current_parent+file+"/")

            files.remove(file)

            if len(files) == 0:
                directories_unchecked.pop(current_parent)

    return directories


if __name__ == '__main__':
    main()