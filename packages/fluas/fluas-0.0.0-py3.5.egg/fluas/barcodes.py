import errno
import fileinput
import logging
import os
import pandas as pd
import re
import sys
from collections import OrderedDict

from .fastx import count_per_sequence
from .plots import lorenz_curve
from .stats import gini
from .utils import file_exists, file_transaction, memoize, runcmd, safe_makedir, strip_ext, memoize_outfile


logger = logging.getLogger(__name__)


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
    # replace positive (+) with "pos"
    sampleid = s.replace("+", "-pos")
    if sampleid.endswith("-"):
        sampleid = "%s%s" % (sampleid.rstrip("-"), "-neg")
    # replace non-word characters from sample name with dash
    # idea is to have sampleid_readindex.fastq.gz
    sampleid = re.sub(r'[\W_]', '-', sampleid).strip('-')
    if sampleid[0].isdigit():
        sampleid = "s%s" % sampleid
    return sampleid


@memoize_outfile(ext="_validated.tsv")
def preprocess_barcodes(tsv, out_file=None):
    """Reformats barcodes using `check_sample_id` and verifies uniqueness. A backup of the input
    file is created in the process.

    Args:
        tsv (str): TSV file path with SampleID<tab stop>BarcodeSequence
        out_file (Optional[str]): file path to TSV with valid sample names

    Returns:
        str: path to validated barcode TSV
    """
    if file_exists(out_file):
        return out_file
    # read in the barcodes
    barcodes = OrderedDict()
    with open(tsv, 'rU') as rfh:
        for line in rfh:
            toks = line.rstrip("\r\n").split("\t")
            sampleid = check_sample_id(toks[0])
            if not sampleid == toks[0]:
                logger.debug("renaming %s to %s" % (toks[0], sampleid))
            sequence = toks[1]

            if not sequence:
                logger.error("no barcode found for %s" % toks[0])
                raise ValueError("could not find sequence for sample %s" % toks[0])
            # handling duplicate barcodes
            if sampleid in barcodes:
                # also has a duplicate barcode!
                if sequence == barcodes[sampleid]:
                    logger.warning("%s entered more than once in barcodes list" % sampleid)
                    continue
                else:
                    previous_sequence = barcodes.pop(sampleid)
                    # update previous entry to include its barcode
                    barcodes["%s-%s" % (sampleid, previous_sequence)] = previous_sequence
                    # handle current entry
                    barcodes["%s-%s" % (sampleid, sequence)] = sequence
                    logger.warning("Appending barcode sequence to duplicate sample %s" % sampleid)
            else:
                barcodes[sampleid] = sequence

    with file_transaction(out_file) as tx:
        with open(tx, 'w') as wfh:
            for name, seq in barcodes.items():
                print(name, seq, sep="\t", file=wfh)
    return out_file


def samples_from_barcodes(tsv):
    """Just grab the sample:barcode from the barcodes TSV.

    Args:
        tsv (str): file path to barcodes TSV

    Returns:
        dict

    Raises:
        AssertionError: sample duplicates are not permitted
    """
    sample_names = {}
    with open(tsv, 'rU') as fh:
        for line in fh:
            toks = line.strip().split("\t")
            assert toks[0] not in sample_names
            sample_names[toks[0]] = toks[1]
    return sample_names


@memoize
def expected_out_files_from_barcodes(tsv, out_dir):
    """Given the barcodes TSV and output directory for fastq-multx, return the list of output
    files we're expecting.

    Args:
        tsv (str): TSV file path with SampleID<tab stop>BarcodeSequence
        out_dir (str): path to output directory of fastq-multx

    Returns:
        list: [(r1 file path, r2 file path)]
    """
    # sample name\tbarcode
    # expected demux format is out_dir/%_R1.fastq, out_dir/%_R2.fastq
    out_files = []
    out_dir = os.path.abspath(out_dir)
    with open(tsv, 'rU') as fh:
        for line in fh:
            toks = line.strip().split("\t")
            sample_name = toks[0]
            # barcode = toks[1]
            # owner = toks[2]
            r1 = os.path.join(out_dir, "%s_R1.fastq" % sample_name)
            r2 = os.path.join(out_dir, "%s_R2.fastq" % sample_name)
            out_files.append((r1, r2))
    return out_files


def get_master_barcodes(tsv):
    """Read in TSV of master barcodes

    Args:
        tsv (str): file path to master barcode list

    Returns:
        pandas.DataFrame: indexed by barcode sequence

    Note:
        Header of the TSV must be present and match:
            Plate Name(s), Plate Number, Well Position, Sequence Name, Sequence, Barcode

    Raises:
        ValueError: if duplicate barcode sequences exist
    """
    df = pd.read_table(tsv, sep="\t", header=0)
    try:
        df.set_index("Barcode", inplace=True, verify_integrity=True)
    except ValueError:
        logger.error("The master barcode list has duplicate barcodes", exc_info=True)
        raise
    return df


