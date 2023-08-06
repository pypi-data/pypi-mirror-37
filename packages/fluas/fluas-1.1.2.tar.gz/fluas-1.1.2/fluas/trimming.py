import os
from .utils import runcmd


def run_trimmomatic_pe(
    r1,
    r2,
    r1_paired,
    r1_orphaned,
    r2_paired,
    r2_orphaned,
    threads=1,
    phred=33,
    trimlog=None,
    illumina_clip=None,
    sliding_window=None,
    max_info=None,
    leading=None,
    trailing=None,
    crop=None,
    head_crop=None,
    min_len=None,
    avg_qual=None,
    to_phred33=False,
    to_phred64=False,
):
    """
    Args:
        r1 (str): file path to R1 fastq
        r2 (str): file path to R2 fastq
        r1_paired (str): output file path to paired R1 reads
        r1_orphaned (str): output file path to unpaired, orphaned R1 reads
        r2_paired (str): output file path to paired R2 reads
        r2_orphaned (str): output file path to unpaired, orphaned R2 reads
        threads (Optional[int]): processing threads
        phred (Optional[int]): phred score of input; 33 or 64
        trimlog (Optional[str]): output file path for trimming logs
        illumina_clip (Optional[list]): format args as a list of file path to fasta, seed
                                        mismatches, palindrome clip threshold, simple clip
                                        threshold, minimum adapter length, keep both reads
                                        (boolean). For example:
                                        [test.fasta, 1, 9, 7, 8, false]
        sliding_window (Optional[list]): list of window size and required quality, e.g [4,15]
        max_info (Optional[list]): list of target length and strictness, e.g. [240,0.9]
        leading (Optional[int]): minimum quality required to keep a base at beginning of read
        trailing (Optional[int]): minimum quality required to keep a base at end of read
        crop (Optional[int]): number of bases to trim from start of read
        head_crop (Optional[int]): number of bases to trim from the end of the read
        min_len (Optional[int]): minimum length of read to be kept
        to_phred33 (Optional[boolean]): (re)encodes the qualities to base 33
        to_phred64 (Optional[boolean]): (re)encodes the qualities to base 64

    Returns:
        tuple: r1 paired, r2 paired, r1 orphans, r2 orphans
    """
    assert phred == 33 or phred == 64
    if trimlog:
        trimlog = '-trimlog %s' % trimlog
    else:
        trimlog = ''
    trimmer = []
    if illumina_clip:
        assert os.path.exists(illumina_clip[0])
        trimmer.append('ILLUMINACLIP:%s' % ':'.join(illumina_clip))
    # docs unclear about MAXINFO and whether or not it's mutually exclusive
    if sliding_window:
        trimmer.append('SLIDINGWINDOW:%s' % ':'.join(sliding_window))
    if max_info:
        trimmer.append('MAXINFO:%s' % ':'.join(max_info))
    if leading:
        trimmer.append('LEADING:%d' % leading)
    if trailing:
        trimmer.append('TRAILING:%d' % trailing)
    if crop:
        trimmer.append('CROP:%d' % crop)
    if head_crop:
        trimmer.append('HEADCROP:%d' % head_crop)
    if min_len:
        trimmer.append('MINLEN:%d' % min_len)
    if avg_qual:
        trimmer.append('AVGQUAL:%d' % avg_qual)
    if to_phred33 and to_phred64:
        logger.warn('Ambiguous phred conversion. Skipping')
    elif to_phred33:
        trimmer.append('TOPHRED33')
    elif to_phred64:
        trimmer.append('TOPHRED64')
    cmd = (
        "java -jar {jar} PE -threads {threads} -phred{phred} {log} "
        "{r1} {r2} {r1p} {r2p} {r1o} {r2o} {trimmer}"
    ).format(
        jar="",
        log=trimlog,
        threads=threads,
        phred=phred,
        trimlog=trimlog,
        r1=r1,
        r2=r2,
        r1p=r1_paired,
        r2p=r2_paired,
        r1o=r1_orphaned,
        r2o=r2_orphaned,
        trimmer=" ".join(trimmer),
    )
    runcmd(cmd)
    return r1_paired, r2_paired, r1_orphaned, r2_orphaned
