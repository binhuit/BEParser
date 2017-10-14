from unittest import TestCase
from hash_table import HashTable
from utils import read_corpus, get_action, RIGHT, LEFT, get_edge, apply_action
from constants import ROOT


class TestApply_action(TestCase):
    sents = list(read_corpus('../data/toydata'))
    label_hash = HashTable()
    for sent in sents:
        for token in sent:
            label_hash.add(token['prel'])

    def test_apply_action(self):
        pending = [ROOT] + self.sents[1]
        before_length = len(pending)
        g_dependent = pending[1]['id']
        g_head = pending[2]['id']
        g_label = 'root'
        action = get_action(1, 7, self.label_hash)
        arcs = []
        apply_action(pending, arcs, action)
        self.assertEqual(1, len(arcs))
        self.assertTrue((g_dependent, g_head, g_label) in arcs)
        self.assertEqual(len(pending), before_length-1)

