from .transform import SkipThoughtTransform
from common.utils import CorpusIterator


class DefaultSkipThoughtCorpusIterator(CorpusIterator):
    def __init__(self, files):
        super(DefaultSkipThoughtCorpusIterator, self).__init__(files)

    def analysis_line(self, line):
        pairs = line.strip().split("\t")
        if len(pairs) == 3:
            doc1 = [p for p in pairs[0]]
            doc2 = [p for p in pairs[1]]
            doc3 = [p for p in pairs[2]]
            return [doc1, doc2, doc3]
        return []


class DefaultSkipThoughtTransform(SkipThoughtTransform):
    def __init__(self, config):
        super(DefaultSkipThoughtTransform, self).__init__(config=config,
                                                          corpus_iter=DefaultSkipThoughtCorpusIterator(
                                                              [config.train_input_path, config.test_input_path]))

    def parse_text_line(self, line):
        pairs = line.strip().split("\t")
        if len(pairs) == 3:
            doc1 = [p for p in pairs[0]]

            doc2 = [p for p in pairs[1]]
            doc2.insert(0, "<LM_START_LABEL>")
            doc2.append("<LM_END_LABEL>")

            doc3 = [p for p in pairs[2]]
            doc3.insert(0, "<LM_START_LABEL>")
            doc3.append("<LM_END_LABEL>")

            return doc1, doc2, doc3

        return [], [], []

