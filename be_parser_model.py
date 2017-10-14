from hash_table import HashTable
from utils import *
from ml.ml import MultitronParameters, MulticlassModel
from ml_lib import MultitronParametersTest
import os


class BETrainingModel:

    def __init__(self, model_path='default_model', beam_size=1):
        self.model_path, self.model_name = split_path(model_path)
        self.beam_size = beam_size
        self.perceptron = None
        self.label_hash = HashTable()

    def save(self):
        labels_file = self.create_file_with_extension('label')
        self.label_hash.save_file(labels_file)
        with open(self.create_file_with_extension(),'w') as model_file:
            model_file.write(str(self.beam_size) + '\n')
            model_file.write(str(labels_file) + '\n')
            model_file.write(str(self.create_file_with_extension('weights')) + '\n')

    def setup_model(self, corpus_file):
        # index dependency label
        for label in get_label_conll(corpus_file):
            self.label_hash.add(label)
        n_class = len(self.label_hash) * 2
        self.perceptron = MultitronParameters(n_class)
        self.save()

    def save_weight_file(self,iter):
        weights_file_path = self.create_file_with_extension('weights.' + iter)
        self.perceptron.dump_fin(file(weights_file_path,'w'))

    def update_perceptron_counter(self):
        self.perceptron.tick()

    def create_file_with_extension(self, ext=''):
        return os.path.join(self.model_path, self.model_name + '.' + ext)

    def get_scores(self, features):
        return self.perceptron.get_scores(features)

    def update_paramaters(self, features, cls, value):
        self.perceptron.add(features, cls, value)

    @classmethod
    def load(cls,model_path):
        model_dir, model_file = split_path(model_path)
        with open(model_path,'r') as f:
            beam_size = int(f.readline().strip())
            label_hash_file = f.readline().strip()
            label_hash = load_hash_from_file(label_hash_file)
            weights_file_path = f.readline().strip()+".FINAL"
            perceptron = MulticlassModel(weights_file_path)
            return cls(model_path, beam_size, perceptron, label_hash)


class BEParsingModel:
    def __init__(self, model_path):
        with open(model_path,'r') as f:
            self.beam_size = int(f.readline().strip())
            label_hash_file = f.readline().strip()
            self.label_hash = load_hash_from_file(label_hash_file)
            weights_file_path = f.readline().strip()+".FINAL"
            self.perceptron = MulticlassModel(weights_file_path)

    def get_scores(self, features):
        return self.perceptron.get_scores(features)









