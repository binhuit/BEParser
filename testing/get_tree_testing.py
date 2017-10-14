from utils import read_corpus, get_tree
import unittest


class TreeBuild(unittest.TestCase):
    sents = read_corpus('../data/toydata')

    def test_len(self):
        for sent in self.sents:
            sent_len = len(sent)
            tree = get_tree(sent)
            tree_len = len(tree)
            self.assertEqual(sent_len, tree_len)

if __name__ == "__main__":
    unittest.main()
