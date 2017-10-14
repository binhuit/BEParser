from utils import read_corpus, get_state, get_tree
from constants import ROOT
import unittest


class TreeBuild(unittest.TestCase):
    sents = read_corpus('../data/toydata')

    def test_score(self):
        for sent in self.sents:
            sent = [ROOT] + sent
            arcs = get_tree(sent)
            state = get_state(sent, arcs=arcs)
            self.assertLess(state['score'],0)

    def test_gold_tree(self):
        for sent in self.sents:
            sent = [ROOT] + sent
            arcs = get_tree(sent)
            state = get_state(sent, arcs=arcs)
            self.assertEqual(len(sent), len(state['arcs']))

if __name__ == "__main__":
    unittest.main()
