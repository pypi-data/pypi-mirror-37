import os
import json
from .dish import Dish

_dirname = os.path.dirname(__file__)
_path = os.path.join(_dirname,"recipes.json")

with open(_path, 'r') as json_file:
    _recipes = json.loads(json_file.read())

dishes = [Dish(r['name']) for r in _recipes]
