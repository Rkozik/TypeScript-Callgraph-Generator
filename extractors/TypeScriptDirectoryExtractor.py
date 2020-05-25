from extractors.IExtractor import IExtractor
from directories.Directory import Directory
from os import listdir
import os


class TypeScriptDirectoryExtractor(IExtractor):
    def __init__(self, file_repository, root):
        self.file_repository = file_repository
        self.root = root

    def execute(self):
        root_directory_name = self.root.split('/')[-2]
        root_directory_path = self.root
        root_directory = Directory(root_directory_name, root_directory_path)
        self.file_repository.add_directory(root_directory)

        directories_unchecked = {self.root: [f for f in listdir(self.root)]}

        while bool(directories_unchecked) is True:
            current_parent = list(directories_unchecked)[0]
            files = directories_unchecked[current_parent]
            for file in files:
                if os.path.isdir(current_parent + file):
                    directories_unchecked[current_parent + file + "/"] = [f for f in listdir(current_parent + file + "/")]
                    new_directory_name = file
                    new_directory_path = current_parent + file + "/"
                    new_directory = Directory(new_directory_name, new_directory_path)
                    self.file_repository.add_directory(new_directory)

                elif file[-3:] == ".ts" and file[-5:] != ".d.ts":
                    parent_directory = self.file_repository.get_directory(current_parent)
                    parent_directory.add_file(current_parent+file)

                files.remove(file)

                if len(files) == 0:
                    directories_unchecked.pop(current_parent)
