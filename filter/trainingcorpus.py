from filter.utils import read_classification_from_file
from filter.corpus import Corpus
from os.path import join

class TrainingCorpus(Corpus):

    def __init__(self, corpus_dir):
        super().__init__(corpus_dir)

    def get_class(self, email):
        tags = read_classification_from_file(join(self.corpus_dir, "!truth.txt"))
        for tag in tags.items():
            if tag[0] == email:
                return tag[1]
