from deps import DependenciesCollection
from engfeatures2 import FeaturesExtractor
from test_features import FeaturesExtractorTest
from hash_table import HashTable
import copy
LEFT = 0
RIGHT = 1


def read_corpus(filename):
    """
    Reading corpus file and yield sentence
    :param filename: corpus file name
    :return: list of tokens
    """
    dependency_corpus = open(filename)
    sent = []
    try:
        for line in dependency_corpus:
            line = line.strip().split()
            if line:
                sent.append(line_to_tok(line))
            elif sent:
                yield sent
                sent = []
    finally:
        if sent:
            yield sent
        dependency_corpus.close()


def line_to_tok(line):
    """
    convert a split line to token
    :param line: 
    :return: token
    """
    return {
        'id': int(line[0]),
        'form': line[1],
        'tag': line[4],
        'parent': int(line[6]),
        'prel': line[7]
    }


def get_tree(sent):
    # take sent as paramater
    # return list of tupples (child_id, parent_id, label)
    arcs = []
    for token in sent:
        if not token['tag'] == 'ROOT':
            arcs.append((token, sent[token['parent']], token['prel']))
    return arcs


def get_state(pending, features=[], score=float('-inf'), cls=None, arcs=[], valid = True):
    # pending is partial tree
    # features is global features of last action apply to pending
    # score is score of last action based on features
    # arcs is arcs which already built

    # make copy of list paramaters
    pending = list(pending)
    features = copy.copy(features)
    arcs = copy.copy(arcs)
    return {
        'pending': pending,
        'features': features,
        'score': score,
        'cls': cls,
        'arcs': arcs,
        'valid': valid
    }


def get_action(attachment_point, cls, label_hash):
    # what is it?
    # use to apply to
    action_id, label_id = divmod(cls, len(label_hash))
    label = label_hash.get_value(label_id)
    return {
        'attachment_point': attachment_point,
        'direction': action_id,
        'label': label
    }


def get_edge(pending, action):
    attachment_point = action['attachment_point']
    action_direction = action['direction']
    label = action['label']
    if action_direction == LEFT:
        head = pending[attachment_point]
        dependent = pending[attachment_point+1]
    else:
        head = pending[attachment_point+1]
        dependent = pending[attachment_point]
    return dependent, head, label


def apply_action(pending, arcs, action):
    pending = list(pending)
    arcs = list(arcs)
    # should this function copy paramaters and return new instance?
    dependent, head, label = get_edge(pending, action)
    arcs.append((dependent, head, label))
    pending.remove(dependent)
    return pending, arcs


def check_valid_action(pending, arcs, action, gold_tree):
    dependent, head, label = get_edge(pending, action)
    # check if edge is in gold
    edge_in_gold = (dependent, head, label) in gold_tree
    # list out all dependent's child in gold
    child_independent = True
    for g_dependent, g_head, g_label in gold_tree:
        if g_head == dependent:
            # check if (g_dependent, g_head, g_label) is in arcs
            if not (g_dependent, g_head, g_label) in arcs:
                child_independent = False
                break
    if not edge_in_gold or not child_independent:
        # if not edge_in_gold:
        #     print 'arc not in gold'
        # if not child_independent:
        #     print 'child not independent'
        return False
    return True


def get_label_conll(filename):
    dependency_corpus = open(filename)
    try:
        for line in dependency_corpus:
            line = line.strip().split()
            if line:
                yield line[7]
    finally:
        dependency_corpus.close()


def features_extract(pending, arcs, attachment_point):
    deps = from_arcs_to_deps(arcs)
    fext = FeaturesExtractor()
    return fext.extract(pending, deps, attachment_point)


def compare_arcs(predict_arcs, gold_arcs):
    if len(predict_arcs) == len(gold_arcs):
        for arcs in predict_arcs:
            if not arcs in gold_arcs:
                return False
    return True


def from_arcs_to_deps(arcs):
    deps = DependenciesCollection()
    for child, parent,_ in arcs:
        deps.add(parent, child)
    return deps


def load_hash_from_file(file_name):
    hash_table = HashTable()
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            hash_table.add(line)
    return hash_table


def split_path(path):
    # check if path is available
    part_of_path = path.split('/')
    if len(part_of_path) > 1:
        dir = '/'.join(part_of_path[:-1])
        file_name = part_of_path[-1]
    else:
        dir = ''
        file_name = part_of_path[0]
    return dir, file_name


