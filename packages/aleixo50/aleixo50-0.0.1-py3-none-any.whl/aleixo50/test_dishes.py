import unittest
import aleixo50
print(aleixo50)

from aleixo50 import dishes
from aleixo50.dish import Dish

class RandTest(unittest.TestCase):
    def test_rand_type(self):
        self.assertEqual(len(dishes), 50)

if __name__ == '__main__':
    unittest.main()
