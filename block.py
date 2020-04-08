from time import time


class Block:
    def __init__(self, index, previous_has, tranactions, proof, timestamp=None):
        self.index = index
        self.previous_has = previous_has
        self.tranactions = tranactions
        self.proof = proof
        self.timestamp = time() if timestamp is None else timestamp
