class TypeScriptClass:
    extension = ".ts"

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.methods = []
        self.fields = []
        self.calls = []
        self.calledBy = []

    def get_name(self):
        return self.name

    def add_method(self, method: str):
        self.methods.append(method)

    def get_methods(self):
        return self.methods

    def add_field(self, field: str):
        self.fields.append(field)

    def get_fields(self):
        return self.fields

    def add_call(self, call, method):
        self.calls.append((call, method))

    def get_calls(self):
        return self.calls

    def add_called_by(self, called_by, method):
        self.calledBy.append((called_by, method))

    def get_called_by(self):
        return self.calledBy

    def get_path(self):
        return self.path
