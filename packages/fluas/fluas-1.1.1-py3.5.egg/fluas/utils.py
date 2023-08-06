import functools
import logging
import os
import pandas as pd
import re
import shutil
import subprocess
import tempfile
import time
from contextlib import contextmanager
from io import TextIOWrapper
from sarge import capture_stdout, capture_stderr


logger = logging.getLogger(__name__)


@contextmanager
def file_transaction(*rollback_files):
    """Wrap file generation in a transaction, moving to output if finishes.

    Args:
        rollback_files (str or list): file path(s) of expected output files

    Yields:
        str or list: temporary file name(s)
    """
    safe_names, orig_names = _flatten_plus_safe(rollback_files)
    # remove any half-finished transactions
    remove_files(safe_names)
    try:
        if len(safe_names) == 1:
            yield safe_names[0]
        else:
            yield tuple(safe_names)
    # failure -- delete any temporary files
    except:
        remove_files(safe_names)
        remove_tmpdirs(safe_names)
        raise
    # worked -- move the temporary files to permanent location
    else:
        for safe, orig in zip(safe_names, orig_names):
            if os.path.exists(safe):
                shutil.move(safe, orig)
        remove_tmpdirs(safe_names)


def remove_tmpdirs(fnames):
    """Removes parent directories of files in the list.

    Args:
        fnames (list): file paths
    """
    for x in fnames:
        xdir = os.path.dirname(os.path.abspath(x))
        if xdir and os.path.exists(xdir):
            shutil.rmtree(xdir, ignore_errors=True)


def remove_files(fnames):
    """Remove files from a list.

    Args:
        fnames (list): file paths
    """
    for x in fnames:
        if x and os.path.exists(x):
            if os.path.isfile(x):
                os.remove(x)
            elif os.path.isdir(x):
                shutil.rmtree(x, ignore_errors=True)


def _flatten_plus_safe(rollback_files):
    """Flatten names of files and create temporary file names.

    Args:
        rollback_files (list): list of file paths or list of lists of file paths to be created in the process

    Returns:
        list, list: temporary file names, original file names
    """
    tx_files, orig_files = [], []
    for fnames in rollback_files:
        if isinstance(fnames, str):
            fnames = [fnames]
        for fname in fnames:
            basedir = safe_makedir(os.path.dirname(fname))
            tmpdir = safe_makedir(tempfile.mkdtemp(dir=basedir))
            tx_file = os.path.join(tmpdir, os.path.basename(fname))
            tx_files.append(tx_file)
            orig_files.append(fname)
    return tx_files, orig_files


def safe_makedir(dname):
    """Make a directory if it doesn't exist, handling concurrent race conditions.

    Args:
        dname (str): directory path

    Returns:
        str: the input dname
    """
    if not dname:
        return dname
    num_tries = 0
    max_tries = 5
    while not os.path.exists(dname):
        try:
            os.makedirs(dname)
        except OSError:
            if num_tries > max_tries:
                raise
            num_tries += 1
            time.sleep(2)
    return dname


def check_sample_id(s):
    """Standardize a sample ID.

    Replace '+' with 'pos'
    Replace ending '-' with 'neg'
    Replace remaining non-word characters with '-'
    Prepend 's' if sample ID starts with a digit

    Args:
        s (str): the sample id string

    Returns:
        str

    >>> check_sample_id("88-9")
    's88-9'
    >>> check_sample_id("88.9")
    's88-9'
    >>> check_sample_id("88.9+")
    's88-9-pos'
    >>> check_sample_id("test-")
    'test-neg'
    >>> check_sample_id("test_sample.3")
    'test-sample-3'
    """
    sampleid = str(s)
    if sampleid[0].isdigit():
        sampleid = "s%s" % sampleid
    # replace positive (+) with "pos"
    sampleid = sampleid.replace("+", "-pos")
    if sampleid.endswith("-"):
        sampleid = "%s%s" % (sampleid.rstrip("-"), "-neg")
    # replace non-word characters from sample name with dash
    # idea is to have sampleid_readindex.fastq.gz
    sampleid = re.sub(r'[\W_]', '-', sampleid).strip('-')
    return sampleid


