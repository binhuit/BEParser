from unittest import TestCase
from utils import *
from tools import *
from constants import ROOT
from be_parser_model import BETrainingModel
from be_parser import BEParser
from beam import Beam

class TestBEParser(TestCase):
    sent = get_sample_sent()
    model = BETrainingModel()
    model.setup_model('test_data')

    def update_paramaters(self, state, value):
        features = state['features']
        cls = state['cls']
        self.model.update_paramaters(features, cls, value)

    def test_iter_2(self):
        parser = BEParser(self.model)
        parser.train_sent(self.sent)
        # take sent from corpus and update weight vector
        # according to this example
        self.model.update_perceptron_counter()
        # init state
        sent = [ROOT] + self.sent
        state = get_state(sent)
        # build gold tree
        gold_tree = get_tree(sent)
        beam = Beam(self.model.beam_size)
        top_valid_state = Beam(self.model.beam_size)
        pending = state['pending']
        prev_features = state['features']
        prev_score = state['score']
        arcs = state['arcs']
        for attachment_point in xrange(len(pending) - 1):
            local_features = features_extract(pending, arcs, attachment_point)
            # features extract funtion has not be built yet
            scores = self.model.get_scores(local_features)
            global_features = prev_features + local_features
            for cls_id, score in scores.iteritems():
                action = get_action(attachment_point, cls_id, self.model.label_hash)
                # check if action is valid
                valid_action = check_valid_action(pending, arcs, action, gold_tree)
                # apply action to pending
                new_pending, new_arcs = apply_action(pending, arcs, action)
                # create new state
                if prev_score == float('-inf'):
                    current_score = score
                else:
                    current_score = prev_score + score
                new_state = get_state(new_pending, global_features, current_score, cls_id, new_arcs)
                # add new state to beam
                beam.add(new_state)
                if valid_action:
                    top_valid_state.add(new_state)
        self.assertTrue(True)





