from .transform import DeepLMTransform


class DefaultTransform(DeepLMTransform):
    def __init__(self, config):
        super(DefaultTransform, self).__init__(config=config, corpus_iter=None)

    def parse_text_line(self, line):
        pairs = [p for p in line.strip().split(" ") if p != ""]
        if len(pairs) > 0:
            words = ["<LM_START_LABEL>"]
            words.extend(pairs)
            words.append("<LM_END_LABEL>")
            return words
        else:
            return []

