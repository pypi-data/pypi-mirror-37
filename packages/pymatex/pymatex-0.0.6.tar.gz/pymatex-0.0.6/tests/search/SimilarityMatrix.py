import unittest
from pymatex.search import SimilarityMatrix


class SimilarityMatrixTests(unittest.TestCase):

    def test_read(self):
        s = SimilarityMatrix(path='tests/search/resources/SimilarityMatrixTests.txt')

