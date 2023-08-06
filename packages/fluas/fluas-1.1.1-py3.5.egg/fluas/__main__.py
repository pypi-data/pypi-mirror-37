import argparse
import logging
import os.path
import sys
from fluas import (__version__, preprocess_barcodes, preprocess_samplesheet,
                   barcode_stats, barcode_tsv_from_samplesheet, demultiplex_fastq,
                   reference_contamination_check, fastq_join, contamination_per_plate)


def pfile_exists(parser, arg):
    """Argparse file exists verification."""
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    return os.path.abspath(arg)


description = """
Barcodes
    barcode-stats               barcode usage statistics from Undetermined reads
    validate-barcodes           validate and preprocess barcodes TSV file

SampleSheet
    validate-samplesheet        validate and preprocess samplesheet XLS file
    samplesheet-to-barcodes     pull barcode TSV from samplesheet CSV
    samplesheet-to-heatmap      plot contamination heatmaps from annotated SampleSheet

Fastq
    demultiplex                 demultiplex a fastq
    join-reads                  join paired-end reads using fastq-join
    cross-over                  check FASTQ(s) against control reference FASTA(s)

"""


def main():
    fmt = argparse.ArgumentDefaultsHelpFormatter
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    # p.add_argument('--config', help="configuration file")
    p.add_argument('--debug', action="store_true", help="increase verbosity")
    p.add_argument('-t', '--threads', metavar="INT", type=int, default=8,
        help="Processing threads where applicable")

    sp = p.add_subparsers(dest="subparser_name", title="commands", description=description)

    spbarcodes = sp.add_parser('barcode-stats', description=("Provides basic demultiplexing "
        "statistics with the option to check all barcodes against all previously used barcodes. "
        "By default, barcode counts are output to STDOUT."))
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
                                                  "'s' if the sample ID starts with a digit."))
    preproc_barcodes.add_argument('tsv', metavar="TSV", type=lambda x: pfile_exists(p, x),
                                  help="Barcodes TSV file path of format NAME<tab>BARCODE")
    preproc_barcodes.add_argument('--out-file', metavar="STR",
                                  help=("Path to validated TSV file; by default it's "
                                  "written to <tsv>_validated.tsv"))

    spsamplesheet = sp.add_parser('validate-samplesheet', formatter_class=fmt,
                                   description=("Validates the sample IDs of the samplesheet in "
                                        "addition to checking POC, barcodes, and other "
                                        "required columns"))
    spsamplesheet.add_argument('excel_file', metavar="XLS",
                                help=("Excel sample sheet with a minimum of 'POC', 'SAMPLE_ID', "
                                      "'PRIMER_PLATE_NAME', 'PRIMER_PLATE_NUMBER', "
                                      "'PRIMER_WELL_POSITION', 'PRIMER_SEQUENCE_NAME', "
                                      "'SEQUENCE', 'PRIMER_BARCODE'"))
    spsamplesheet.add_argument('-o', '--out_file', metavar="FILENAME",
        help="Validated samplesheet as CSV; if not specified, SampleSheet.csv is written to excel_file directory")
    spsamplesheet.add_argument('--columns', metavar="STR",
        help=("column label and values to add onto sheet, e.g. 'SEQUENCE_CENTER:PNNL,"
              "PLATFORM:Illumina'; organized as column header and column value pairs"))
    spsamplesheet.add_argument('--reverse-complement', action="store_true",
        help="reverse complement the primer barcode")

    spbarcode_from_samplesheet = sp.add_parser('samplesheet-to-barcodes', formatter_class=fmt,
        description="Get TSV of SAMPLE:SEQUENCE from samplesheet CSV file")
    spbarcode_from_samplesheet.add_argument('samplesheet', metavar='CSV',
        help="Samplesheet CSV from 'validate-samplesheet'")
    spbarcode_from_samplesheet.add_argument('-o', '--out_file', metavar='FILENAME',
        help="Barcodes TSV output file; if not specified, barcodes.tsv is written to samplesheet directory")

    spsample_to_heatmap = sp.add_parser('samplesheet-to-heatmap', formatter_class=fmt,
        description=("From a fully annotated (contains POSITIVE_CONTROL columns) samplesheet, plot "
        "heatmaps per plate number"))
    spsample_to_heatmap.add_argument('samplesheet', metavar='CSV', help='fully annotated SampleSheet')
    spsample_to_heatmap.add_argument('out_file', metavar='PDF', help='out file path as pdf')

    demux = sp.add_parser('demultiplex', description=("Runs demultiplexing through fastq-multx "
        "using barcodes file. It's recommended you preprocess you barcodes TSV beforehand."),
        formatter_class=fmt)
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
                            description="Join paired-end reads using fastq-join")
    joining.add_argument('r1', metavar="R1", type=lambda x: pfile_exists(p, x),
                         help="R1 fastq of read set")
    joining.add_argument('r2', metavar="R2", type=lambda x: pfile_exists(p, x),
                         help="R2 fastq of read set")
    joining.add_argument('out_file', metavar="FASTQ",
                         help="Joined fastq file path")
    joining.add_argument('-m', metavar="INT", type=int, default=240,
                         help="Minimum overlap")
    joining.add_argument('-p', metavar="INT", type=int, default=2,
                         help="Percent maximum difference")

    crosscontam = sp.add_parser('cross-over', formatter_class=fmt,
                                description=("Checks FASTQs against reference FASTAs "
                                             "and provides statistics table containing "
                                             "contamination hits per sample"))
    crosscontam.add_argument('fastq', metavar="FASTQ", type=lambda x: pfile_exists(p, x),
                             help="FASTQ file path")
    crosscontam.add_argument('stats_file', metavar="CSV",
                             help="Alignment stats per reference as CSV")
    crosscontam.add_argument('hits_file', metavar="TXT",
                             help="Text file of READNAME:REFERENCE name per passing alignment")
    crosscontam.add_argument('-r', '--references', metavar="FASTA", required=True,
                             action='append', help=("FASTA reference file path; can specify "
                             "multiple times for each reference fasta"))
    crosscontam.add_argument('--overlap', metavar="FLOAT", default=0.95, type=float,
                             help=("Required fraction of overlap for alignment "
                                   "to be considered"))
    crosscontam.add_argument('--identity', metavar="FLOAT", default=0.99, type=float,
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
    elif args.subparser_name == "validate-samplesheet":
        preprocess_samplesheet(args.excel_file, args.out_file, args.columns, args.reverse_complement)
    elif args.subparser_name == "samplesheet-to-barcodes":
        barcode_tsv_from_samplesheet(args.samplesheet, args.out_file)
    elif args.subparser_name == "samplesheet-to-heatmap":
        contamination_per_plate(args.samplesheet, args.out_file)
    elif args.subparser_name == "demultiplex":
        demultiplex_fastq(args.tsv, args.r1, out_dir=args.out_dir, stats_file=args.stats,
                          dist_plot=args.dist_plot, m=args.m, d=args.d, q=args.q)
    elif args.subparser_name == "cross-over":
        reference_contamination_check(args.fastq, args.stats_file, args.hits_file, args.references,
                                      threads=args.threads, overlap=args.overlap,
                                      identity=args.identity)
    elif args.subparser_name == "join-reads":
        fastq_join(args.r1, args.r2, args.out_file, p=args.p, m=args.m)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
