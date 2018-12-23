class Problem(object):
    def __init__(self, name, contents):
        self.name = name
        self.contents = contents

    def _set_name(self, name):
        self.name = name

    def _set_contents(self, contents):
        self.contents = contents

    def get_name(self):
        return self.name

    def get_contents(self):
        return self.contents
