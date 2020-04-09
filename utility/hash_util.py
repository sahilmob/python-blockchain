
from hashlib import sha256
from json import dumps


def has_string_265(string):
    return sha256(string).hexdigest()


def hash_block(block):
    hasable_block = block.__dict__.copy()
    hasable_block["transactions"] = [
        tx.to_ordered_dict() for tx in hasable_block["transactions"]]
    return has_string_265(dumps(hasable_block, sort_keys=True).encode())
