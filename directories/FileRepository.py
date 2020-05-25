class FileRepository:
    directories = []

    def __init__(self):
        pass

    def add_directory(self, directory):
        self.directories.append(directory)

    def get_directories(self):
        return self.directories

    def get_directory(self, path):
        for directory in self.get_directories():
            if directory.get_path() == path:
                return directory