def memoize(f):
    """Memoization decorator for functions taking one or more arguments.
    http://code.activestate.com/recipes/578231-probably-the-fastest-memoization-decorator-in-the-/
    """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)


def file_exists(fnames):
    """Check if a file or files exist and are non-empty.

    Args:
        fnames (str or list): file path as string or paths as list; if list, all must exist

    Returns:
        boolean
    """
    if isinstance(fnames, str):
        fnames = [fnames]
    for f in fnames:
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            return False
    return True


def strip_ext(fname):
    """Strips the extension, including ".gz" or ".bz2" from the file name.

    Args:
        fname (str): file path

    Returns:
        str
    """
    fname = os.path.abspath(fname)
    parent = os.path.dirname(fname)
    f, ext = os.path.splitext(os.path.basename(fname))
    if ext in [".gz", ".bz2"]:
        f, ext = os.path.splitext(f)
    return os.path.join(parent, f)


def stdout_iter(cmd):
    p = capture_stdout(cmd)
    for line in TextIOWrapper(p.stdout):
        yield line


def runcmd(cmd, description=None, iterable=False):
    if description:
        logger.info(description)
    logger.debug("$> %s" % cmd)
    if iterable:
        return stdout_iter(cmd)
    else:
        p = capture_stderr(cmd)
        # could check list of acceptable returncodes and ignore
        if p.returncode != 0:
            for line in TextIOWrapper(p.stderr):
                logger.error(line.strip())
            raise subprocess.CalledProcessError(p.returncode, cmd=cmd)
        else:
            return p


