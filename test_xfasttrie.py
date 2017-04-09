import unittest

from xfasttrie import XFastTrie

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.array = [1, 2, 3, 4, 5, 10, 20, 30, 100, 200]
        self.u = 256
        self.trie = XFastTrie(self.array, self.u)


    def test_find(self):
        for i in xrange(self.u):
            expected = i in self.array
            self.assertEqual(self.trie.find(i), expected)


    def test_predecessor(self):
        for i in xrange(self.u):
            correct = None
            for value in self.array:
                if value < i:
                    correct = value
                else:
                    break
            self.assertEqual(self.trie.predecessor(i), correct)


    def test_successor(self):
        for i in xrange(self.u):
            correct = None
            if i < self.array[-1]:
                for value in self.array:
                    if value > i:
                        correct = value
                        break
            self.assertEqual(self.trie.successor(i), correct)


if __name__ == '__main__':
    unittest.main()