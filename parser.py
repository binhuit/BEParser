from beam import Beam
from constants import ROOT
from utils import get_label_conll, get_action, get_tree,\
    get_state, read_corpus, features_extract, apply_action, check_valid_action, compare_arcs
from hash_table import HashTable
from ml.ml import MultitronParameters


class BEParser:
    def __init__(self, beam_size):
        self.beam_size = beam_size
        self.label_hash = HashTable()
        self.n_class = None
        self.scorer = None
        self.train_data = None

    def setup_training_data(self, corpus_file):
        self.train_data = read_corpus(corpus_file)
        # index dependency label
        for label in get_label_conll(corpus_file):
            self.label_hash.add(label)
        self.n_class = len(self.label_hash) * 2
        self.scorer = MultitronParameters(self.n_class)

    def train(self, train_data):
        for sent in train_data:
            self.train_sent(sent)

    def train_sent(self, sent):
        # take sent from corpus and update weight vector
        # according to this example

        # init state
        sent = [ROOT] + sent
        init_state = get_state(sent)
        # build gold tree
        gold_tree = get_tree(sent)
        beam = Beam(self.beam_size)
        top_valid_state = None
        beam.add(init_state)
        # loop n-1 step
        step = 0
        # above check
        for i in xrange(len(sent)-1):
            step += 1
            # extend current beam
            beam, top_valid_state = self.extend_beam(beam, gold_tree)
            # checking here

            if not beam.has_element(top_valid_state.top()):
                self.update_paramaters(beam.top(), -1)
                self.update_paramaters(top_valid_state.top(), 1)
                break
        if step == len(sent)-1:
            top_beam = beam.top()
            predict_arcs = top_beam['arcs']
            if not compare_arcs(predict_arcs, gold_tree):
                self.update_paramaters(top_beam, -1)
                self.update_paramaters(top_valid_state.top(), 1)

    def extend_beam(self, beam, gold_tree):
        """
        
        :param beam: 
        :return: beam, top_valid_state 
        """
        new_beam = Beam(beam_size=self.beam_size)
        top_valid_state = Beam(beam_size=1)

        for state in beam:
            pending = state['pending']
            prev_features = state['features']
            prev_score = state['score']
            arcs = state['arcs']
            for attachment_point, tok1, tok2 in zip(pending, pending[1:]):
                # at this point you could create two new state
                local_features = features_extract(pending, arcs, attachment_point)
                # features extract funtion has not be built yet
                scores = self.scorer.get_scores(local_features)
                global_features = prev_features + local_features
                for cls_id,score in enumerate(scores):
                    action = get_action(attachment_point, cls_id, self.label_hash)
                    # check if action is valid
                    valid_action = check_valid_action(pending, arcs, action, gold_tree)
                    # apply action to pending
                    new_pending, new_arcs = apply_action(pending, arcs, action)
                    # create new state
                    current_score = prev_score + score
                    new_state = get_state(new_pending, global_features, current_score, cls_id, new_arcs)
                    # add new state to beam
                    new_beam.add(new_state)
                    if valid_action:
                        top_valid_state.add(new_state)
        return new_beam, top_valid_state

    def update_paramaters(self, state, value):
        features = state['features']
        cls = state['cls']
        self.scorer.add(features, cls, value)
