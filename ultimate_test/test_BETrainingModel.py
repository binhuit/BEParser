from unittest import TestCase
from utils import *
from tools import *
from constants import ROOT
from be_parser_model import BETrainingModel
from beam import Beam

class TestBETrainingModel(TestCase):
    sent = get_sample_sent()
    model = BETrainingModel()
    model.setup_model('test_data')

    def test_get_scores(self):
        pending = [ROOT] + self.sent
        for id in xrange(len(pending)-1):
            features = features_extract(pending, [], id)
            scores = self.model.get_scores(features)
            for cls, score in scores.iteritems():
                self.assertEqual(score,0.0)

    def update_paramaters(self, state, value):
        features = state['features']
        cls = state['cls']
        self.model.update_paramaters(features, cls, value)

    def test_top_correct(self):
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
                current_score = prev_score + score
                new_state = get_state(new_pending, global_features, current_score, cls_id, new_arcs)
                # add new state to beam
                beam.add(new_state)
                if valid_action:
                    top_valid_state.add(new_state)
        if not beam.has_element(top_valid_state.top()):
            self.update_paramaters(beam.top(), -1)
            self.update_paramaters(top_valid_state.top(), 1)

        hand_features = [['f1w___PAD__',  'f2w_bien', 'n1w_xoa', 'p1w___PAD__', 'f1t_ROOT',  'f2t_N', 'n1t_V',
                         'p1t___PAD__', 'f1tf2t_ROOT_N', 'p1tf1t___PAD___ROOT', 'f2tn1t_N_V'],
                         ['f1w_bien', 'f2w_xoa', 'n1w_tat_ca', 'p1w___PAD__',  'f1t_N',  'f2t_V',  'n1t_P',
                          'p1t_ROOT', 'f1tf2t_N_V', 'p1tf1t_ROOT_N', 'f2tn1t_V_P'],
                         ['f1w_xoa', 'f2w_tat_ca', 'n1w___PAD__', 'p1w_bien', 'f1t_V', 'f2t_P', 'n1t___PAD__', 'p1t_N',
                          'f1tf2t_V_P', 'f2tn1t_P___PAD__', 'p1tf1t_N_V']]
        features = hand_features[1]
        print self.model.get_scores(features)
        self.assertTrue(True)




