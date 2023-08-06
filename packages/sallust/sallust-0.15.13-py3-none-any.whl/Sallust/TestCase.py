class TestCase:
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def set_test_name(self, name):
        self.name = name
