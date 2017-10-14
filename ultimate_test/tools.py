from utils import *


def get_sample_sent():
    return list(read_corpus('test_data'))[0]


def compare_features(feat1, feat2):
    feat1 = set(feat1)
    feat2 = set(feat2)
    if len(feat1) != len(feat2):
        return False
    for feat in feat1:
        if not feat in feat2:
            print feat
            return False
    return True


def get_sample_label_hash():
    label_hash = HashTable()
    for label in get_label_conll('test_data'):
        label_hash.add(label)
    return label_hash
