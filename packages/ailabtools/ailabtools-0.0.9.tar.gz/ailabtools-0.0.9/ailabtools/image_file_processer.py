import magic
import hashlib
from subprocess import call
from PIL import Image
from send2trash import send2trash
from tqdm import tqdm
from .ailab_multiprocessing import pool_worker

def __hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def __change_namge(cur_name, new_name):
    call(['mv', cur_name, new_name])
    log = 'change name file {} to {}'.format(cur_name, new_name)
    return log
    
def __adj_extension(path):
    real_ex = magic.from_file(path, mime=True).split('/')[1]
    cur_ex = path.split('.')[-1]
    if cur_ex != real_ex:
        return __change_namge(path, '{}.{}'.format(path, real_ex))
    else:
        return ''

def adj_extension(paths, num_worker=None, verbose=True):
    """Adjust extension of files
    wrong_name => wrong_name.true_extension

    Parameters
    ----------
    paths : list
        list of path
    num_worker: int
        number of worker
    verbose: bool
        True: progress bar
        False: silent

    Returns
    -------
    logs: list of str
        list name files adjusted extension and new name
    """
    logs = pool_worker(__adj_extension, paths, num_worker, verbose)
    return [log for log in logs if log != '']
        
        
def __rm_unreadable(path):
    try:
        Image.open(path)
        return ''
    except:
        send2trash(path)
        log = 'remove file: {}'.format(path)
        return log
        
def rm_unreadable(paths, num_worker=None, verbose=True):
    """Remove file witch PIL.Image faile to read

    Parameters
    ----------
    paths : list
        list of path
    num_worker: int
        number of worker
    verbose: bool
        True: progress bar
        False: silent

    Returns
    -------
    logs: list of str
        list name files removed
    """
    logs = pool_worker(__rm_unreadable, paths, num_worker, verbose)
    return [log for log in logs if log != '']
        
def rm_duplicate(paths, num_worker=None, verbose=True):
    """Remove duplicate file

    Parameters
    ----------
    paths : list
        list of path
    num_worker: int
        number of worker
    verbose: bool
        True: progress bar
        False: silent

    Returns
    -------
    logs: list of str
        list name files removed
    """
    hashes = pool_worker(__hashfile, paths, num_worker, verbose)
        
    filted = {}
    remove_list = []
    logs = []
    for i in range(len(hashes)):
        if hashes[i] not in filted:
            filted[hashes[i]] = paths[i]
        else:
            send2trash(paths[i])
            logs.append('remove file: {} duplicate with: {}'.format(paths[i], filted[hashes[i]]))
    return logs