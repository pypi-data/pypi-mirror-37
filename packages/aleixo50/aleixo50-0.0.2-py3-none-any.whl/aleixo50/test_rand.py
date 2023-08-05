import unittest
import aleixo50
print(aleixo50)

from aleixo50 import rand
from aleixo50.dish import Dish

class RandTest(unittest.TestCase):
    def test_rand_type(self):
        self.assertIsInstance(rand(), Dish)

if __name__ == '__main__':
    unittest.main()
