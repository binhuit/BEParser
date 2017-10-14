from unittest import TestCase
from tools import *
from constants import ROOT
from utils import *
from hash_table import HashTable


class TestApplyAction(TestCase):
    sent = get_sample_sent()
    label_hash = get_sample_label_hash()

    def test_apply_action(self):
        pending = [ROOT] + self.sent
        arcs = []
        n_cls = len(self.label_hash) * 2
        for id in xrange(len(pending)-1):
            for cls in xrange(n_cls):
                action = get_action(id, cls, self.label_hash)
                new_pending, new_arcs = apply_action(pending, arcs, action)
                direction = cls / len(self.label_hash)
                if direction == 0:
                    self.assertTrue(not pending[id+1] in new_pending)
                else:
                    self.assertTrue(not pending[id] in new_pending)

    def test_apply_action_arcs(self):
        gold_arcs = [(1,0,'sub'), (1,0,'root'), (1,0,'dob'), (0,1,'sub'),(0,1,'root'),(0,1,'dob')]
        pending = [ROOT] + self.sent
        arcs = []
        n_cls = len(self.label_hash) * 2
        id = 0
        for cls in xrange(n_cls):
            action = get_action(id, cls, self.label_hash)
            new_pending, new_arcs = apply_action(pending, arcs, action)
            child_id, parent_id, label = gold_arcs[cls]
            arcs = (pending[child_id], pending[parent_id], label)
            self.assertTrue(arcs in new_arcs)



