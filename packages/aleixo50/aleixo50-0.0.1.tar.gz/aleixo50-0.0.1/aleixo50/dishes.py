import os
import json
from .dish import Dish

dishes = []

with open(os.path.join(os.path.dirname(__file__),"recipes.json"), 'r') as json_file:
    _recipes = json.loads(json_file.read())

    dishes = [Dish(r['name']) for r in _recipes]