def transform_to(ext):
    """
    Decorator to create an output filename from an output filename with
    the specified extension. Changes the extension, in_file is transformed
    to a new type.
    Takes functions like this to decorate:
    f(in_file, out_dir=None, out_file=None) or,
    f(in_file=in_file, out_dir=None, out_file=None)

    Examples:
    @transform(".bam")
    f("the/input/path/file.sam") -> f("the/input/path/file.sam", out_file="the/input/path/file.bam")
    @transform(".bam")
    f("the/input/path/file.sam", out_dir="results") -> f("the/input/path/file.sam", out_file="results/file.bam")
    """

    def decor(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            out_file = kwargs.get("out_file", None)
            if not out_file:
                in_path = kwargs.get("in_file", args[0])
                out_dir = kwargs.get("out_dir", os.path.dirname(in_path))
                safe_makedir(out_dir)
                out_name = replace_suffix(os.path.basename(in_path), ext)
                out_file = os.path.join(out_dir, out_name)
            kwargs["out_file"] = out_file
            if not file_exists(out_file):
                out_file = f(*args, **kwargs)
            else:
                logger.info("%s exists; skipping." % out_file)
            return out_file
        return wrapper
    return decor


def filter_to(word):
    """
    Decorator to create an output filename from an input filename by
    adding a word onto the stem. in_file is filtered by the function
    and the results are written to out_file. You would want to use
    this over transform_to if you don't know the extension of the file
    going in. This also memoizes the output file.
    Takes functions like this to decorate:
    f(in_file, out_dir=None, out_file=None) or,
    f(in_file=in_file, out_dir=None, out_file=None)

    Examples:
    @filter_to(".foo")
    f("the/input/path/file.sam") -> f("the/input/path/file.sam", out_file="the/input/path/file.foo.bam")
    @filter_to(".foo")
    f("the/input/path/file.sam", out_dir="results") -> f("the/input/path/file.sam", out_file="results/file.foo.bam")
    """

    def decor(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            out_file = kwargs.get("out_file", None)
            if not out_file:
                in_path = kwargs.get("in_file", args[0])
                out_dir = kwargs.get("out_dir", os.path.dirname(in_path))
                safe_makedir(out_dir)
                out_name = append_stem(os.path.basename(in_path), word)
                out_file = os.path.join(out_dir, out_name)
            kwargs["out_file"] = out_file
            if not file_exists(out_file):
                out_file = f(*args, **kwargs)
            else:
                logger.info("%s exists; skipping." % out_file)
            return out_file
        return wrapper
    return decor


def memoize_outfile(ext=None, stem=None):
    """
    Memoization decorator.
    See docstring for transform_to and filter_to for details.
    """
    if ext:
        return transform_to(ext)
    if stem:
        return filter_to(stem)


def replace_suffix(to_transform, suffix):
    """
    replaces the suffix on a filename or list of filenames
    example: replace_suffix("/path/to/test.sam", ".bam") ->
    "/path/to/test.bam"
    """
    if is_sequence(to_transform):
        transformed = []
        for f in to_transform:
            (base, _) = os.path.splitext(f)
            transformed.append(base + suffix)
        return transformed
    elif is_string(to_transform):
        (base, _) = os.path.splitext(to_transform)
        return base + suffix
    else:
        raise ValueError("replace_suffix takes a single filename as a string or "
                         "a list of filenames to transform.")


def append_stem(to_transform, word):
    """
    renames a filename or list of filenames with 'word' appended to the stem
    of each one:
    example: append_stem("/path/to/test.sam", "_filtered") ->
    "/path/to/test_filtered.sam"
    """
    if is_sequence(to_transform):
        return [append_stem(f, word) for f in to_transform]
    elif is_string(to_transform):
        (base, ext) = splitext_plus(to_transform)
        return "".join([base, word, ext])
    else:
        raise ValueError("append_stem takes a single filename as a string or "
                         "a list of filenames to transform.")


def is_sequence(arg):
    """
    check if 'arg' is a sequence
    example: arg([]) -> True
    example: arg("lol") -> False
    """
    # this needs work for py3 compatibility
    # return (not hasattr(arg, "strip") and
    #         hasattr(arg, "__getitem__") or
    #         hasattr(arg, "__iter__"))
    if isinstance(arg, list) or isinstance(arg, tuple):
        return True
    else:
        return False


def is_string(arg):
    return isinstance(arg, str)


def df_from_csvs(csvs, **kwargs):
    """Create a single pandas.DataFrame from multiple input CSV files.

    Args:
        csvs (list): list of CSV file paths

    Returns:
        pandas.DataFrame
    """
    list_of_df = []
    for csv in csvs:
        individual = pd.read_csv(csv, **kwargs)
        list_of_df.append(individual)
    return pd.concat(list_of_df)


def df_from_dict(d, columns=None, index=None):
    """
    >>> import pandas as pd
    >>> d = {'sample1': 'ACC', 'sample2': 'AGG', 'sample3': 'TCA'}
    >>> df = dict_to_df(d)
    >>> df.columns
    Int64Index([0, 1], dtype='int64')
    >>> df.index
    Int64Index([0, 1, 2], dtype='int64')
    >>> df = dict_to_df(d, columns=['sample', 'barcode'])
    >>> df.columns
    Index(['sample', 'barcode'], dtype='object')
    >>> df = dict_to_df(d, columns=['sample', 'barcode'], index='barcode')
    >>> df.index
    Index(['AGG', 'TCA', 'ACC'], dtype='object', name='barcode')
    """
    if columns:
        if index and index in columns:
            return pd.DataFrame(list(d.items()), columns=columns).set_index(index)
        else:
            return pd.DataFrame(list(d.items()), columns=columns)
    return pd.DataFrame(list(d.items()))


def touch(fname, mode=0o666, dir_fd=None, **kwargs):
    """http://stackoverflow.com/questions/1158076/implement-touch-using-python"""
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname,
            dir_fd=None if os.supports_fd else dir_fd, **kwargs)