def run_fastq_multx(tsv, r1, r2, i1, out_dir, stats_file=None, m=0, d=2, q=0):
    """Formats command and makes system call to fastq-multx. Output fastqs are written into
    same folder as R1.

    Args:
        tsv (str): file path of barcodes TSV with name<tab>barcode
        i1 (str): file path of Index Fastq
        r1 (str): file path of Read 1
        r2 (str): file path of Read 2
        out_dir (str): directory path for demultiplexed reads
        out_file (Optional[str]): file path to output stats TSV
        m (Optional[int]): allowable mismatches in barcode as long as they are unique
        d (Optional[int]): require a minimum distance of N between the best and the next best
        q (Optional[int]): require a minimum phred quality of N to accept a barcode base

    Returns:
        list: [(r1 file path, r2 file path)]
    """
    # we expect some of these may be 0
    out_dir = safe_makedir(out_dir)
    expected_fastqs = expected_out_files_from_barcodes(tsv, out_dir)

    rerun = False
    for (fq1, fq2) in expected_fastqs:
        if not os.path.exists(fq1) or not os.path.exists(fq2):
            rerun = True
    if not rerun:
        return expected_fastqs

    if not stats_file:
        stats_file = os.devnull
    # demultiplexed using pattern: %_R[1,2].fastq
    # file transaction doesn't work on this due to how file names are written
    cmd = ("fastq-multx -B {tsv} {i1} {r1} {r2} "
           "-o n/a -o {dir}/%_R1.fastq -o {dir}/%_R2.fastq "
           "-m {m} -d {d} -q {q} > {stats}").format(tsv=tsv, i1=i1, r1=r1, r2=r2,
                                                    dir=out_dir, m=m, d=d, q=q,
                                                    stats=stats_file)
    runcmd(cmd, description="demultiplexing")
    unmatched_r1 = os.path.join(out_dir, "unmatched_R1.fastq")
    unmatched_r2 = os.path.join(out_dir, "unmatched_R2.fastq")
    if os.path.exists(unmatched_r1):
        os.remove(unmatched_r1)
    if os.path.exists(unmatched_r2):
        os.remove(unmatched_r2)
    # validate that we have the right files here
    for (o1, o2) in expected_fastqs:
        if not os.path.exists(o1):
            logger.error("Expected file %s was not found!" % o1)
        if not os.path.exists(o2):
            logger.error("Expected file %s was not found!" % o2)
    return expected_fastqs


def counts_from_demultiplex_stats(tsv):
    """Parse the TSV into a Series of count data after removing the counts for unmatched and total.

    Expected input header looks like:
        Id<tab>Count<tab>File(s)

    Args:
        tsv (str): file path to fastq-multx STDOUT

    Returns:
        pd.Series
    """
    # plot read distribution across samples
    df = pd.read_table(tsv, index_col=False, usecols=[0,1], header=0)
    df = df.set_index(['Id'])
    df = df.drop(df.loc[['unmatched', 'total']].index)
    return df['Count'].values


def gini_from_demultiplex_stats(tsv):
    """Calculate the Gini Coefficient from fastq-multx read count data.

    Args:
        tsv (str): path to fastq-multx STDOUT capture

    Returns:
        float
    """
    counts = counts_from_demultiplex_stats(tsv)
    try:
        g = gini(counts)
    except AssertionError:
        logger.error("No reads were matched to their respective barcode.")
        raise
    return g


@memoize_outfile(ext=".pdf")
def lorenz_curve_from_demultiplex_stats(tsv, out_file=None):
    """Parse fastq-multx STDOUT and plot distribution.

    Args:
        tsv (str): path to fastq-multx STDOUT capture
        out_file (Optional[str]): path to output PDF

    Returns:
        str: output file path
    """
    counts = counts_from_demultiplex_stats(tsv)
    out_file = lorenz_curve(counts, out_file)
    return out_file


