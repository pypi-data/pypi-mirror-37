from .transform import DeepOCRTransform
from PIL import Image
import numpy as np


class DefaultTransform(DeepOCRTransform):
    def __init__(self, config):
        super(DefaultTransform, self).__init__(config=config)

    def image_label_load(self, line):
        pair = line.strip().split("\t")
        if len(pair) != 2:
            return None, []

        image_path = pair[0]
        image = Image.open(image_path)
        image = image.resize(self.config.image_shape, Image.ANTIALIAS)
        image = np.array(image)
        text = [w for w in pair[1]]
        return image, text
