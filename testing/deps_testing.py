from utils import *
from constants import ROOT

sents = list(read_corpus('../data/toydata'))
sent = [ROOT]+sents[1]
arcs = []
print features_extract(sent, arcs, 1)
