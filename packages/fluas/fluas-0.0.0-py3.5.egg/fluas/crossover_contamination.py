import logging
import os
import pandas as pd
import sys
from collections import Counter
from contextlib import contextmanager
from functools import partial
from itertools import repeat
from multiprocessing import Pool

from .fastx import fastx_reader, combine_fastas
from .utils import file_exists, runcmd, strip_ext


logger = logging.getLogger(__name__)


@contextmanager
def bwa_index(reference, options=None):
    """Builds an index using `bwa index`.

    Args:
        reference (str): file path of reference fasta
        options (Optional[str]): options passed to bwa index, eg. "-a is"

    Yields:
        str: file path of reference as it's used as the prefix in `bwa index`
    """
    ref = os.path.abspath(reference)
    idx_files = [ref + x for x in ['.amb', '.ann', '.bwt', '.pac', '.sa']]
    if not file_exists(idx_files):
        logger.debug("Creating BWA index for %s" % ref)
        cmd = "bwa index {options}{reference}".format(options=options + " " if options else "", reference=reference)
        runcmd(cmd)
    yield reference


def bwa_to_small_reference(fastq, references, outfile, threads=8, overlap=0.95, identity=0.95):
    """Align fastq to each reference saving read names that map and counts to which reference
    a read maps to.

    Args:
        fastq (str): file path of fastq to be checked for contamination
        references (list): list of reference fasta file paths
        outfile (str): file path for readname:referencename hits to be written
        threads (Optional[int]): number of threads to utilize during mapping
        overlap (Optional[float]): fraction of overlap when mapping sequence to reference
        identity (Optional[float]): fraction of matching bases in passing alignment

    Returns:
        (set, Counter): (read names, reference_name:count)
    """
    d_identity = 1.0 - identity
    # may be useful to later track hits by reference
    # hits = set()
    reference_hits = Counter()
    # want to limit mappings, but could have implications later if used with shorter reads
    seedlen = 100
    tmp_fasta = combine_fastas(references)

    # ref_name = os.path.basename(strip_ext(ref))
    # create an index for each reference
    with bwa_index(tmp_fasta, "-a is") as bwaidx, open(outfile, 'w') as hitsfile:
        cmd = ("bwa mem -t {threads} -k {seedlen} -a {index} {fastq} 2> {devnull} "
               "| samtools view -F 4 - 2> {devnull}").format(threads=threads, seedlen=seedlen,
                                                             index=bwaidx, fastq=fastq,
                                                             devnull=os.devnull)
        # align using bwa mem; filter unmapped reads (-F4)
        for aln in runcmd(cmd, iterable=True):
            try:
                # grab the first digit of edit distance
                observed_mismatches = int(aln.split("NM:i:")[1][0])
                toks = aln.rstrip("\r\n").split("\t")
                ref_name = toks[2].partition("|")[0]
                # verify length of match of bwa can/will align local segments
                matching = float(toks[5].split("M")[0])
                seqlen = len(toks[9])
            except ValueError:
                # one of the splits didn't work above
                continue
            if observed_mismatches / seqlen <= d_identity and matching / seqlen >= overlap:
                name = toks[0]
                # save the read name of the contaminant
                print(name, ref_name, sep=",", file=hitsfile)
                # count this contaminant against this reference
                reference_hits.update([ref_name])

    return reference_hits


def reference_contamination_check(fastq, references, outfiles, threads=8, overlap=0.95, identity=0.95):
    """Align reads against all references, flagging contaminant reads, and generating a stats
    table of:
        ReadsFile,Reference1,Reference2
        read1.fastq,0,10

    Args:
        fastq (str): file path of fastq to be checked for contamination
        references (list): list of reference fasta file paths
        outfiles (list): path to contaminant reads text file and contaminant count table csv
        threads (Optional[int]): number of threads to utilize during mapping
        overlap (Optional[float]): fraction of overlap when mapping sequence to reference
        identity (Optional[float]): fraction of matching bases in passing alignment

    Returns:
        list: outfiles
    """
    assert len(outfiles) > 1, "You need to specify paths for both output files."
    if file_exists(outfiles):
        return outfiles
    fastq = os.path.abspath(fastq)
    logger.debug("Running reference contamination check on %s" % fastq)
    reference_hits = bwa_to_small_reference(fastq, references, outfiles[0], threads, overlap, identity)
    # read IDs that we could maybe remove later
    # with open(outfiles[0], 'w') as fh:
    #     print(*hits, sep="\n", file=fh)
    # sample names are the first section of the file name up to first underscore
    sample_name = os.path.basename(fastq).partition("_")[0]
    df = pd.DataFrame(reference_hits, index=[sample_name])
    df.to_csv(outfiles[1], index_label="Sample")
    return outfiles


def df_from_csvs(csvs, **kwargs):
    """Create a single pandas.DataFrame from multiple input CSV files.

    Args:
        csvs (list): list of CSV file paths

    Returns:
        pandas.DataFrame
    """
    # TODO: figure out a better place for this method
    list_of_df = []
    for csv in csvs:
        individual = pd.read_csv(csv, **kwargs)
        list_of_df.append(individual)
    return pd.concat(list_of_df)


def crossover_contamination_check(fastqs, references, outfile, threads=8, overlap=0.95, identity=0.99):
    """Run cross-over contamination check against a set of FASTQs.

    Args:
        fastqs (list): list of fastq file paths
        references (list): list of reference fasta file paths
        outfile (str): output statistics table with contamination stats
        threads (Optional[int]): number of threads to use during alignment
        overlap (Optional[float]): fraction of overlap required when mapping sequence to reference
        identity (Optional[float]): fraction of matching bases in passing alignment

    Returns:
        str: path of output file
    """
    outfile = os.path.abspath(outfile)
    if file_exists(outfile):
        return outfile
    logger.info("Starting cross-over contamination check")
    if isinstance(fastqs, str):
        fastqs = [fastqs]

    # written alongside fastq being analyzed
    ref_outfiles = []
    for fq in fastqs:
        prefix = fq.rpartition("_")[0]
        fq_reads = prefix + "_contaminant_reads.txt"
        fq_counts = prefix + "_contaminant_table.csv"
        ref_outfiles.append((fq_reads, fq_counts))

    pool_size = int(os.cpu_count() / threads) or 1
    results = []
    with Pool(pool_size) as p:
        results = p.starmap(reference_contamination_check, zip(fastqs,
                                                               repeat(references),
                                                               ref_outfiles,
                                                               repeat(threads),
                                                               repeat(overlap),
                                                               repeat(identity)))
    stat_tables = [j for i, j in results]
    df = df_from_csvs(stat_tables, header=0, index_col=0)
    df.to_csv(outfile, na_rep=0)
    logger.info("Cross-over contamination check is complete")
    return outfile
