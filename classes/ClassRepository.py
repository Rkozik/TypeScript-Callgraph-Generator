class ClassRepository:
    def __init__(self):
        self.classes = []

    def add_class(self, the_class: str):
        self.classes.append(the_class)

    def get_classes(self):
        return self.classes

    def get_class(self, class_requested):
        for stored_class in self.get_classes():
            if stored_class.get_name() == class_requested:
                return stored_class
