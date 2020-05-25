class Directory:
    name: str
    path: str

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.files = []

    def add_file(self, file_name: str):
        self.files.append(file_name)

    def get_files(self):
        return self.files

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path
