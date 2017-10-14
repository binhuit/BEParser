from unittest import TestCase
from hash_table import HashTable
from utils import *
from constants import ROOT


class TestCheck_valid_action(TestCase):
    sents = list(read_corpus('../data/toydata'))
    label_hash = HashTable()
    for sent in sents:
        for token in sent:
            label_hash.add(token['prel'])

    def test_check_valid_action(self):
        print "test case 1"
        pending = [ROOT] + self.sents[1]
        arcs = []
        gold_tree = get_tree(pending)
        action = get_action(0,0,self.label_hash)
        invalid = check_valid_action(pending, arcs, action, gold_tree)
        self.assertFalse(invalid)

    def test_check_valid_action_case_2(self):
        print "test case 2"
        pending = [ROOT] + self.sents[1]
        arcs = []
        gold_tree = get_tree(pending)
        action = get_action(1, 3, self.label_hash)
        valid = check_valid_action(pending, arcs, action, gold_tree)
        self.assertTrue(valid)

    def test_check_valid_action_case_3(self):
        print "test case 3"
        pending = [ROOT] + self.sents[1]
        arcs = []
        gold_tree = get_tree(pending)
        action = get_action(1, 3, self.label_hash)
        valid = check_valid_action(pending, arcs, action, gold_tree)
        self.assertTrue(valid)

