import hashlib
from functools import partial


def textmd5sum(text):
    md5sum = hashlib.md5()
    hash_seed = text.encode('utf-8')
    md5sum.update(hash_seed)
    md5string = str(md5sum.hexdigest())
    return md5string


def filemd5sum(file_path):
    with open(file_path, 'rb') as file_handler:
        md5sum = hashlib.md5()
        for part in iter(partial(file_handler.read, 128), b''):
            md5sum.update(part)
    return md5sum.hexdigest()