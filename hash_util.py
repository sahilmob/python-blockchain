
from hashlib import sha256
from json import dumps


def has_string_265(string):
    return sha256(string).hexdigest()


def hash_block(block):
    return has_string_265(dumps(block, sort_keys=True).encode())
