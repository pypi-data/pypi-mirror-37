from .transform import DeepMatchTransform
from common.utils import CorpusIterator


class DefaultCorpusIterator(CorpusIterator):
    def __init__(self, files):
        super(DefaultCorpusIterator, self).__init__(files)

    def analysis_line(self, line):
        pairs = line.strip().split("\t")
        if len(pairs) == 3:
            doc1 = pairs[0].split(" ")
            doc2 = pairs[1].split(" ")
            return [doc1, doc2]
        return []


class DefaultTransform(DeepMatchTransform):
    def __init__(self, config):
        super(DefaultTransform, self).__init__(config=config,
                                               corpus_iter=DefaultCorpusIterator([config.train_input_path,
                                                                                  config.test_input_path]))

    def parse_line(self, line):
        pairs = line.strip().split("\t")
        if len(pairs) == 3:
            doc1 = pairs[0].split(" ")
            doc2 = pairs[1].split(" ")
            label = float(pairs[2])
            return doc1, doc2, label
        return [], [], 0.

