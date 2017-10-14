from beam import Beam
from constants import ROOT
from utils import *
from be_parser_model import BETrainingModel


class BEParser:
    def __init__(self, model=None):
        self.model = model

    def train(self, corpus_file, iter):
        train_data = list(read_corpus(corpus_file))
        print "Training data ..."
        for ITER in xrange(1,iter+1):
            print "iter "+str(ITER)
            for i,sent in enumerate(train_data):
                if i % 100 == 0:
                    print i
                self.train_sent(sent)
            self.model.save_weight_file(str(ITER))
        self.model.save_weight_file('FINAL')

    def train_sent(self, sent):
        # take sent from corpus and update weight vector
        # according to this example
        self.model.update_perceptron_counter()
        # init state
        sent = [ROOT] + sent
        init_state = get_state(sent)
        # build gold tree
        gold_tree = get_tree(sent)
        beam = Beam(self.model.beam_size)
        top_valid_state = None
        beam.add(init_state)
        # loop n-1 step
        step = 0
        # above check
        for i in xrange(len(sent)-1):
            step += 1
            # extend current beam
            beam, top_valid_state = self.extend_beam_for_train(beam, gold_tree)
            try:
                if not beam.has_element(top_valid_state.top()):
                    self.update_paramaters(beam.top(), -1)
                    self.update_paramaters(top_valid_state.top(), 1)
                    break
            except Exception:
                raise
        if step == len(sent)-1:
            top_beam = beam.top()
            predict_arcs = top_beam['arcs']
            if not compare_arcs(predict_arcs, gold_tree):
                self.update_paramaters(top_beam, -1)
                self.update_paramaters(top_valid_state.top(), 1)

    def extend_beam_for_train(self, beam, gold_tree):
        """
        
        :param beam: 
        :param gold_tree: 
        :return: 
        """
        new_beam = Beam(beam_size=self.model.beam_size)
        top_valid_state = Beam(beam_size=1)

        for state in beam:
            pending = state['pending']
            prev_features = state['features']
            prev_score = state['score']
            arcs = state['arcs']
            state_valid = state['valid']
            for attachment_point in xrange(len(pending)-1):
                # at this point you could create n new state
                local_features = features_extract(pending, arcs, attachment_point)
                # features extract funtion has not be built yet
                scores = self.model.get_scores(local_features)
                global_features = prev_features + local_features
                for cls_id, score in scores.iteritems():
                    action = get_action(attachment_point, cls_id, self.model.label_hash)
                    # check if action is valid
                    valid_action = False
                    if state_valid:
                        valid_action = check_valid_action(pending, arcs, action, gold_tree)
                    # apply action to pending
                    new_pending, new_arcs = apply_action(pending, arcs, action)
                    # create new state

                    if prev_score == float('-inf'):
                        current_score = score
                    else:
                        current_score = prev_score + score

                    new_state = get_state(new_pending, global_features, current_score, cls_id, new_arcs, valid_action)
                    # add new state to beam
                    new_beam.add(new_state)
                    if valid_action:
                        top_valid_state.add(new_state)
        return new_beam, top_valid_state

    def update_paramaters(self, state, value):
        features = state['features']
        cls = state['cls']
        self.model.update_paramaters(features, cls, value)

    def parse(self, sent):
        sent = [ROOT] + sent
        init_state = get_state(sent)
        beam = Beam(self.model.beam_size)
        beam.add(init_state)
        for i in xrange(len(sent) - 1):
            beam = self.extend_beam_for_parse(beam)
        final_state = beam.top()
        return final_state['arcs']

    def extend_beam_for_parse(self, beam):
        new_beam = Beam(beam_size=self.model.beam_size)
        for state in beam:
            pending = state['pending']
            prev_features = state['features']
            prev_score = state['score']
            arcs = state['arcs']
            for attachment_point in xrange(len(pending) - 1):
                # at this point you could create n new state
                local_features = features_extract(pending, arcs, attachment_point)
                # features extract funtion has not be built yet
                scores = self.model.get_scores(local_features)
                global_features = prev_features + local_features
                for cls_id, score in scores.iteritems():
                    action = get_action(attachment_point, cls_id, self.model.label_hash)
                    # apply action to pending
                    new_pending, new_arcs = apply_action(pending, arcs, action)
                    # create new state

                    if prev_score == float('-inf'):
                        current_score = score
                    else:
                        current_score = prev_score + score

                    new_state = get_state(new_pending, global_features, current_score, cls_id, new_arcs)
                    # add new state to beam
                    new_beam.add(new_state)
        return new_beam

