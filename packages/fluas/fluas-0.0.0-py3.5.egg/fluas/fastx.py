import logging
import os.path
import pandas as pd
import pysam
import tempfile
from collections import Counter
from itertools import repeat
from multiprocessing import Pool

from .utils import file_exists, file_transaction, replace_suffix, runcmd, strip_ext
from .plots import read_joining_summary_plot


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
    >>> f.write("@seq1\nACTG\n+\nQQQQ")
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
            if f.quality:
                yield f.name.decode(), f.sequence.decode(), f.quality.decode()
            else:
                yield f.name.decode(), f.sequence.decode(), None
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
    else:
        count_file = fname + ".count"

    if file_exists(count_file):
        with open(count_file) as fh:
            for line in fh:
                total = int(line.strip())
                return total

    if not fq:
        cmd = 'gzip -d -c %s | grep -c "^>"' % fname
    else:
        cmd = 'cat %s | wc -l' % fname

    for line in runcmd(cmd, iterable=True):
        total = int(line.rstrip())
        if fq:
            assert total % 4 == 0, "Multi-line or invalid FASTQ"
            total = int(total / 4)

    with open(count_file, 'w') as fh:
        print(total, file=fh)

    return total


def join_reads(r1, r2, outfile, p=2, m=240):
    """Join paired-end fastqs using fastq-join. Unjoined reads are discarded.

    Args:
        r1 (str): file path to R1 fastq
        r2 (str): file path to R2 fastq
        outfile (str): file path of joined reads fastq
        p (Optional[int]): n-percent maximum difference
        m (Optional[int]): n-minimum overlap

    Returns:
        str
    """
    if file_exists(outfile):
        return outfile

    joined_read_lengths = replace_suffix(outfile, "_lengths.txt")
    joined_read_stats = replace_suffix(outfile, "_stats.txt")

    with file_transaction([outfile, joined_read_lengths, joined_read_stats]) as tx:
        dname = os.path.dirname(tx[0])
        tmp = tx[0] + "_%.fastq"
        # should also save the stdout of this call
        cmd = ("fastq-join -p {p} -m {m} -o {out} "
               "-r {lengths} {r1} {r2} > {stats}").format(p=p, m=m, out=tmp, lengths=tx[1],
                                                          r1=r1, r2=r2, stats=tx[2])
        runcmd(cmd, "Joining %s and %s" % (os.path.basename(r1), os.path.basename(r2)))
        os.rename(tx[0] + "_join.fastq", tx[0])
    return outfile


def fastq_join_stdout_to_dataframe(fnames):
    """
    Total reads: 31102
    Total joined: 17766
    Average join len: 249.00
    Stdev join len: 0.09
    Version: 1.01.759
    """
    d = {}
    for f in fnames:
        sample = os.path.basename(f).partition("_")[0]
        sd = {}
        with open(f) as rfh:
            for line in rfh:
                toks = line.strip().split(":")
                sd[toks[0].strip()] = toks[1].strip()
        d[sample] = sd
    df = pd.DataFrame(d).T
    df = df.convert_objects(convert_numeric=True)
    df.rename(columns={'Total reads':'Read pairs'}, inplace=True)
    df['Total unjoined'] = df['Read pairs'] - df['Total joined']
    df = df[["Read pairs", "Total joined", "Total unjoined",
             "Average join len", "Stdev join len", "Version"]]
    return df


def batch_join_reads(r1s, r2s, outfiles, join_stats=None, p=2, m=240, threads=8):
    """Run list of fastqs through join_reads.

    Args:
        r1s (list): list of file paths for R1 FASTQs
        r2s (list): list of file paths for R2 FASTQs
        outfiles (list): list of output files
        join_stats (Optional[str]): file path to join stats table
        p (Optional[int]): n-percent maximum difference
        m (Optional[int]): n-minimum overlap
        threads (Optional[int]): simultaneous join commands

    Returns:
        list: file paths of joined reads
    """
    assert len(r1s) == len(r2s) == len(outfiles)
    results = []
    #TODO pool creation should be handled by a utils function
    with Pool(threads) as pool:
        results = pool.starmap(join_reads, zip(r1s, r2s, outfiles, repeat(p), repeat(m)))
    if join_stats:
        stat_files = [replace_suffix(f, "_stats.txt") for f in outfiles]
        df = fastq_join_stdout_to_dataframe(stat_files)
        plot_file = replace_suffix(join_stats, ".pdf")
        read_joining_summary_plot(df['Total unjoined'], df['Total joined'], plot_file)
        df.to_csv(join_stats, index_label="Sample")
    return results


def combine_fastas(fastas):
    tmp = tempfile.mktemp()
    with open(tmp, 'w') as fh:
        for fa in fastas:
            fa_name = os.path.basename(fa).split('.')[0]
            for name, seq, qual in fastx_reader(fa):
                print(">%s|%s" % (fa_name, name), seq, sep="\n", file=fh)
    return tmp
