from unittest import TestCase
from hash_table import HashTable
from utils import read_corpus, get_action, RIGHT, LEFT
from constants import ROOT


class TestGet_action(TestCase):
    sents = list(read_corpus('../data/toydata'))
    label_hash = HashTable()
    for sent in sents:
        for token in sent:
            label_hash.add(token['prel'])
    actions = [get_action(1,i,label_hash) for i in xrange(12)]
    def test_get_action(self):
        for i, action in enumerate(self.actions):
            direction = action['direction']
            test_direction = i / len(self.label_hash)
            self.assertEqual(direction, test_direction)
