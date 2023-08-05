class Dish(object):
    def __init__(self, name, ingredients=[], instructions=[]):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def __repr__(self):
        return 'Dish({0.name!r}, {0.ingredients!r}, {0.instructions!r})'.format(self)

    def __str__(self):
        return 'Dish({0.name})'.format(self)


