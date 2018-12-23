class User(object):
    def __init__(self, name):
        self.name = name

    def _set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

