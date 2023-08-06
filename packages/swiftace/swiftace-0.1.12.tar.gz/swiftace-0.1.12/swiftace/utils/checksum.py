
import os
import hashlib
import re
from tqdm import tqdm_notebook as tqdm

HASH_FUNCS = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha256': hashlib.sha256,
    'sha512': hashlib.sha512
}


def get_hash(path, hashfunc='md5'):
    """Generic checksum utily function (works for both files and directories"""
    if not os.path.exists(path):
        raise FileNotFoundError(f'No such file or directory: {path}')
    if os.path.isdir(path):
        return dirhash(path, hashfunc, ignore_hidden=True)
    hash_func = HASH_FUNCS.get(hashfunc)
    if not hash_func:
        raise NotImplementedError('{} not implemented.'.format(hashfunc))
    return filehash(path, hash_func)


def dirhash(dirname, hashfunc='md5', excluded_files=None, ignore_hidden=False,
            followlinks=False, excluded_extensions=None):
    """Function for deterministically creating a single hash for a directory of files,
    taking into account only file contents and not filenames.
    """

    hash_func = HASH_FUNCS.get(hashfunc)
    if not hash_func:
        raise NotImplementedError('{} not implemented.'.format(hashfunc))

    if not excluded_files:
        excluded_files = []

    if not excluded_extensions:
        excluded_extensions = []

    if not os.path.isdir(dirname):
        raise TypeError('{} is not a directory.'.format(dirname))
    hashvalues = []

    filecounter = 0
    for root, dirs, files in os.walk(dirname, topdown=True, followlinks=followlinks):
        filecounter += 1

    for root, dirs, files in tqdm(os.walk(dirname, topdown=True, followlinks=followlinks), total=filecounter):
        if ignore_hidden:
            if not re.search(r'/\.', root):
                hashvalues.extend(
                    [filehash(os.path.join(root, f),
                              hash_func) for f in files if not
                     f.startswith('.') and not re.search(r'/\.', f)
                     and f not in excluded_files
                     and f.split('.')[-1:][0] not in excluded_extensions
                     ]
                )
        else:
            hashvalues.extend(
                [
                    filehash(os.path.join(root, f), hash_func)
                    for f in files
                    if f not in excluded_files
                    and f.split('.')[-1:][0] not in excluded_extensions
                ]
            )
    return _reduce_hash(hashvalues, hash_func)


def filehash(filepath, hashfunc):
    hasher = hashfunc()
    blocksize = 64 * 1024
    with open(filepath, 'rb') as fp:
        while True:
            data = fp.read(blocksize)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def _reduce_hash(hashlist, hashfunc):
    hasher = hashfunc()
    for hashvalue in sorted(hashlist):
        hasher.update(hashvalue.encode('utf-8'))
    return hasher.hexdigest()
