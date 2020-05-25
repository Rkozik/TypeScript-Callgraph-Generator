from extractors.IExtractor import IExtractor
from helpers import files


class TypeScriptClassCallsExtractor(IExtractor):
    def __init__(self, file_repository, class_repository):
        self.file_repository = file_repository
        self.class_repository = class_repository

    def execute(self):
        for typescript_class in self.class_repository.get_classes():
            typescript_class = typescript_class.get_name()

            for directory in self.file_repository.get_directories():
                for file in directory.get_files():
                    with open(file) as theFile:
                        current_class = None
                        current_method = None
                        for line in theFile:
                            line = line.strip()

                            if files.extract_class_name(line) is not None:
                                current_class = files.extract_class_name(line)

                            if files.extract_method_name(line) is not None:
                                current_method = files.extract_method_name(line)

                            if "new " + typescript_class in line or "<" + typescript_class + ">" in line or ": " + typescript_class in line:
                                # Line isn't a field or a new method declaration
                                if files.extract_field_name(line) is None and current_class is not None and current_method is not None:
                                    # Lines isn't commented out
                                    if line[0] != "/" and line[0] != "*":

                                        # Log who the current class is calling
                                        class_from_repo = self.class_repository.get_class(current_class)
                                        class_from_repo.add_call(typescript_class, current_method)

                                        # Register the event with class we're accessing
                                        called_class_from_repo = self.class_repository.get_class(typescript_class)
                                        called_class_from_repo.add_called_by(current_class, current_method)

                    theFile.close()
