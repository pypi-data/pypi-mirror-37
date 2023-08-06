"""
Next-gen data processing commands and workflows.
"""
import argparse
import logging
import os.path
import sys

from fluas import (__version__, batch_join_reads, barcode_stats,
                   crossover_contamination_check, demultiplex_fastq,
                   join_reads, preprocess_barcodes, read_count, safe_makedir,
                   reference_contamination_check, file_exists)


def pfile_exists(parser, arg):
    """Argparse file exists verification."""
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    return os.path.abspath(arg)


def run_all(run_id, barcodes, r1, bc_mismatches=0, bc_distance=2, bc_quality=0, join_overlap=240,
            join_difference=2, master_tsv=None, references=None, overlap=0.95, identity=0.99,
            threads=8, out_dir=None):
    """Runs the Demultiplex and QC protocol for the MiSeq.

    Args:
        run_id (str): unique ID that identifies this sequencing run
        barcodes (str): file path to barcodes TSV of NAME:BARCODE
        r1 (str): path to R1 fastq -- R2 and I1 must be in same directory
        bc_mismatches (Optional[int]): allowable mismatches in barcode as long as they are unique
        bc_distance (Optional[int]): require a minimum distance of N between the best and the next best
        bc_quality (Optional[int]): require a minimum phred quality of N to accept a barcode base
        master_tsv (Optional[int]): master barcode list as TSV containing header in the
                                    order of: Plate Name(s)
                                              Plate Number
                                              Well Position
                                              Sequence Name
                                              Sequence
                                              Barcode
        references (Optional[int]): FASTA reference file paths
        overlap (Optional[int]): required fraction of overlap for alignment to be considered
        identity (Optional[int]): required mapping fraction of overlap for alignment to be considered
    """
    r1 = os.path.abspath(r1)
    if "_R1" not in r1:
        logging.critical(
            "_R1 ('_R2' and '_I1') must exist within the read name(s).")
        sys.exit(1)
    r2 = r1.replace("_R1", "_R2")
    if not os.path.exists(r2):
        logging.critical("R2 was not found. It should be located in the same directory as R1.")
        sys.exit(1)
    i1 = r1.replace("_R1", "_I1")
    if not os.path.exists(i1):
        logging.critical(
            "I1 was not found. It should be located in the same directory as R1.")
        sys.exit(1)

    logging.info("""Processing started for RUN: {run_id}
    Barcodes file: {barcodes}
    R1 FASTQ: {r1}
    R2 FASTQ: {r2}
    I1 FASTQ: {i1}
    Barcode mismatches: {bc_mismatches}
    Barcode distance: {bc_distance}
    Join overlap: {join_overlap}
    Join difference: {join_difference}
    Master barcodes: {master_tsv}
    References: {references}
    Cross-over contamination overlap: {overlap}
    Cross-over contamination identity: {identity}""".format(**locals()))

    if out_dir:
        outd = safe_makedir(out_dir)
    else:
        outd = os.path.dirname(r1)
    # saved metadata associated with the run
    stats_dir = safe_makedir(os.path.join(outd, "run_stats"))
    # a place for everything as we'll group and tar later
    samples_dir = safe_makedir(os.path.join(outd, "sample_files"))
    # demultiplex the reads
    barcodes = preprocess_barcodes(barcodes)
    fastqs = demultiplex_fastq(barcodes, r1, out_dir=samples_dir,
                               stats_file=os.path.join(stats_dir, "demultiplexing_stats.tsv"),
                               dist_plot=os.path.join(stats_dir, "on_target_read_distribution.pdf"),
                               m=bc_mismatches, d=bc_distance, q=bc_quality)
    # this is independent of demultiplexing
    barcode_stats(run_id, i1, barcodes, count_table=os.path.join(stats_dir, "barcode_counts.csv"),
                  stat_table=os.path.join(stats_dir, "barcode_stats.csv"),
                  all_barcodes=master_tsv)
    # read count > 0
    r1_passing = [i1 for (i1, i2) in fastqs if file_exists(i1) and file_exists(i2)]
    r2_passing = [i.replace("_R1", "_R2") for i in r1_passing]
    # trim the reads
    # join the reads
    joined_fastqs = [os.path.join(samples_dir, fq.rpartition("_")[0] + "_join.fastq") for fq in r1_passing]
    # don't run join with no fastqs
    if len(r1_passing) > 0:
        joined_fastqs = batch_join_reads(r1_passing, r2_passing, joined_fastqs,
                                         join_stats=os.path.join(stats_dir, "join_stats.csv"),
                                         p=join_difference, m=join_overlap, threads=threads)
        # cross-over contamination
        if references:
            crossover_stats = crossover_contamination_check(joined_fastqs, references,
                                                            os.path.join(stats_dir, "crossover_stats.csv"),
                                                            threads=threads, overlap=overlap,
                                                            identity=identity)
    # this should not go here, but for now I want a sample stats table at the end of processing
    with open(os.path.join(stats_dir, "sample_stats.csv"), 'w') as fh:
        print("sample", "run_id", "individual_reads", "joined_pairs", "contaminated_reads", sep=",", file=fh)
        for (r1, r2) in fastqs:
            sample = os.path.basename(r1).partition("_")[0]
            stub = os.path.join(os.path.dirname(r1), sample)
            reads = read_count(r1) * 2
            try:
                joined_reads = read_count("%s_join.fastq" % stub)
            except OSError:
                joined_reads = "NA"
            try:
                with open("%s_contaminant_reads.txt" % stub) as rfh:
                    for i, line in enumerate(rfh):
                        pass
                contaminated_reads = i + 1
            except OSError:
                contaminated_reads = "NA"
            print(sample, run_id, reads, joined_reads, contaminated_reads, sep=",", file=fh)
    logging.info("Finished processing %s" % run_id)


