"""
"""
import logging
import os.path
import pysam
import tempfile
from collections import Counter

from .utils import file_exists, runcmd


logger = logging.getLogger(__name__)


def fastx_reader(fastx_file):
    """Fasta or Fastq iterator

    Accepts file path of Fastq or Fasta and yields 3 fields regardless of file type (name, sequence, quality)

    Args:
        fastx_file (str): Fastq or Fasta file path

    Yields:
        tuple: (name, sequence, quality)

    >>> import os
    >>> import pysam
    >>> f = open("test.fastq", 'w')
    >>> f.write("@seq1\\nACTG\\n+\\nQQQQ")
    >>> f.close()
    >>> for name, seq, qual in fastx_reader(f.name):
            assert name == "seq1"
            assert seq == "ACTG"
            assert qual == "QQQQ"
    >>> os.remove("test.fastq")
    """
    fx = ""
    try:
        fx = pysam.FastqFile(fastx_file)
        for f in fx:
            yield f.name, f.sequence, f.quality
    finally:
        if fx:
            fx.close()


def count_per_sequence(fastx):
    """Grab the all sequences observed in a FASTQ or FASTA file.

    This method is intended to be used to quantify the Index read of MiSeq runs.

    Args:
        fastx (str): file path of FASTQ or FASTA file

    Returns:
        collections.Counter: {seq (str): count (int)}
    """
    logger.debug("Counting sequences in %s" % fastx)
    c = Counter()
    for name, seq, qual in fastx_reader(fastx):
        c.update([seq])
    return c


def read_count(fname):
    """Count the number of reads and write metadata .count file.

    Args:
        fname (str): fastq or fasta file path

    Returns:
        int
    """
    total = 0
    fq = True
    for name, seq, qual in fastx_reader(fname):
        if not qual:
            fq = False
        break

    if fname.endswith("gz"):
        count_file = fname.rsplit(".gz", 1)[0] + ".count"
        cat = "gzip -d -c"
    else:
        count_file = fname + ".count"
        cat = "cat"

    if file_exists(count_file):
        with open(count_file) as fh:
            for line in fh:
                total = int(line.strip())
                return total

    if not fq:
        cmd = '%s %s | grep -c "^>"' % (cat, fname)
    else:
        cmd = '%s %s | wc -l' % (cat, fname)

    for line in runcmd(cmd, iterable=True):
        total = int(line.rstrip())
        if fq:
            assert total % 4 == 0, "Multi-line or invalid FASTQ"
            total = int(total / 4)

    with open(count_file, 'w') as fh:
        print(total, file=fh)

    return total


def combine_fastas(fastas):
    tmp = tempfile.mktemp()
    with open(tmp, 'w') as fh:
        for fa in fastas:
            fa_name = os.path.basename(fa).split('.')[0]
            for name, seq, qual in fastx_reader(fa):
                print(">%s|%s" % (fa_name, name), seq, sep="\n", file=fh)
    return tmp
