import os
import pandas as pd

from .fastx import read_count
from .utils import replace_suffix, touch, file_transaction, runcmd, file_exists


def fastq_join(r1, r2, out_file, p=2, m=240):
    """Join paired-end fastqs using fastq-join. Unjoined reads are discarded.

    Args:
        r1 (str): file path to R1 fastq
        r2 (str): file path to R2 fastq
        out_file (str): file path of joined reads fastq
        p (Optional[int]): n-percent maximum difference
        m (Optional[int]): n-minimum overlap

    Returns:
        str
    """
    joined_read_lengths = replace_suffix(out_file, "_lengths.txt")
    joined_read_stats = replace_suffix(out_file, "_stats.txt")
    # ~empty input file
    if os.path.exists(r1) and read_count(r1) == 0:
        touch(out_file)
        touch(joined_read_lengths)
        touch(joined_read_stats)
        return out_file

    # complete output file
    if file_exists(out_file):
        return out_file

    with file_transaction([out_file, joined_read_lengths, joined_read_stats]) as tx:
        dname = os.path.dirname(tx[0])
        tmp = tx[0] + "_%.fastq"
        # should also save the stdout of this call
        cmd = (
            "fastq-join -p {p} -m {m} -o {out} " "-r {lengths} {r1} {r2} > {stats}"
        ).format(
            p=p, m=m, out=tmp, lengths=tx[1], r1=r1, r2=r2, stats=tx[2]
        )
        runcmd(cmd, "Joining %s and %s" % (os.path.basename(r1), os.path.basename(r2)))
        os.rename(tx[0] + "_join.fastq", tx[0])
    return out_file


def fastq_join_stdout_to_dataframe(fnames):
    """`fastq-join` STDOUT:
    Total reads: int
    Total joined: int
    Average join len: float
    Stdev join len: float
    Version: string

    Args:
        fnames (list): list of file paths of fastq-join stdout

    Returns:
        pandas.DataFrame
    """
    d = {}
    for f in fnames:
        if os.path.getsize(f) < 50:
            continue

        sample = os.path.basename(f).partition("_")[0]
        sd = {}
        with open(f) as rfh:
            for line in rfh:
                toks = line.strip().split(":")
                sd[toks[0].strip()] = toks[1].strip()
        d[sample] = sd
    df = pd.DataFrame(d).T
    df[['Total joined', 'Total reads']] = df[['Total joined', 'Total reads']].astype(
        int
    )
    df[['Average join len', 'Stdev join len']] = df[
        ['Average join len', 'Stdev join len']
    ].astype(
        float
    )
    df.rename(columns={'Total reads': 'Read pairs'}, inplace=True)
    df['Total unjoined'] = df['Read pairs'] - df['Total joined']
    df = df[
        [
            "Read pairs",
            "Total joined",
            "Total unjoined",
            "Average join len",
            "Stdev join len",
            "Version",
        ]
    ]
    return df
