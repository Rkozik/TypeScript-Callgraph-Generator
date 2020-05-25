from extractors.IExtractor import IExtractor
from classes.TypeScriptClass import TypeScriptClass
from helpers import files


class TypeScriptClassExtractor(IExtractor):
    def __init__(self, file_repository, class_repository):
        self.file_repository = file_repository
        self.class_repository = class_repository

    def execute(self):
        for directory in self.file_repository.get_directories():
            for file in directory.get_files():
                with open(file) as theFile:
                    current_class = None
                    for line in theFile:

                        # Extract class name
                        class_name = files.extract_class_name(line)
                        if class_name:
                            new_class = TypeScriptClass(class_name, directory.get_path())
                            self.class_repository.add_class(new_class)
                            current_class = class_name

                        if current_class is not None:
                            # Extract class fields
                            field_name = files.extract_field_name(line)
                            if field_name:
                                current_class_object = self.class_repository.get_class(current_class)
                                current_class_object.add_field(field_name)

                            # Extract class methods
                            method_name = files.extract_method_name(line)
                            if method_name:
                                current_class_object = self.class_repository.get_class(current_class)
                                current_class_object.add_method(method_name)

                theFile.close()
