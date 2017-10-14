from unittest import TestCase
from hash_table import HashTable
from utils import read_corpus, get_action, RIGHT, LEFT, get_edge
from constants import ROOT


class TestGet_edge(TestCase):
    sents = list(read_corpus('../data/toydata'))
    label_hash = HashTable()
    for sent in sents:
        for token in sent:
            label_hash.add(token['prel'])

    def test_get_edge(self):
        pending = [ROOT] + self.sents[1]
        action = get_action(1, 7, self.label_hash)
        g_head = pending[2]
        g_dependent = pending[1]
        dependent, head, label = get_edge(pending, action)
        self.assertEqual(g_head, head)
        self.assertEqual(g_dependent, dependent)

