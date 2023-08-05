# -*- coding=utf-8 -*-
from enum import IntEnum


class EmbeddingType(IntEnum):
    empty = 0
    custom = 1
    word2vec = 2
    lm = 3