def demultiplex_fastq(tsv, r1, i1=None, r2=None, out_dir=None, stats_file=None, dist_plot=None, m=0, d=2, q=0):
    """Run fastq-multx across an Undetermined paired-end fastq group.

    Args:
        tsv (str): file path of barcodes TSV with name<tab>barcode
        r1 (str): file path of Read 1
        i1 (Optional[str]): file path of Index Fastq if not in same dir as `r1`
        r2 (Optional[str]): file path of Read 2 if not in same dir as `r1`
        out_dir (Optional[str]): directory path for demultiplexed reads; defaults to r1 dir
        stats_file (Optional[str]): file path to stats CSV
        dist_plot (Optional[str]): file path to inequality plot (PDF)
        m (Optional[int]): allowable mismatches in barcode as long as they are unique
        d (Optional[int]): require a minimum distance of N between the best and the next best
        q (Optional[int]): require a minimum phred quality of N to accept a barcode base

    Returns:
        list: [(r1 path, r2 path), ...]
    """
    # get the file names
    r1 = os.path.abspath(r1)
    if not r2 and not i1:
        if "_R1" not in r1:
            logging.critical("_R1 ('_R2' and '_I1') must exist within the read name(s).")
            raise OSError(errno.ENOENT, "Invalid naming convention", r1)
    if not r2:
        r2 = r1.replace("_R1", "_R2")
    if not file_exists(r2):
        logging.critical("R2 was not found. It should be located in the same directory as R1.")
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), r2)
    if not i1:
        i1 = r1.replace("_R1", "_I1")
    if not file_exists(i1):
        logging.critical("I1 was not found. It should be located in the same directory as R1.")
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), i1)
    if not out_dir:
        out_dir = os.path.dirname(os.path.abspath(r1))

    # run demultiplexing
    fastqs = run_fastq_multx(tsv, r1, r2, i1, out_dir, stats_file=stats_file, m=m, d=d, q=q)

    # process stats file into plot
    if stats_file and file_exists(stats_file):
        if dist_plot:
            lorenz_curve_from_demultiplex_stats(stats_file, out_file=dist_plot)
        else:
            lorenz_curve_from_demultiplex_stats(stats_file)
    return fastqs


def dict_to_df(d, columns=None, index=None):
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


def barcode_stats(run_id, fastq, run_barcodes, count_table=None, stat_table=None, all_barcodes=None):
    """Wrapper method for command line entry point `carry-over`.

    Builds a stats table of barcode sequences along with the master and run barcodes and then
    generates a mapping table to give insights into demultiplexing quality and library diversity.

    Args:
        run_id (str): unique ID that identifies this sequencing run
        fastq (str): file path to multiplexed Index Fastq
        run_barcodes (str): file path to barcodes used for this run (see Note)
        count_table (Optional[str]): file path to all counts
        stat_table (Optional[str]): file path to stats on the counts
        all_barcodes (Optional[str]): file path to master barcode list (see Note)

    Returns:
        tuple: (count_table file path, stat_table file path)

    Note:
        Columns in run_barcodes TSV are sampleID and sequence.
        Header exists with titles in `all_barcodes` TSV are:
            Plate Name(s), Plate Number, Well Position, Sequence Name, Sequence, Barcode
    """
    if count_table and stat_table and file_exists([count_table, stat_table]):
        return count_table, stat_table

    # sample:barcode
    samples = samples_from_barcodes(run_barcodes)
    samples = dict_to_df(samples, columns=['Sample', 'Barcode'], index='Barcode')
    # barcode:count
    counts_by_seq = count_per_sequence(fastq)
    counts = pd.Series(counts_by_seq, name="Count")
    # index on barcode
    counts.index.name = "Barcode"

    # carry-over contamination checking
    if all_barcodes:
        # read in TSV to DataFrame
        master = get_master_barcodes(all_barcodes)
        df = master.join(samples, how="outer")
        df = df.join(counts, how="outer")
    else:
        df = counts.join(samples, how="outer")

    # add the run metadata to the table
    df['RunID'] = run_id
    df.sort(columns='Count', ascending=False, inplace=True, kind="mergesort")
    df.to_csv(count_table if count_table else sys.stdout, index_label="Barcode", float_format='%.0f')

    if stat_table:
        total = df.Count.sum()
        on_target_df = df.ix[:, ["Sample", "Count"]].dropna()
        on_target = on_target_df.Count.sum()
        f_on_target = on_target / total

        if all_barcodes:
            off_target = df.ix[df.Sample.isnull()].dropna(subset=["Plate Number"]).Count.sum()
            f_off_target = off_target / total
            unmatched = (total - off_target - on_target) / total
        else:
            f_off_target = "NA"
            unmatched = (total - on_target) / total

        try:
            gcoef = gini(on_target_df.Count.values)
        except AssertionError:
            logger.error("No reads were matched to their respective barcode.")
            gcoef = 1.0

        with open(stat_table, 'w') as fh:
            print("RunID", "OnTarget", "OffTarget", "Unmatched", "GiniCoefficient", sep=",", file=fh)
            print(run_id, f_on_target, f_off_target, unmatched, gcoef, sep=",", file=fh)

    return count_table, stat_table
