from utils import read_corpus
from hash_table import HashTable
from constants import ROOT
import unittest


class LabelTest(unittest.TestCase):
    sents = read_corpus('../data/toydata')

    def label_set_len(self):
        label_hash = HashTable()
        for sent in self.sents:
            for token in sent:
                label_hash.add(token['prel'])
        self.assertEqual(label_hash.get_value(1), 'dep')


if __name__ == "__main__":
    unittest.main()