# The ClassMaker is cribbed from SO
# https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
# Classmaker and the @catalog_class.maker decorator allow class instantiation from
# strings. The main block can simply call the desired class using the convention
# argument instead of messy if/then/else blocks
# Instantiate the class maker with catalog_class = ClassMaker()

class ClassMaker:
    """ Class to instantiate other classes from strings"""

    def __init__(self):
        self.classes = {}

    def add_class(self, c):
        self.classes[c.__name__] = c

    # define the class decorator to return the class passed
    def maker(self, c):
        self.add_class(c)
        return c

    def __getitem__(self, n):
        return self.classes[n]


# instantiate a data crawler class maker object
crawler = ClassMaker()
