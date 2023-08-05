
class BaseModel(object):
    def __init__(self, session, transformer, config):
        self.session = session
        self.transformer = transformer
        self.config = config
        self.loss = None

        self.scope = ""
        if len(self.config.gpu_list) > 0:
            self.scope = "reuse_model/"


