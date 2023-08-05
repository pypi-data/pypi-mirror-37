import threading


class PipelineLoader:

    _default_loader = None
    _default_loader_lock = threading.Lock()

    @classmethod
    def default_loader(cls):
        with cls._default_loader_lock:
            if cls._default_loader is None:
                cls._default_loader = cls()
            return cls._default_loader

    def __init__(self):
        self._pipelines = {}

    def add_pipeline(self, name, pipeline):
        self._pipelines[name] = pipeline

    def get_pipeline(self, name):
        p = self._pipelines.get(name)
        if not p:
            from .pipeline import Pipeline
            p = Pipeline(name=name, loader=self)
            self.add_pipeline(name, p)
        return p

    def remove_pipeline(self, name):
        if name in self._pipelines:
            del self._pipelines[name]

