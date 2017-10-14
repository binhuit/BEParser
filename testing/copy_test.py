from hash_table import HashTable
from utils import *
from constants import ROOT
import copy

sents = list(read_corpus('../data/toydata'))
pending = sents[1]


def get_dict(pending):
    pending = list(pending)
    return {
        'pending': pending
    }

a = get_dict(pending)
a = a['pending']
a = a[:-1]

print pending == a
