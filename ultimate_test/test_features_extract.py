from unittest import TestCase
from constants import ROOT
from utils import *
from tools import *


class TestFeaturesExtract(TestCase):
    sent = get_sample_sent()

    def test_features_extract(self):
        pending = [ROOT]+self.sent
        arcs = []
        hand_features = [['f1w___PAD__',  'f2w_bien', 'n1w_xoa', 'p1w___PAD__', 'f1t_ROOT',  'f2t_N', 'n1t_V',
                         'p1t___PAD__', 'f1tf2t_ROOT_N', 'p1tf1t___PAD___ROOT', 'f2tn1t_N_V'],
                         ['f1w_bien', 'f2w_xoa', 'n1w_tat_ca', 'p1w___PAD__',  'f1t_N',  'f2t_V',  'n1t_P',
                          'p1t_ROOT', 'f1tf2t_N_V', 'p1tf1t_ROOT_N', 'f2tn1t_V_P'],
                         ['f1w_xoa', 'f2w_tat_ca', 'n1w___PAD__', 'p1w_bien', 'f1t_V', 'f2t_P', 'n1t___PAD__', 'p1t_N',
                          'f1tf2t_V_P', 'f2tn1t_P___PAD__', 'p1tf1t_N_V']]
        for id, features in enumerate(hand_features):
            test_features = features_extract(pending, arcs, id)
            self.assertTrue(compare_features(features, test_features))

