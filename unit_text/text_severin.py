import unittest

import unittest

def est_pair_ou_impair(nombre):
    if nombre % 2 == 0:
        return "pair"
    else:
        return "impair"

class TestEstPairOuImpair(unittest.TestCase):
    def test_pair(self):
        self.assertEqual(est_pair_ou_impair(2), "pair")
        self.assertEqual(est_pair_ou_impair(4), "pair")
        self.assertEqual(est_pair_ou_impair(0), "pair")

    def test_impair(self):
        self.assertEqual(est_pair_ou_impair(3), "impair")
        self.assertEqual(est_pair_ou_impair(5), "impair")
        self.assertEqual(est_pair_ou_impair(7), "impair")

if __name__ == "__main__":
    unittest.main()