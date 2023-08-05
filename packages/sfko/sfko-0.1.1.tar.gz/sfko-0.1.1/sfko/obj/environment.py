from pipewrench import Message

from ..util.prng import prng


class Environment(Message):
    def __init__(self, *args, **kwargs):
        self.scenario = None
        self.buckets = []
        self.objects = []
        super().__init__(*args, **kwargs)
