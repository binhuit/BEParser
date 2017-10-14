# -*- coding: utf-8 -*-

from be_parser_model import BEParsingModel, BETrainingModel
from be_parser import BEParser
from utils import *
from constants import ROOT
data_path = 'data/fold_test_1.conll'
test_data = list(read_corpus(data_path))

training_model = BETrainingModel('model/model',4)
training_model.setup_model(data_path)
parser = BEParser(training_model)
parser.train(data_path, 20)


testing_model = BEParsingModel('model/model')
parsing = BEParser(testing_model)

res = []
for sent in test_data:
    res.append(parser.parse(sent))
correct = 0
total = 0
for sent, arcs in zip(test_data, res):
    sent = [ROOT] + sent
    for token in sent[1:]:
        if (token, sent[token['parent']], token['prel']) in arcs:
            correct += 1
        total += 1

print total
print correct