def main():
    fmt = argparse.ArgumentDefaultsHelpFormatter
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--version', action='version',
                   version='%(prog)s {version}'.format(version=__version__))
    # p.add_argument('--config', help="configuration file")
    p.add_argument('--debug', action="store_true", help="increase verbosity")
    p.add_argument('-t', '--threads', metavar="INT", type=int, default=8,
                   help="Processing threads where applicable")
    sp = p.add_subparsers(metavar='command', dest="subparser_name", title="available functions",
                          help="description")

    spbarcodes = sp.add_parser('barcode-stats',
                               description=("Provides basic demultiplexing statistics with the "
                                            "option to check all barcodes against all previously "
                                            "used barcodes. By default, barcode counts are output "
                                            "to STDOUT."),
                               help="barcode usage statistics")
    spbarcodes.add_argument('run_id', metavar="ID",
                            help="Metadata identifier for this particular run")
    spbarcodes.add_argument('fastq', metavar="FASTQ", type=lambda x: pfile_exists(p, x),
                            help="Multiplexed index read, e.g. Undetermined I1")
    spbarcodes.add_argument('run_tsv', metavar="TSV", type=lambda x: pfile_exists(p, x),
                            help="Barcodes TSV of Name:Barcode")
    spbarcodes.add_argument('--counts', metavar="CSV",
                            help=("Capture barcode counts to this file rather than "
                                  "sending to STDOUT"))
    spbarcodes.add_argument('--master', metavar="TSV", type=lambda x: pfile_exists(p, x),
                            help=("Master barcode list as TSV containing header in the "
                                  "order of: Plate Name(s), Plate Number, Well Position, "
                                  "Sequence Name, Sequence, and Barcode"))
    spbarcodes.add_argument('--stats', metavar="CSV",
                            help="Summary statistics of observed counts; skipped if not used")

    preproc_barcodes = sp.add_parser('validate-barcodes',
                                     description=("Checks for duplicate samples, renames '+' to "
                                                  "'pos', renames ending '-' to 'neg', replace "
                                                  "any non-word characters with '-', and prepend "
                                                  "'s' if the sample ID starts with a digit."),
                                     help="validate and preprocess barcodes TSV file")
    preproc_barcodes.add_argument('tsv', metavar="TSV", type=lambda x: pfile_exists(p, x),
                                  help="Barcodes TSV file path of format NAME<tab>BARCODE")
    preproc_barcodes.add_argument('--out-file', metavar="STR",
                                  help=("Path to validated TSV file; by default it's "
                                  "written to <tsv>_validated.tsv"))

    demux = sp.add_parser('demultiplex',
                          description=("Runs demultiplexing through fastq-multx "
                                       "using barcodes file. It's recommended you "
                                       "preprocess you barcodes TSV beforehand."),
                          formatter_class=fmt,
                          help="demultiplex a fastq")
    demux.add_argument('tsv', metavar='TSV', type=lambda x: pfile_exists(p, x),
                       help="Barcodes TSV of Name:Barcode")
    demux.add_argument('r1', metavar="R1", type=lambda x: pfile_exists(p, x),
                       help='Undetermined R1 reads')
    demux.add_argument('--i1', metavar="I1", type=lambda x: pfile_exists(p, x),
                       help=('Undetermined index reads; you only have to '
                             'specify if I1 is not in the same dir as R1'))
    demux.add_argument('--r2', metavar="R2", type=lambda x: pfile_exists(p, x),
                       help=('Undetermined R2 reads; you only have to '
                             'specify if R2 is not in the same dir as R1'))
    demux.add_argument('--out-dir', metavar="STR",
                       help="Directory in which to write demultiplexed reads")
    demux.add_argument('--stats', metavar="STR",
                       help=("Capture demultiplex statistics from "
                             "fastq-multx STDOUT to this TSV"))
    demux.add_argument('--dist-plot', metavar="STR",
                       help=("Plot read distribution across samples to "
                             "this PDF; plotting is skipped if you don't "
                             "want to save the stats file"))
    demux.add_argument('-m', metavar="INT", type=int, default=0,
                       help="Allowable mismatches in barcode as long as they are unique")
    demux.add_argument('-d', metavar="INT", type=int, default=2,
                       help=("Require a minimum distance of N between the "
                             "best and the next best"))
    demux.add_argument('-q', metavar="INT", type=int, default=0,
                       help=("Require a minimum phred quality of N to "
                             "accept a barcode base"))

    joining = sp.add_parser('join-reads', formatter_class=fmt,
                            description="Join paired-end reads using fastq-join",
                            help="join paired-end reads using fastq-join")
    joining.add_argument('r1', metavar="R1", type=lambda x: pfile_exists(p, x),
                         help="R1 fastq of read set")
    joining.add_argument('r2', metavar="R2", type=lambda x: pfile_exists(p, x),
                         help="R2 fastq of read set")
    joining.add_argument('outprefix', metavar="PREFIX",
                         help="Prefix for output files '<outprefix>_join.fastq.gz'")
    joining.add_argument('-m', metavar="INT", type=int, default=240,
                         help="Minimum overlap")
    joining.add_argument('-p', metavar="INT", type=int, default=2,
                         help="Percent maximum difference")

    crosscontam = sp.add_parser('cross-over', formatter_class=fmt,
                                description=("Checks FASTQs against reference FASTAs "
                                             "and provides statistics table containing "
                                             "contamination hits per sample"),
                                help="check FASTQ(s) against control reference FASTA(s)")
    crosscontam.add_argument('--fastqs', metavar="FASTQS", required=True, nargs="+",
                             help="FASTQ file paths")
    crosscontam.add_argument('--references', metavar="REFERENCES", required=True,
                             nargs="+", help="FASTA reference file paths")
    crosscontam.add_argument('--outfile', metavar="OUTFILE", required=True,
                             help="Output stats file as CSV")
    crosscontam.add_argument('--overlap', metavar="FLOAT", default=0.95, type=float,
                             help=("Required fraction of overlap for alignment "
                                   "to be considered"))
    crosscontam.add_argument('--identity', metavar="FLOAT", default=0.99, type=float,
                             help=("Required mapping fraction of overlap for "
                                   "alignment to be considered"))

    runall = sp.add_parser('run-all', formatter_class=fmt,
                           description="Demultiplex and QC protocol",
                           help="demultiplex and QC protocol")
    runall.add_argument('run_id', metavar="RUN-ID",
                        help="Unique name for MiSeq run")
    runall.add_argument('barcodes', metavar="BARCODES", type=lambda x: pfile_exists(p, x),
                        help="Barcodes TSV of NAME:BARCODE")
    runall.add_argument('r1', metavar="R1", type=lambda x: pfile_exists(p, x),
                        help='Path to R1 fastq -- R2 and I1 must be in same directory')
    runall.add_argument('--out-dir', metavar="STR", help="Output directory")
    runall_demux = runall.add_argument_group("Demultiplexing")
    runall_demux.add_argument('--mismatches', metavar="INT", type=int, default=0,
                              help=("Allowable mismatches in barcode "
                                    "as long as they are unique"))
    runall_demux.add_argument('--distance', metavar="INT", type=int, default=2,
                              help=("Require a minimum distance of N between "
                                    "the best and the next best when allowing mismatches"))
    runall_demux.add_argument('--quality', metavar="INT", type=int, default=0,
                              help="Require a minimum phred quality of N to accept a barcode base")
    runall_join = runall.add_argument_group("Joining")
    runall_join.add_argument('--join-overlap', metavar="INT", type=int, default=240,
                             help="Minimum overlap")
    runall_join.add_argument('--join-difference', metavar="INT", type=int, default=2,
                             help="Percent maximum difference")
    runall_carryover = runall.add_argument_group("Carry-over Contamination")
    runall_carryover.add_argument('--master', metavar="TSV", type=lambda x: pfile_exists(p, x),
                                  help=("Master barcode list as TSV containing "
                                        "header in the order of: Plate Name(s), "
                                        "Plate Number, Well Position, Sequence Name, "
                                        "Sequence, and Barcode"))
    runall_crossover = runall.add_argument_group("Cross-over Contamination")
    runall_crossover.add_argument('--references', metavar="FASTAS", nargs="+",
                                  help=("FASTA reference file paths; terminate "
                                        "file list with -- (eg. r1.fa r2.fa --) "
                                        "if this is the last option used"))
    runall_crossover.add_argument('--overlap', metavar="FLOAT", default=0.95, type=float,
                                  help=("Required fraction of overlap for "
                                        "alignment to be considered"))
    runall_crossover.add_argument('--identity', metavar="FLOAT", default=0.99, type=float,
                                  help=("Required mapping fraction of overlap for "
                                        "alignment to be considered"))

    args = p.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M",
                            format="[%(asctime)s - %(name)s:%(levelname)s] %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d %H:%M",
            format="[%(asctime)s - %(name)s:%(levelname)s] %(message)s")
    logger = logging.getLogger(__name__)

    if args.subparser_name == "validate-barcodes":
        preprocess_barcodes(args.tsv, out_file=args.out_file)
    elif args.subparser_name == "barcode-stats":
        barcode_stats(args.run_id, args.fastq, args.run_tsv, count_table=args.counts,
                      stat_table=args.stats, all_barcodes=args.master)
    elif args.subparser_name == "demultiplex":
        demultiplex_fastq(args.tsv, args.r1, out_dir=args.out_dir, stats_file=args.stats,
                          dist_plot=args.dist_plot, m=args.m, d=args.d, q=args.q)
    elif args.subparser_name == "cross-over":
        crossover_contamination_check(args.fastqs, args.references, args.outfile,
                                      threads=args.threads, overlap=args.overlap,
                                      identity=args.identity)
    elif args.subparser_name == "join-reads":
        join_reads(args.r1, args.r2, args.outprefix, args.m, args.p)
    # this could easily also be recipe like Argonne's assembly service
    # 16S, join, flash, trimming, etc.
    elif args.subparser_name == "run-all":
        run_all(args.run_id, args.barcodes, args.r1, bc_mismatches=args.mismatches,
                bc_distance=args.distance, bc_quality=args.quality, join_overlap=args.join_overlap,
                join_difference=args.join_difference, master_tsv=args.master,
                references=args.references, overlap=args.overlap, identity=args.identity,
                threads=args.threads, out_dir=args.out_dir)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
