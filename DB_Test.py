import unittest
import pythonTestFramework.Generation.GenerationData as gen

class print_test(unittest.TestCase):
    def test_pass(self):
        print "Hello"

    # def genOrder(self):
        # g = gen.GenerationData()
        # print g.generate_data("Order")

    def test_fail(self):
        assert 2 == 3

    def test_error(self):
        x = 2 / 0
